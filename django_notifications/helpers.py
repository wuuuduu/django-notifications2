import logging
from abc import ABC
from smtplib import SMTPException
from typing import List, Union, Type
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.db import transaction, OperationalError
from django.utils import timezone

from django_notifications.models import NotificationQueue, NotificationQueueQuerySet

logger = logging.getLogger(__name__)


class BaseNotificationQueueManagement:
    KLASS: Type[NotificationQueue]
    backend: str

    def get_notifications(self) -> Union[NotificationQueueQuerySet, List[NotificationQueue]]:
        return self.KLASS.objects.select_for_update(nowait=True).filter(
            backend=self.backend,
            send_after__lte=timezone.now()
        )

    def delete_notification(self, notification: NotificationQueue):
        return notification.delete()

    def send_notification(self, notification: NotificationQueue):
        raise NotImplementedError()

    def successfully_sent_notification(self, notification: NotificationQueue):
        logger.info(
            'Notification<%s_%s> has been sent successfully.' % (
                notification.backend, notification.custom_notification_id
            )
        )
        self.delete_notification(notification=notification)

    def error_sending_notification(self, notification: NotificationQueue, error_message: str):
        raise NotImplementedError()

    @transaction.atomic()
    def send_notifications(self):
        try:
            notifications = self.get_notifications()
            for notification in notifications:
                self.send_notification(notification)

        except OperationalError as e:
            logger.info('Table is locked. %s' % e)


class NotificationQueueManagement(BaseNotificationQueueManagement, ABC):
    KLASS = NotificationQueue

    def get_notifications(self):
        queryset = super(NotificationQueueManagement, self).get_notifications()
        return queryset.normal_queue()

    def error_sending_notification(self, notification: NotificationQueue, error_message: str):
        logger.warning(
            'Notification<%s> has not been send: %s' % (notification, error_message)
        )
        notification.queue = NotificationQueue.ERROR_QUEUE
        notification.save()


class NotificationErrorQueueManagement(NotificationQueueManagement, ABC):

    def get_notifications(self):
        queryset = super(NotificationQueueManagement, self).get_notifications()
        return queryset.error_queue()

    def error_sending_notification(self, notification: NotificationQueue, error_message: str):
        logger.error(
            'Notification<%s> has not been send: %s' % (notification, error_message)
        )

        notification.attempts_number += 1
        notification.save(update_fields=['attempts_number'])

        max_attempts_number: int = getattr(settings, 'MAX_ATTEMPTS_NUMBER', 3)

        if notification.attempts_number >= max_attempts_number:
            logger.error(
                'Notification<%s> has been deleted because max attempts number(%s) has been reached(%s): %s' % (
                    notification,
                    max_attempts_number, notification.attempts_number,
                    error_message
                )
            )
            self.delete_notification(notification=notification)


class EmailNotificationQueueManagement(NotificationQueueManagement):
    backend = 'email'

    def send_notification(self, notification: NotificationQueue):

        logger.info('Processing %s' % notification)

        email = EmailMultiAlternatives(
            subject=notification.data.get('subject'),
            body='',
            to=[notification.data.get('to')],
            headers={'Message-ID': notification.custom_notification_id},
        )

        email.mixed_subtype = 'related'  # if we want to use images in html (cid:..)

        email.attach_alternative(content=notification.data.get('body'), mimetype='text/html')
        try:
            email.send(fail_silently=False)
            self.successfully_sent_notification(notification=notification)
        except (SMTPException, OSError) as e:
            self.error_sending_notification(notification=notification, error_message=str(e))


class EmailNotificationErrorQueueManagement(NotificationErrorQueueManagement, EmailNotificationQueueManagement):
    pass
