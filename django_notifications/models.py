from django.db import models
from django.utils.translation import gettext_lazy as _


class NotificationQueueQuerySet(models.QuerySet):
    def normal_queue(self):
        return self.filter(queue=NotificationQueue.STANDARD_QUEUE)

    def error_queue(self):
        return self.filter(queue=NotificationQueue.ERROR_QUEUE)


class NotificationQueue(models.Model):
    STANDARD_QUEUE = 1
    ERROR_QUEUE = 2

    QUEUES = (
        (STANDARD_QUEUE, _('Standard queue')),
        (ERROR_QUEUE, _('Error queue')),
    )
    attempts_number = models.PositiveIntegerField(default=0, null=False)
    backend = models.CharField(max_length=255, blank=False, null=False)  # e-mail, discord, messenger etc
    custom_notification_id = models.CharField(max_length=255, null=False, blank=False)
    data = models.JSONField()
    queue = models.PositiveSmallIntegerField(choices=QUEUES, default=STANDARD_QUEUE, null=False)
    created = models.DateTimeField(auto_now_add=True)

    objects = NotificationQueueQuerySet().as_manager()

    class Meta:
        unique_together = ('custom_notification_id', 'backend')

    def __str__(self):
        return f'id: {self.pk} - {self.custom_notification_id} via {self.backend}'
