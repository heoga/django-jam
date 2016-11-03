from django.conf.urls import url, include
from rest_framework import routers

from .serializers.user import UserViewSet
from .serializers.profile import ProfileViewSet

from .views.dashboard import DashboardView

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^$', DashboardView.as_view(), name='dashboard'),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls'))
]
