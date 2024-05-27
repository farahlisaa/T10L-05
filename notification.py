import time
from winotify import Notification, audio

# Function to parse the notification.txt file
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

# Parse the file to get the customization data
notifications_data = parse_notification_file('notification.txt')

# Function to create and show a notification
def show_notification(notification_data):
    toast = Notification(
        app_id=notification_data.get('app_id', 'DefaultAppID'),
        title=notification_data.get('title', 'Default Title'),
        msg=notification_data.get('msg', 'Default Message'),
        duration=notification_data.get('duration', 'short')
    )

    # Set audio and looping based on parsed data
    if 'audio' in notification_data:
        toast.set_audio(getattr(audio, notification_data['audio']), loop=notification_data.get('loop', 'False') == 'True')

    # Add action based on parsed data
    if 'label' in notification_data and 'launch' in notification_data:
        toast.add_actions(label=notification_data['label'], launch=notification_data['launch'])

    # Show the notification
    toast.show()

# Show all notifications from the parsed data
for notification_name, notification_data in notifications_data.items():
    show_notification(notification_data)

# For demonstration purposes, printing the parsed data
print(notifications_data)

 
