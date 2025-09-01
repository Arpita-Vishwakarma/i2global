from django.db import models

# Create your models here.
import uuid
from django.db import models
from users.models import User


class Note(models.Model):
    note_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    note_title = models.CharField(max_length=255)
    note_content = models.TextField()
    owner = models.ForeignKey(User, related_name="notes", on_delete=models.CASCADE)
    last_update = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.note_title
