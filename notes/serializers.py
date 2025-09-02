from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["note_id", "note_title", "note_content", "owner", "created_on", "last_update"]
        read_only_fields = ["note_id", "owner", "created_on", "last_update"]
