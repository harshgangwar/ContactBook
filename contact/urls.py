from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from contact.views import ContactViewSet


ContactRouter = DefaultRouter(trailing_slash=False)

ContactRouter.register(r'contact', ContactViewSet, base_name='noauth')

urlpatterns = [
    url(r'^', include(ContactRouter.urls))
]