import time
from datetime import datetime, timedelta
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
    target_time = datetime.strptime(target_time_str, "%H:%M:%S").time()
    current_time = datetime.now().time()

    # Debug statements to check current time and target time
    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Target time: {target_time.strftime('%H:%M:%S')}")

    # Calculate target datetime for today
    target_datetime = datetime.combine(datetime.today(), target_time)

    # Check if the target time is exactly the current time
    if target_time.hour == current_time.hour and target_time.minute == current_time.minute:
        delay = 0
    else:
        # Calculate delay in seconds
        delay = (target_datetime - datetime.now()).total_seconds()

        # If the target time is in the past, but within the same hour, set delay to 0
        if delay < 0 and target_datetime.date() == datetime.now().date():
            target_time = datetime.combine(datetime.today(), target_time)
            if target_time > datetime.now():
                delay = (target_time - datetime.now()).total_seconds()
            else:
                delay = -1

    return delay


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


notifications_data = parse_notification_file('notification.txt')

for notification_name, notification_data in notifications_data.items():
    target_time_str = notification_data.get("time")
    if target_time_str:
        delay = calculate_delay(target_time_str)
        if delay >= 0:
            print(f"Waiting for {delay} seconds to show notification: {notification_name}")
            time.sleep(delay)
            show_notification(notification_data)
        else:
            print(f"Error: Target time for notification '{notification_name}' has already passed for today")
    else:
        print(f"Error: 'time' key not found for notification '{notification_name}'")

print(notifications_data)


