using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class basketball_bounce : MonoBehaviour
{
    float animTime = 0.0f;

    public float compressTime = 0.5f;
    public float bounceTime = 1.0f;

    public float compressTo = 0.3f;

    public float bounceTo = 1f;

    public float initialScale = 0.15f;

    public float floor = 0.15f/2;

    public float initialX = 0.01f;
    public float initialZ = 1.53f;


    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        animTime += Time.deltaTime;
        animTime %= (compressTime + bounceTime);

        if (animTime < compressTime) { //compress first
            transform.localPosition = new Vector3(initialX, floor, initialZ);
            float newScaleY = 1 + 4 * compressTo / (compressTime * compressTime) * (animTime - (0 + compressTime / 2)) * (animTime - (0 + compressTime / 2)) - compressTo;
            transform.localScale = new Vector3(initialScale, initialScale*newScaleY, initialScale);
        }
        else { //bounce
            transform.localScale = new Vector3(initialScale, initialScale, initialScale);
            float newY = -4 * bounceTo / (bounceTime * bounceTime) * ((animTime - compressTime) - (0 + bounceTime / 2)) * ((animTime - compressTime) - (0 + bounceTime / 2)) + bounceTo;
            transform.localPosition = new Vector3(initialX, floor+newY, initialZ);
        }


    }
}
