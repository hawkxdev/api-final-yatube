"""Модели постов."""

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    """Группа постов."""

    title = models.CharField('Название', max_length=200)
    slug = models.SlugField('Слаг', max_length=50, unique=True)
    description = models.TextField('Описание')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        """Название группы."""
        return self.title


class Post(models.Model):
    """Пост пользователя."""

    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL, related_name='posts',
        blank=True, null=True, verbose_name='Группа')

    def __str__(self):
        """Текст поста."""
        return self.text


class Comment(models.Model):
    """Комментарий поста."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        """Комментарий автора."""
        return f'Комментарий {self.author} к посту {self.post.id}'


class Follow(models.Model):
    """Подписка пользователя."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower',
        verbose_name='Подписчик')
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following',
        verbose_name='Подписка')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_user_following'
            )
        ]

    def __str__(self):
        """Подписка пользователя."""
        return f'{self.user} подписан на {self.following}'
