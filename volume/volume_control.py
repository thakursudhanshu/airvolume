from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

class VolumeControl:
    def __init__(self):
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            self.volume = interface.QueryInterface(IAudioEndpointVolume)
            self.min_vol, self.max_vol = self.volume.GetVolumeRange()[:2]
        except Exception as e:
            print(f"Error initializing volume control: {e}")
            self.volume = None

    def set_volume(self, level):
        if self.volume:
            vol = self.min_vol + (level / 100) * (self.max_vol - self.min_vol)
            self.volume.SetMasterVolumeLevel(vol, None)

    def get_volume(self):
        if self.volume:
            vol = self.volume.GetMasterVolumeLevel()
            return (vol - self.min_vol) / (self.max_vol - self.min_vol) * 100
        return 0