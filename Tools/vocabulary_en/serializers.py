from rest_framework import serializers
# from bookmark_collection.serializers import EntrySerializer
from vocabulary_en.models import Word, TouchHistory, Interpretation

class WordSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(WordSerializer, self).__init__(many = many, *args, **kwargs)
    class Meta:
        model = Word
        fields = ('uid',
                  'word',
                  'rating',
                  'count')

class TouchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TouchHistory
        fields = ('uid',
                  'touchee',
                  'rate')

class InterpretationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interpretation
        fields = ('uid',
                   'word',
                   'interpretation')