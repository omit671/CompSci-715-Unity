using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(AudioSource))]
public class PortalsAudioUpdate : MonoBehaviour
{
    public Transform player;
    public Transform originalPortal;
    public Transform propagatedPortal;
    public Transform originalAudio;
    private readonly float halfPortal = 0.5f;
    private float volume;

    // Start is called before the first frame update
    void Start()
    {
        volume = gameObject.GetComponent<AudioSource>().volume;
        updateAudio();
    }

    // Update is called once per frame
    void Update()
    {
        updateAudio();
    }

    private void updateAudio()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            Debug.Log(gameObject.name + " Player x Portal Point: " + propagatedPortal.InverseTransformPoint(player.position).ToString());
            Debug.Log(gameObject.name + " Sound Point: " + transform.position.ToString());
            Debug.Log(gameObject.name + " distance: " + Vector3.Distance(propagatedPortal.position, player.position));
        }

        var audioPointRelativeToOriginalPortal = originalPortal.InverseTransformPoint(originalAudio.position);
        var playerPointRelativeToPropagatedPortal = propagatedPortal.InverseTransformPoint(player.position);
        var audioPointRelativeToPropagatedPortal = audioPointRelativeToOriginalPortal;
        var audioPropagatedVolume = volume;

        if (Mathf.Abs(playerPointRelativeToPropagatedPortal.x) > halfPortal)
        {
            audioPointRelativeToPropagatedPortal = Vector3.Reflect(audioPointRelativeToPropagatedPortal, Vector3.right);
        }

        if (Mathf.Sign(playerPointRelativeToPropagatedPortal.z) == Mathf.Sign(audioPointRelativeToOriginalPortal.z))
        {
            audioPointRelativeToPropagatedPortal = Vector3.Reflect(audioPointRelativeToPropagatedPortal, Vector3.forward);
            audioPropagatedVolume *= 0.8f;
        }

        //var distancePlayerToPropagatedPortal = Vector3.Distance(propagatedPortal.position, player.position);
        //audioPropagatedVolume -= Mathf.Round(distancePlayerToPropagatedPortal) * (volume / 10);

        gameObject.GetComponent<AudioSource>().volume = audioPropagatedVolume;
        transform.position = propagatedPortal.TransformPoint(audioPointRelativeToPropagatedPortal);

        if (Mathf.Abs(playerPointRelativeToPropagatedPortal.x) < halfPortal && Mathf.Abs(playerPointRelativeToPropagatedPortal.z) < halfPortal)
        {
            transform.LookAt(player.position);
        }
        else
        {
            transform.LookAt(propagatedPortal.position);
        }
    }
}
