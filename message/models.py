from user.models import AuthUser
from django.db import models


class Message(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    sender = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="receiver")
    message = models.TextField(null=True, max_length=1200)
    subject = models.CharField(null=True, max_length=800)
    has_read = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    class Meta:
        db_table = "message"
        ordering = ("creation_date",)
