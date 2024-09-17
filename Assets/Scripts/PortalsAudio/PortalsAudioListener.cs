using PortalsVR;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(PortalsVR.Portal))]
public class PortalsAudioListener : MonoBehaviour
{
    #region Fields
    [SerializeField] private Transform _player;

    private List<AudioSource> _clonedAudioSources;
    #endregion

    #region Methods
    void Start()
    {
        _clonedAudioSources = new List<AudioSource>();
        PortalsVR.Portal portal = gameObject.GetComponent<PortalsVR.Portal>();
        PortalsVR.Portal linkedPortal = portal.GetLinkedPortal();
        PortalsAudioSource[] _audioSources = Resources.FindObjectsOfTypeAll<PortalsAudioSource>();
        foreach (var portalAudio in _audioSources)
        {
            var audioSource = portalAudio.GetComponent<AudioSource>();
            float distanceAudioToPortal = Vector3.Distance(portal.transform.position, portalAudio.transform.position);

            if (distanceAudioToPortal < audioSource.maxDistance && portalAudio.GetComponent<PortalsAudioUpdate>() == null)
            {
                var positionRelativeToSameRoomPortal = gameObject.transform.InverseTransformPoint(portalAudio.transform.position);
                var linkedPortalAudiosComponent = linkedPortal.transform.Find("Audios");
                var clonedAudio = Instantiate(audioSource, linkedPortalAudiosComponent != null ? linkedPortalAudiosComponent : linkedPortal.transform);
                clonedAudio.name = $"{linkedPortal.name}: {clonedAudio.name}";
                Destroy(clonedAudio.GetComponent<PortalsAudioSource>());
                var clonedAudioUpdate = clonedAudio.gameObject.AddComponent<PortalsAudioUpdate>();
                clonedAudioUpdate.player = _player;
                clonedAudioUpdate.originalPortal = gameObject.transform;
                clonedAudioUpdate.propagatedPortal = linkedPortal.transform;
                clonedAudioUpdate.originalAudio = portalAudio.transform;
                _clonedAudioSources.Add(clonedAudio);
            }
        }
    }

    private void OnEnable()
    {
        if (_clonedAudioSources != null)
        {
            foreach (var clonedAudioSource in _clonedAudioSources)
            {
                clonedAudioSource.gameObject.SetActive(true);
            }
        }
    }

    private void OnDisable()
    {
        if (_clonedAudioSources != null)
        {
            foreach (var clonedAudioSource in _clonedAudioSources)
            {
                clonedAudioSource.gameObject.SetActive(false);
            }
        }
    }
    #endregion

}
