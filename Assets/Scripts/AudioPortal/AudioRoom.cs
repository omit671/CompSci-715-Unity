using System.Linq;
using PortalsVR;
using UnityEngine;

public class AudioRoom : MonoBehaviour
{ 
    public Portal[] portals;
    public static AudioRoom currentRoom;
    private BoxCollider collider;

    void Start() {
        GetComponentsInChildren<AudioSource>().ToList().ForEach(obj => {
            var pss = obj.gameObject.AddComponent<PropagatedSoundSource>();
            pss.soundSource = obj;
            pss.parentRoom = this;
        });

        var bounds = new Bounds() {
            center = transform.position,
            size = Vector3.zero
        };

        GetComponentsInChildren<Renderer>().ToList().ForEach(renderer => {
            bounds.Encapsulate(renderer.bounds);
        });

        collider = gameObject.AddComponent<BoxCollider>();
        collider.size = bounds.size;

        portals = FindObjectsOfType<Portal>()
            .Where(portal => bounds.Contains(portal.transform.position))
            .ToArray();

        foreach(Portal portal in portals) {
            portal.parentRoom = this;
        }

        GameObject player = GameObject.FindGameObjectWithTag("Player");
        if(bounds.Contains(player.transform.position)) {
            currentRoom = this;
        }
    }

    void Update() {
        GameObject player = GameObject.FindGameObjectWithTag("Player");
        if(collider.bounds.Contains(player.transform.position) && currentRoom != this) {
            Debug.Log("Player has entered room " + name);
            currentRoom = this;
        }
    }

    // void OnDrawGizmos()
    // {
    //     Gizmos.color = currentRoom == this ? Color.blue : Color.red;
    //     Gizmos.DrawWireCube(
    //         bounds.center,
    //         bounds.size
    //     );
    // }

    public bool IsInside(Vector3 position) => collider.bounds.Contains(position);
}
