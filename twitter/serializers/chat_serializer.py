from twitter.models import Conversation, Message
from rest_framework import serializers

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'message', 'timestamp']
    
    def create(self, validated_data):
        # Obtenha o remetente e o destinatário da mensagem
        sender = validated_data.get('sender')
        receiver = validated_data.get('receiver')
        
        # Verifique se já existe uma conversa entre o remetente e o destinatário
        conversation = Conversation.objects.filter(user1=sender, user2=receiver).first()
        
        # Se a conversa não existir, crie uma nova
        if not conversation:
            conversation = Conversation.objects.create(user1=sender, user2=receiver)
        
        # Adicione a conversa aos dados validados
        validated_data['conversation'] = conversation
        
        # Crie a mensagem associada à conversa
        return super().create(validated_data)

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'user1', 'user2', 'messages']