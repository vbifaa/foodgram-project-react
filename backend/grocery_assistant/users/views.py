from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

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
        serializer = FollowingUsersSerializer(
            following, context={'request': request}, many=True
        )
        return Response(serializer.data)

    @action(['get', 'delete'], detail=True)
    def subscribe(self, request, *args, **kwargs):
        cur_user = get_object_or_404(User, email=self.request.user)
        author = get_object_or_404(User, id=self.kwargs['id'])
        follow = author.following.filter(user=cur_user)

        if request.method == 'DELETE':
            return self.delete_follow(
                author=author, user=cur_user, follow=follow
            )
        return self.create_follow(
            author=author, user=cur_user, follow=follow, request=request
        )

    def create_follow(self, author, user, follow, request):
        if author == user or follow.exists():
            return self.bad_400_status_to_follow(
                author_equals_user=(author == user),
                error_author_eq_user='Нельзя подписываться на самого себя.',
                error_otherwise='Вы уже подписаны на этого пользователя.'
            )

        Follow.objects.create(author=author, user=user)
        serializer = FollowingUsersSerializer(
            author, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_follow(self, author, user, follow):
        if author == user or not follow.exists():
            return self.bad_400_status_to_follow(
                author_equals_user=(author == user),
                error_author_eq_user='Нельзя отписываться от самого себя.',
                error_otherwise='Вы не подписаны на этого пользователя.'
            )

        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def bad_400_status_to_follow(
        self, author_equals_user, error_author_eq_user, error_otherwise
    ):
        if author_equals_user:
            error_msg = error_author_eq_user
        else:
            error_msg = error_otherwise

        return Response(
                {'errors': error_msg},
                status=status.HTTP_400_BAD_REQUEST
            )
