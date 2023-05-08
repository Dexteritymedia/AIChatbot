from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model()
 
class ChatBotSession(models.Model):
	text = models.TextField()
	date = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username
	
class ChatBot(models.Model):
    chat_session = models.ForeignKey(ChatBotSession, on_delete=models.CASCADE)
    message = models.TextField()
    bot_response = models.TextField()
    feedback = models.BooleanField()
    date = models.DateTimeField()
    
    def __str__(self):
        return self.chat_session.user.username
