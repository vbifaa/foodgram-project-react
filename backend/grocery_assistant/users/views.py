from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404

from .pagination import UsersPagination
from .serializers import FollowingUsersSerializer
from .models import Follow


User = get_user_model()


class CustomUserViewSet(UserViewSet):
    pagination_class = UsersPagination
    
    @action(['post'], detail=False)
    def set_password(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.request.user.set_password(serializer.data['new_password'])
        self.request.user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(['get'], detail=False)
    def subscriptions(self, request, *args, **kwargs):
        following = User.objects.filter(following__user=request.user)
        serializer = FollowingUsersSerializer(
            following, context={'request': request}, many=True
        )
        return Response(serializer.data)

    @action(['get', 'delete'], detail=True)
    def subscribe(self, request, *args, **kwargs):
        cur_user = get_object_or_404(User, email=self.request.user)
        author = get_object_or_404(User, id=self.kwargs['id'])
        follow = Follow.objects.filter(user=cur_user, author=author)

        create_wrong = self.request.method == 'GET' and follow.exists()
        delete_wrong = self.request.method == 'DELETE' and not follow.exists()
        
        if author == cur_user or create_wrong or delete_wrong:
            if author == cur_user:
                if self.request.method == 'GET':
                    error = 'Нельзя подписываться на самого себя.'
                else:
                    error = 'Нельзя отписываться от самого себя.'
            elif create_wrong:
                error = 'Вы уже подписаны на этого пользователя.'
            else:
                error = 'Вы не подписаны на этого пользователя.'
            return Response(
                {
                    'errors': error
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if self.request.method == 'GET':
            Follow.objects.create(author=author, user= cur_user)
            serializer = FollowingUsersSerializer(author, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
