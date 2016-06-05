from django.db import models
from django.conf import settings
from model_utils.models import TimeStampedModel


class Message(TimeStampedModel):
    """
    Model to create email.

    :sender: A single person who can send email.
    :receivers: A single person can send email to multiple receivers.
    :msg_header: An email contains a title.
    :msg_content: An email contains a body.
    """
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sender")
    receivers = models.ManyToManyField(
        settings.AUTH_USER_MODEL)
    msg_header = models.CharField(max_length=500)
    msg_content = models.TextField()

    def __str__(self):
        return self.sender + ': ' + self.recievers
