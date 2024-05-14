from win10toast import ToastNotifier
import winsound 


toaster=ToastNotifier()
toaster.show_toast("Title",
                   "Message",
                   duration=2)
    
sound_path="noti_sound.wav"
winsound.PlaySound(sound_path, winsound.SND_ALIAS)