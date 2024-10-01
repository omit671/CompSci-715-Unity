using System.Collections.Generic;
using System.Linq;
using PortalsVR;
using UnityEngine;
using Vector3 = UnityEngine.Vector3;

class PropagatedSoundSource : MonoBehaviour
{
    public AudioSource soundSource;

    [HideInInspector] public AudioRoom parentRoom;
    [HideInInspector] private GameObject playerCamera;
    [HideInInspector] private AudioRoom prevCameraRoom = null;

    private List<List<(Portal from, Portal to)>> pathsToCamera = new ();
    public int numPaths => pathsToCamera.Count;

    private Dictionary<Portal, (AudioSource source, List<(Portal from, Portal to)> path)> temporaryAudioSources = new ();

    void Start()
    {
        // Do not clone already cloned objects.
        // Dirty workaround.
        if (gameObject.name.EndsWith("(Clone)"))
        {
            DestroyImmediate(this);
            return;
        }

        playerCamera = GameObject.FindGameObjectWithTag("MainCamera");
        RecalculateAudio();
    }

    void Update()
    {
        if (playerCamera == null)
        {
            playerCamera = GameObject.FindGameObjectWithTag("MainCamera");
        }

        if (prevCameraRoom != AudioRoom.currentRoom)
        {
            // The player has moved to a different room,
            // we need to recalculate the paths to the player.
            RecalculateAudio();
        }

        prevCameraRoom = AudioRoom.currentRoom;

        foreach ((AudioSource source, var path) in temporaryAudioSources.Values)
        {
            source.transform.position = path[0].from.GetClosestPoint(playerCamera.transform.position);
            source.transform.position += (source.transform.position - playerCamera.transform.position).normalized * GetPathLength(path);
        }
    }

    void OnDrawGizmosSelected()
    {
        // Draw the paths to the camera.
        foreach (List<(Portal from, Portal to)> path in pathsToCamera)
        {
            for (int i = 0; i < path.Count; i++)
            {
                if (i != path.Count - 1)
                {
                    Gizmos.color = Color.green;
                    Gizmos.DrawLine(path[i].from.transform.position, path[i].to.transform.position);
                }
                Gizmos.color = Color.red;
                Gizmos.DrawLine(path[i].to.transform.position, path[i].from.transform.position);
            }
        }
    }

    float GetPathLength(List<(Portal from, Portal to)> path)
    {
        float distance = 0;

        // distance += Vector3.Distance(path[0].from.transform.position, playerCamera.transform.position);
        distance += Vector3.Distance(path[path.Count - 1].to.transform.position, soundSource.transform.position);

        for (int i = 0; i < path.Count - 1; i++)
        {
            distance += Vector3.Distance(path[i].to.transform.position, path[i + 1].from.transform.position);
        }

        return distance;
    }

    // This is only called when the player moves to a different room.
    // This generates a path between the player and the sound source,
    // but is very rough. The path is refined in the PathRefiner class.
    void RecalculateAudio()
    {
        // Destroy the temporary audio sources.
        foreach ((AudioSource audioSource, _) in temporaryAudioSources.Values)
        {
            Destroy(audioSource.gameObject);
        }
        temporaryAudioSources.Clear();
        pathsToCamera.Clear();

        if (AudioRoom.currentRoom == null)
        {
            soundSource.mute = true;
            return;
        }

        if (AudioRoom.currentRoom == parentRoom)
        {
            soundSource.mute = false;
            return;
        }
        soundSource.mute = true;

        Portal[] playerPortals = AudioRoom.currentRoom.portals;
        Portal[] soundPortals = parentRoom.portals;

        foreach (Portal playerPortal in playerPortals)
        {

            List<List<(Portal, Portal)>> potentialPaths = new ();
            foreach (Portal soundPortal in soundPortals)
            {
                var path = playerPortal.FindShortestPathTo(soundPortal);

                if (path != null && path.Count > 0)
                {
                    potentialPaths.Add(path);
                }
            }

            // Sort the potential paths by length.
            potentialPaths.Sort((a, b) => GetPathLength(a).CompareTo(GetPathLength(b)));
            Debug.Log("Potential paths: " + potentialPaths.Count);

            if (potentialPaths.Count > 0)
            {
                var pathApproximation = potentialPaths.First();
                pathsToCamera.Add(pathApproximation);

                // Create a temporary audio source for this path.
                if (!temporaryAudioSources.ContainsKey(playerPortal))
                {
                    AudioSource source = Instantiate(soundSource, playerPortal.transform);
                    source.time = soundSource.time;
                    source.transform.position = playerPortal.GetClosestPoint(playerCamera.transform.position);
                    source.mute = false;

                    temporaryAudioSources.Add(playerPortal, (source, pathApproximation));
                }
            }
        }

    }
}