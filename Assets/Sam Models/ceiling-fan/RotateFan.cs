using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class RotateFan : MonoBehaviour
{
    public float angularVecolity = 2 * Mathf.PI;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        float angularDisplacement = angularVecolity * Time.deltaTime;
        transform.Rotate(0, angularDisplacement * Mathf.Rad2Deg, 0);
    }
}
