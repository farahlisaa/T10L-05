import time
from datetime import datetime
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

def calculate_delay(target_time_str):
    target_time = datetime.strptime(target_time_str, "%d-%m-%Y %H:%M:%S")
    current_time = datetime.now()
    delay = (target_time - current_time).total_seconds()
    return max(delay, 0)

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

notifications_data = parse_notification_file('notification.txt') 

for notification_name, notification_data in notifications_data.items():
    target_time_str = notification_data.get("time")
    if target_time_str:
        delay = calculate_delay(target_time_str)
        print(f"Waiting for {delay} to show notifications: {notification_name}")
        time.sleep(delay)
        show_notification(notification_data)

print(notifications_data)
