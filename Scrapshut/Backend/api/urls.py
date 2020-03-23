# myapi/urls.py
from django.urls import include, path
from django.conf.urls import url
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
# router.register(r'urls', views.URLViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^url_verification',views.url_verification),
    url(r'^add_review',views.add_review),
    url(r'^user_login',views.user_login),
    url(r'^user_signup',views.user_signup),
    # path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]