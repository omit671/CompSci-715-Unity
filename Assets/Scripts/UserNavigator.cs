using System.Collections;
using System.Collections.Generic;
using PortalsVR;
using UnityEngine;

public class UserNavigator : MonoBehaviour
{

    private static UserNavigator _instance;
    public static UserNavigator Instance
    {
        get
        {
            if(_instance == null)
            {
                _instance = FindObjectOfType<UserNavigator>();
            }
            return _instance;
        }
    }

    [Tooltip("The list of portals that we want the user to navigate through")]
    public List<Portal> portalStack;

    public void ExitPortal(Portal portal)
    {
        if(portalStack.Count > 0) {
            Portal topPortal = portalStack[0];
            if(topPortal == portal.GetLinkedPortal()) {
                portalStack.RemoveAt(0);
            } else {
                portalStack.Insert(0, portal);
            }
        }
    }

    // Update is called once per frame
    void Update()
    {
        if(portalStack.Count > 0)
        {
            Portal nextPortal = portalStack[0];
            if(nextPortal != null)
            {
                transform.position = nextPortal.gameObject.transform.position;
            }
        } else {
            // Move the navigator off-screen.
            transform.position = new Vector3(0, -1000, 0);
        }
    }

    void OnDrawGizmosSelected() {
        Gizmos.color = Color.green;
        for (int i = 0; i < portalStack.Count - 1; i++)
        {
            Gizmos.DrawLine(
                portalStack[i].GetLinkedPortal().transform.position,
                portalStack[i + 1].transform.position
            );
        }
    }
}
