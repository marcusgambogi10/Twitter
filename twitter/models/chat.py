from django.db import models
from twitter.models import User

class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    user1 = models.ForeignKey(User, related_name='conversations_as_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='conversations_as_user2', on_delete=models.CASCADE)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    message = models.CharField(max_length=100000)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']