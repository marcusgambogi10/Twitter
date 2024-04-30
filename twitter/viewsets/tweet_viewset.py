from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from twitter.models import Tweet, User
from twitter.serializers import TweetSerializer

class TweetViewSet(viewsets.ViewSet):
    def create(self, request, user_id=None):
        # Get the user object or return 404 if not found
        user = get_object_or_404(User, pk=user_id)

        # Add the user object to the request data
        tweet_data = request.data
        tweet_data['author'] = user.id  # Assuming 'author' is the field name in your TweetSerializer

        # Serialize the tweet data
        serializer = TweetSerializer(data=tweet_data)

        # Validate the serializer
        if serializer.is_valid():
            # Save the tweet with the user object as the author
            tweet = serializer.save(author=user)
            return Response(TweetSerializer(tweet).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete_tweet(self, request, tweet_id):
        tweet = get_object_or_404(Tweet, id=tweet_id)
        tweet.delete()
        return Response({"message": "Tweet excluído com sucesso"}, status=status.HTTP_204_NO_CONTENT)