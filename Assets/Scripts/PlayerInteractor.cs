using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerInteractor : MonoBehaviour
{
    [SerializeField] private GameObject stopRecording;
    [SerializeField] private GameObject startTasks;
    [SerializeField] private GameObject firstTask;
    [SerializeField] private GameObject secondTask;
    [SerializeField] private GameObject thirdTask;

    private void OnTriggerEnter(Collider other)
    {
        if (other.gameObject.tag == "StartRecording")
        {
            Recorder.Main.StartRecording();
            GameObject.FindGameObjectWithTag("StartRecording").SetActive(false);
            startTasks.SetActive(true);
        }
        else if (other.gameObject.tag == "StartTask")
        {
            Recorder.Main.PlaySuccessAudio();
            GameObject.FindGameObjectWithTag("StartTask").SetActive(false);
            firstTask.SetActive(true);
        }
        else if (other.gameObject.tag == "FirstTask")
        {
            Recorder.Main.PlaySuccessAudio();
            GameObject.FindGameObjectWithTag("FirstTask").SetActive(false);
            secondTask.SetActive(true);
        }
        else if (other.gameObject.tag == "SecondTask")
        {
            Recorder.Main.PlaySuccessAudio();
            GameObject.FindGameObjectWithTag("SecondTask").SetActive(false);
            thirdTask.SetActive(true);
        }
        else if (other.gameObject.tag == "ThirdTask")
        {
            Recorder.Main.PlaySuccessAudio();
            GameObject.FindGameObjectWithTag("ThirdTask").SetActive(false);
            stopRecording.SetActive(true);
        }
        else if (other.gameObject.tag == "StopRecording")
        {
            Recorder.Main.StopRecording();
        }
    }
}
