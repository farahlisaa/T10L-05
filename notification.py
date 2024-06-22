import time
from datetime import datetime
from winotify import Notification, audio
import sqlite3

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

def show_notification(notification_data):
    toast = Notification(
        app_id=notification_data.get('app_id', 'DefaultAppID'),
        title=notification_data.get('title', 'Default Title'),
        msg=notification_data.get('msg', 'Default Message'),
        duration=notification_data.get('duration', 'short'),
        icon=notification_data.get('icon')
    )

    if 'audio' in notification_data:
        toast.set_audio(getattr(audio, notification_data['audio']),
                        loop=notification_data.get('loop', 'False').lower() == 'true')

    if 'label' in notification_data and 'launch' in notification_data:
        toast.add_actions(label=notification_data['label'], launch=notification_data['launch'])

    toast.show()

def check_and_notify(db_path, notification_file):
    notifications_data = parse_notification_file(notification_file)
    notification_data = notifications_data.get('Login Reminder', {})

    if not notification_data:
        print("Notification configuration not found.")
        return

    target_time = datetime.strptime(notification_data.get("time", "12:30:00"), "%H:%M:%S").time()
    current_time = datetime.now().time()

    if current_time >= target_time:
        today_str = datetime.now().strftime('%d/%m/%Y')

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM expenses WHERE date = ?", (today_str,))
        expenses_count = cursor.fetchone()[0]

        conn.close()

        if expenses_count == 0:
            show_notification(notification_data)




