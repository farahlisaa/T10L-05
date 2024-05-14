import time
from winotify import Notification, audio

toast=Notification(app_id="FinanceBook", 
                   title="Bill reminders!!",
                   msg="Your bill is overdue, please make a payment asap",
                   duration="short")


toast.set_audio(audio.LoopingCall, loop=False)

#the link is an example
toast.add_actions(label="Click Me!", launch="https://ebwise.mmu.edu.my/course/view.php?id=7193")

toast.show()
 