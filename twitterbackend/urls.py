from django.contrib import admin
from django.urls import include, path
from twitter.viewsets import UserViewSet, TweetViewSet
from rest_framework.routers import DefaultRouter
from twitter.viewsets import ChatMessageViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path("admin/", admin.site.urls),
    path('users/<int:user_id>/tweet/', TweetViewSet.as_view({'post': 'create'}), name='user_tweet_create'),
    path('users/tweet/<int:tweet_id>/delete/', TweetViewSet.as_view({'delete': 'delete_tweet'}), name='tweet-delete'),
    path('users/<int:pk>/follow/<int:target_pk>', UserViewSet.as_view({'post': 'follow'}), name='user-follow'),
    path('users/<int:pk>/unfollow/<int:target_pk>', UserViewSet.as_view({'post': 'unfollow'}), name='user-unfollow'),
    path('users/<int:user_id>/user_messages/', ChatMessageViewSet.as_view({'get': 'user_messages'}), name='user-messages'),
    path('users/<int:user_id>/send_message/<int:receiver_id>/', ChatMessageViewSet.as_view({'post': 'send_message'}), name='send-message'),
]
