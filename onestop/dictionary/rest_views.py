from .models import EnglishWord, OshindongaWord
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import EnglishWordSerializer, OshindongaWordSerializer


class EnglishWordViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows English words to be viewed or edited.
    """
    queryset = EnglishWord.objects.all().order_by('word')
    serializer_class = EnglishWordSerializer
    permission_classes = [permissions.IsAuthenticated]


class OshindongaWordViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Oshindonga words to be viewed or edited.
    """
    queryset = OshindongaWord.objects.all().order_by('word')
    serializer_class = OshindongaWordSerializer
    permission_classes = [permissions.IsAuthenticated]