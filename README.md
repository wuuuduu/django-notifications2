
# django-notifications

### Quick start


1. Add "django_notifications" to your INSTALLED_APPS setting like this:
    ```
        INSTALLED_APPS = [
            ...
            'django_notifications',
        ]
    ```

1. Run `python manage.py migrate` to create the django_notifications models.

1. Settings:
    ```
    MAX_ATTEMPTS_NUMBER: [DEFAULT=3] 
    How many times should we try to send a notification. If the number is reached, the notification will be removed.
   ```

1. Examples
 
    a) Creating e-mail notification:
    ```python3
    NotificationQueue.objects.create(
        custom_notification_id='USER1_LOGGED_IN_070920202201', 
        backend='email', 
        data={
            'subject': 'Login from a new device', 
            'body': '<h1>It looks like you’ve recently signed in.....</h1>', 
            'to': 'email@localhost'
        }
    )
   
   ...
   from django_notifications.helpers import EmailNotificationQueueManagement
   EmailNotificationQueueManagement().send_notifications()
   
   # if the notification is not sent, it will go to the error queue
   
   from django_notifications.helpers import EmailNotificationErrorQueueManagement
   
   EmailNotificationErrorQueueManagement().send_notifications()
    ```