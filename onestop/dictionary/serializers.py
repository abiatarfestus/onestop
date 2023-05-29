from .models import EnglishWord, OshindongaWord
from rest_framework import serializers


class EnglishWordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EnglishWord
        fields = ["url", "word", "word_case"]


class OshindongaWordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OshindongaWord
        fields = ["url", "english_word", "word", "word_case", "word_phonetics"]