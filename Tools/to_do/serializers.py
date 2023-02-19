from rest_framework import serializers
from to_do.models import Entry

class ToDoSerializer(serializers.ModelSerializer):
    url = serializers.CharField(max_length = 200, allow_blank = True)
    class Meta:
        model = Entry
        fields = ('uid',
                 'completed',
                 'complete_time',
                 'title',
                 'url')