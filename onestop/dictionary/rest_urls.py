from django.urls import include, path
from rest_framework import routers
from . import rest_views

router = routers.DefaultRouter()
router.register(r'english_words', rest_views.EnglishWordViewSet)
router.register(r'oshindonga_words', rest_views.OshindongaWordViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]