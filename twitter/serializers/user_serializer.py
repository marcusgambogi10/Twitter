from rest_framework import serializers
from twitter.serializers.tweet_serializer import TweetSerializer

from twitter.models import User

class UserSerializer(serializers.ModelSerializer):
    follows = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    tweets = TweetSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'follows', 'followers', 'tweets']
        
    def get_follows(self, obj):
        return obj.follows.values('id', 'name', 'email',)
    
    def get_followers(self, obj):
        return obj.followers.values('id', 'name', 'email',)
        
    def get_tweets(self, obj):
        tweets = obj.get_tweets()
        tweet_data = []
        for tweet in tweets:
            tweet_serializer = TweetSerializer(tweet)
            tweet_data.append(tweet_serializer.data)
        return tweet_data
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['tweets'] = self.get_tweets(instance)
        return data