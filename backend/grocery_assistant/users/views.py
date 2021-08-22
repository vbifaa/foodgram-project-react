from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from grocery_assistant.actions import create_or_delete_obj_use_func

from .models import Follow
from .pagination import UsersPagination
from .serializers import FollowingUsersSerializer

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
        following = self.get_queryset().filter(following__user=request.user)

        page = self.paginate_queryset(following)
        serializer = FollowingUsersSerializer(
                page or following, context={'request': request}, many=True
            )
        if page is not None:
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

    @action(['get', 'delete'], detail=True)
    def subscribe(self, request, *args, **kwargs):
        serializer = FollowingUsersSerializer(
            data=self.kwargs['id'], context={'request': request}
        )
        author = get_object_or_404(User, id=self.kwargs['id'])

        if request.method == 'DELETE':
            return create_or_delete_obj_use_func(
                is_delete=True,
                serializer=serializer,
                func=author.following.filter(
                    user=self.request.user
                ).delete,
                args={},
                msg_error='Не получилось отписаться от пользователя.'
            )
        return create_or_delete_obj_use_func(
            is_delete=False,
            serializer=serializer,
            func=Follow.objects.create,
            args={'author': author, 'user': self.request.user},
            msg_error='Не получилось подписаться на пользователя.'
        )
