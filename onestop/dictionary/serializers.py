from rest_framework import serializers

from .models import EnglishWord, OshindongaPhonetic, OshindongaWord


class EnglishWordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EnglishWord
        fields = ["url", "id", "word", "word_case"]


class OshindongaWordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OshindongaWord
        fields = ["url", "id", "english_word", "word", "word_case", "word_phonetics"]


class OshindongaPhoneticSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OshindongaPhonetic
        fields = ["url", "id", "oshindonga_word", "pronunciation", "phonetics"]
