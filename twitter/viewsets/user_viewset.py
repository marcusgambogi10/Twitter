from rest_framework import viewsets, status
from twitter.models import User
from twitter.serializers import UserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None, target_pk=None):
        # Obtenha o usuário logado
        user = User.objects.filter(pk=pk).first()
        
        # Obtenha o usuário alvo que será seguido
        target_user = User.objects.filter(pk=target_pk).first()
        
        # Verifique se o usuário alvo existe
        if target_user is None:
            return Response({"Error": "Usuário alvo não encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        # Verifique se o usuário já está seguindo o usuário-alvo
        if user.follows.filter(pk=target_user.pk).exists():
            return Response({"Error": "Você já está seguindo este usuário"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Adicione o usuário alvo aos seguidos pelo usuário que está seguindo
        user.follows.add(target_user)

        # Adicione o usuário que está seguindo aos seguidores do usuário alvo
        target_user.followers.add(user)
        
        # Serialize os dados completos dos usuários
        user_serializer = UserSerializer(user)
        target_user_serializer = UserSerializer(target_user)

        # Retorne os dados dos usuários seguindo o padrão especificado no serializer
        return Response({
            "Message": f"Você seguiu com sucesso o usuário: {target_user.name}",
            "Follower": user_serializer.data,
            "Following": target_user_serializer.data
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None, target_pk=None):
        # Obtenha o usuário logado
        user = User.objects.filter(pk=pk).first()

        # Obtenha o usuário alvo que será deixado de seguir
        target_user = User.objects.filter(pk=target_pk).first()

        if target_user is None:
            return Response({"error": "Usuário alvo não encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # Remova o usuário alvo dos seguidos pelo usuário que está deixando de seguir
        user.follows.remove(target_user)

        # Remova o usuário que está deixando de seguir dos seguidores do usuário alvo
        target_user.followers.remove(user)

        # Serialize os dados completos dos usuários
        user_serializer = UserSerializer(user)
        target_user_serializer = UserSerializer(target_user)

        # Retorne os dados dos usuários seguindo o padrão especificado no serializer
        return Response({
            "Message": f"Você deixou de seguir com sucesso o usuário: {target_user.name}",
            "Follower": user_serializer.data,
            "Following": target_user_serializer.data
        }, status=status.HTTP_200_OK)