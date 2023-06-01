from rest_framework import permissions, viewsets

from .models import EnglishWord, OshindongaPhonetic, OshindongaWord
from .serializers import (
    EnglishWordSerializer,
    OshindongaPhoneticSerializer,
    OshindongaWordSerializer,
)


class EnglishWordViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows English words to be viewed or edited.
    """

    queryset = EnglishWord.objects.all().order_by("word")
    serializer_class = EnglishWordSerializer
    permission_classes = [permissions.IsAuthenticated]


class OshindongaWordViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Oshindonga words to be viewed or edited.
    """

    queryset = OshindongaWord.objects.all().order_by("word")
    serializer_class = OshindongaWordSerializer
    permission_classes = [permissions.IsAuthenticated]


class OshindongaPhoneticViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Oshindonga phonetics to be viewed or edited.
    """

    queryset = OshindongaPhonetic.objects.all().order_by("oshindonga_word")
    serializer_class = OshindongaPhoneticSerializer
    permission_classes = [permissions.IsAuthenticated]
