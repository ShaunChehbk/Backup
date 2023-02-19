from rest_framework import serializers
from bookmark_collection.models import Entry

import logging

class EntrySerializer(serializers.ModelSerializer):
    description = serializers.CharField(max_length = 200, allow_blank = True)
    title = serializers.CharField(max_length = 200, allow_blank = True)
    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(EntrySerializer, self).__init__(many = many, *args, **kwargs)

    def update(self, instance, validated_data):
        logging.debug("updating")
        instance.hash = validated_data.get('hash', instance.hash)
        instance.url = validated_data.get('url', instance.url)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        return super().update(instance, validated_data)
        # return instance
    class Meta:
        model = Entry
        fields = ('uid',
                  'hash',
                  'title',
                  'url',
                  'description')
        # read_only_fields = ['uid']
    