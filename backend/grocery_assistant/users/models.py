from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.expressions import Exists, OuterRef
from django.db.models import BooleanField, Value
from django.contrib.auth.models import UserManager


class CustomUserQuerySet(models.QuerySet):
    def annotate_flags(self, user):
        if user.is_anonymous:
            return User.objects.annotate(
                is_subscribed=Value(False, output_field=BooleanField())
            )

        is_subscribed = Follow.objects.filter(
            author=OuterRef('pk'),
            user=user
        )
        return self.annotate(
            is_subscribed=Exists(is_subscribed),
        )


class CustomUserManager(UserManager):
    def get_queryset(self):
        return CustomUserQuerySet(self.model, using=self._db)

    def annotate_flags(self, user):
        return self.get_queryset().annotate_flags(user)


class User(AbstractUser):
    email = models.EmailField('Email', unique=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                name='user != author',
                check=~models.Q(user=models.F('author')),
            ),
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_follow'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('author',)
