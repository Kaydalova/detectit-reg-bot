from django.db import models


class Game(models.Model):
    name = models.CharField(
        verbose_name='Название игры',
        max_length=200)
    number = models.PositiveSmallIntegerField(
        verbose_name='Номер игры')
    date = models.DateTimeField(
        verbose_name='Дата проведения')
    place = models.CharField(
        verbose_name='Место',
        max_length=200)

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(
        verbose_name='Название команды',
        max_length=200)
    captain = models.CharField(
        verbose_name='Капитан',
        max_length=20)
    phone = models.CharField(
        verbose_name='Контактный телефон',
        max_length=200)
    members = models.PositiveSmallIntegerField(
        verbose_name='Участники')
    game = models.ForeignKey(
        Game,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Игра')

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

    def __str__(self):
        return self.name


class Confirmation(models.Model):
    text = models.TextField(
        verbose_name='Сообщение')

    class Meta:
        verbose_name = 'Подтверждение'
        verbose_name_plural = 'Подтверждения'
