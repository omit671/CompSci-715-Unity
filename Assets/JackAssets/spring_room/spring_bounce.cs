using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class spring_bounce : MonoBehaviour
{
    float animTime = 0.0f;

    public float compressTime = 0.5f;
    public float bounceTime = 1.0f;

    public float compressTo = 0.3f;

    public float bounceTo = 1f;


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
            transform.localPosition = new Vector3(0, 0, 0);
            float newScaleY = 1 + 4 * compressTo / (compressTime * compressTime) * (animTime - (0 + compressTime / 2)) * (animTime - (0 + compressTime / 2)) - compressTo;
            transform.localScale = new Vector3(1, newScaleY, 1);
        }
        else { //bounce
            transform.localScale = new Vector3(1, 1, 1);
            float newY = -4 * bounceTo / (bounceTime * bounceTime) * ((animTime - compressTime) - (0 + bounceTime / 2)) * ((animTime - compressTime) - (0 + bounceTime / 2)) + bounceTo;
            transform.localPosition = new Vector3(0, newY, 0);
        }


    }
}
