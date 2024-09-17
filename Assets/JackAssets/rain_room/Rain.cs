using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Rain : MonoBehaviour
{

    public GameObject rainDrop;
    public Vector3 spawnArea = new Vector3(10, 10, 10);
    public float spawnRate = 0.1f;
    public float gravity = 9.8f;
    public float lifetime = 1.0f;

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
        Vector3 spawnPosition = new Vector3(Random.Range(-spawnArea.x/2, spawnArea.x/2), spawnArea.y, Random.Range(-spawnArea.z/2, spawnArea.z/2));
        GameObject drop = Instantiate(rainDrop, transform.position + spawnPosition, Quaternion.identity);
        StartCoroutine(Drop(drop));
    }

    private IEnumerator Drop(GameObject drop) {
        Rigidbody rb = drop.AddComponent<Rigidbody>();
        rb.useGravity = false;
        rb.velocity = new Vector3(0, -gravity, 0);

        float time = 0;
        while (time < lifetime) {
            rb.velocity = new Vector3(0, -gravity, 0);
            time += Time.deltaTime;
            yield return null;
        }

        Destroy(drop);
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
