from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from twitter.models import Message, User
from twitter.serializers import MessageSerializer
from django.db.models import Q

class ChatMessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        return Message.objects.all()
    
    def user_messages(self, request, user_id=None):
        # Obtem todas as mensagens em que o usuário é o remetente ou o destinatário
        messages = Message.objects.filter(Q(sender=user_id) | Q(receiver=user_id))

        conversations = {}

        # Agrupa as mensagens por par único de usuários
        for message in messages:
            # Determine a ordem dos usuários na conversa
            user1_id = min(message.sender.id, message.receiver.id)
            user2_id = max(message.sender.id, message.receiver.id)
            
            if user1_id == user_id:
                user1 = User.objects.get(id=user1_id)
                user2 = User.objects.get(id=user2_id)
            else:
                user1 = User.objects.get(id=user2_id)
                user2 = User.objects.get(id=user1_id)
            
            # Cria a chave da conversa
            conversation_key = (user1_id, user2_id)

            # Verifique se a conversa já existe no dicionário, se não, cria
            if conversation_key not in conversations:
                conversations[conversation_key] = {
                    'user1': user1.id,
                    'user2': {
                        'id': user2.id,
                        'name': user2.name
                    },
                    'messages': []
                }

            # Adiciona a mensagem à lista de mensagens da conversa
            conversations[conversation_key]['messages'].append({
                'sender': message.sender.id,
                'receiver': message.receiver.id,
                'message': message.message,
                'timestamp': message.timestamp
            })

        # Converta o dicionário em uma lista de conversas
        conversation_list = [{'user1': conv['user1'], 'user2': conv['user2'], 'messages': conv['messages']} for conv in conversations.values()]

        return Response(conversation_list)
    
    def send_message(self, request, user_id=None, receiver_id=None):
        sender_id = user_id
        receiver_id = receiver_id

        data = {
            'sender': sender_id,
            'receiver': receiver_id,
            'message': request.data.get('message')
        }

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Se houver erros de validação, retorne-os
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)