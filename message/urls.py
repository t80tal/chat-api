from django.urls import path
from . import views


urlpatterns = [
    path("all/", views.get_messages),
    path("unread/", views.get_undread_messages),
    path("create/", views.create_message),
    path("read/<int:message_id>/", views.read_message),
    path("delete/<int:message_id>/", views.delete_message),
]
