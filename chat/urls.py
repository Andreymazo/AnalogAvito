from chat.apps import ChatConfig
from django.urls import include, path

from chat.views import message_detail, message_list


app_name = ChatConfig.name

urlpatterns = [
    path("message_list/", message_list, name="message_list"),
    path("message_detail/<int:pk>", message_detail, name="message_detail"),
   
]