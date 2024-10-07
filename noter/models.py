from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"Note by {self.user.username}"


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class NoteTag(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('note', 'tag')

    def __str__(self):
        return f"{self.tag.name} tagged to {self.note.id}"


class UserPrefs(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=50, default='light')
    notifs_enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"Preferences for {self.user}"


class AuditLogs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    action_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AuditLog by {self.user.username} - {self.action} at {self.action_time}"
