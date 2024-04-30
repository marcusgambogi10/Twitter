from django.db import models
from twitter.models.user import User

class Tweet(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default='')
    text = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Tweet {self.id} by {self.author.name}"
    
    def save(self, *args, **kwargs):
        self.name = self.author.name
        super(Tweet, self).save(*args, **kwargs)