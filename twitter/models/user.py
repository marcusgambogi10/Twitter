from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=20)
    email = models.EmailField()
    password = models.CharField(max_length=40)
    follows = models.ManyToManyField('self', symmetrical=False, related_name='following_set', blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='followers_set', blank=True)
    
    def __str__(self) -> str:
        return self.name
    
    def get_tweets(self):
        from twitter.models.tweet import Tweet  # Importação local
        return Tweet.objects.filter(author=self)