import time
from winotify import Notification, audio

def parse_notification_file(filename):
    notifications = {}
    current_notification = None

    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith('[') and line.endswith(']'):
                current_notification = line[1:-1]
                notifications[current_notification] = {}
            elif '=' in line and current_notification:
                key, value = line.split('=', 1)
                notifications[current_notification][key] = value

    return notifications

notifications_data = parse_notification_file('notification.txt')

def show_notification(notification_data):
    toast = Notification(
        app_id=notification_data.get('app_id', 'DefaultAppID'),
        title=notification_data.get('title', 'Default Title'),
        msg=notification_data.get('msg', 'Default Message'),
        duration=notification_data.get('duration', 'short')
    )

    if 'audio' in notification_data:
        toast.set_audio(getattr(audio, notification_data['audio']), loop=notification_data.get('loop', 'False') == 'True')

    if 'label' in notification_data and 'launch' in notification_data:
        toast.add_actions(label=notification_data['label'], launch=notification_data['launch'])

    toast.show()

for notification_name, notification_data in notifications_data.items():
    delay = int(notification_data.get('delay', 0))
    time.sleep(delay)
    show_notification(notification_data)

print(notifications_data)
