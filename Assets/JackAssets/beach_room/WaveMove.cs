using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class WaveMove : MonoBehaviour
{

    public float initialX = 0;
    public float initialZ = 0;

    public float lowerY = 0;
    public float upperY = 1;

    public float animSpeed = 1;

    public float phaseShift = 0;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        transform.localPosition = new Vector3(initialX, lowerY + (upperY - lowerY) * Mathf.Sin(Time.time * animSpeed + phaseShift), initialZ);
    }
}
