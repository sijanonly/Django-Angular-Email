from django.conf.urls import url

from emailapp.views import EmailView

from .api import (
    MessagePost, MessageList,
    SentMesssageList
)


urlpatterns = [

    url(
        r'^$',
        EmailView.as_view(),
        name='email'),

    url(
        r'^api/$',
        MessageList.as_view(),
        name='inbox-message-list'
    ),
    url(
        r'^api/sent/$',
        SentMesssageList.as_view(),
        name='sent-message-list'
    ),

    url(
        r'^api/post/$',
        MessagePost.as_view(),
        name='message-post'),
]
