using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Rain : MonoBehaviour
{

    public GameObject rainDrop;
    public Vector3 spawnArea = new Vector3(10, 10, 20);
    public float spawnRate = 0.1f;
    public float velocity = 9.8f;
    public float lifetime = 1.0f;

    public float spawnAmount = 5;

    // Start is called before the first frame update
    void Start()
    {
        StartCoroutine(SpawnRain());
    }

    private IEnumerator SpawnRain() {
        while (true) {
            SpawnRainDrop();
            yield return new WaitForSeconds(spawnRate);
        }
    }

    private void SpawnRainDrop() {
        
        for(int i = 0; i < spawnAmount; ++i) {
            Vector3 spawnPosition = new Vector3(Random.Range(-spawnArea.x/2, spawnArea.x/2), spawnArea.y, Random.Range(-spawnArea.z/2, spawnArea.z/2));
            GameObject drop = Instantiate(rainDrop, transform.position + spawnPosition, Quaternion.identity);
            StartCoroutine(Drop(drop));
        }

    }

    private IEnumerator Drop(GameObject drop) {

        float time = 0;
        while (time < lifetime) {
            drop.transform.position += new Vector3(0, -velocity, velocity/2) * Time.deltaTime;
            time += Time.deltaTime;
            yield return null;
        }

        Destroy(drop);
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    private void OnEnable()
    {
        StartCoroutine(SpawnRain());
    }

    private void OnDisable()
    {
        StopCoroutine(SpawnRain());
        GameObject[] allDrops = GameObject.FindGameObjectsWithTag("RainDrop");
        foreach (GameObject drop in allDrops)
        {
            Destroy(drop);
        }
    }
}
