from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

    instance.profile.save()


# class Decks_Names(models.Model):
#     name = models.CharField("Класс колоды", max_length=100)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = "Класс колод"
#         verbose_name_plural = "Классы колод"


class Player(models.Model):
    name = models.CharField("Имя игрока", max_length=100, db_index=True)
    player_nickname = models.CharField("Никнейми игрока", max_length=100)
    rank = models.CharField("Ранк игрока", max_length=100)
    prizes = models.TextField("Награды")

    def __str__(self):
        return self.player_nickname

    class Meta:
        verbose_name = "Игрок"
        verbose_name_plural = "Игроки"


class Arthetype(models.Model):
    name = models.CharField("Архетип", max_length=100)
    winrate = models.SmallIntegerField("Процент побед")
    best_matchup = models.CharField("Лучший противник", max_length=100)
    worst_matchup = models.CharField("Худший противник", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Архетип"
        verbose_name_plural = "Архетипы"


class Deck_Review(models.Model):
    name = models.CharField("Описание колоды", max_length=100)  # код колоды
    rating = models.SmallIntegerField("Оценка")
    comment = models.TextField("Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Опсание колоды"
        verbose_name_plural = "Описания колод"


class Deck(models.Model):
    name = models.CharField("Колода", max_length=100, db_index=True)
    deck_tier = models.CharField("Тир колоды", max_length=100, default='D')
    archetype = models.ForeignKey(Arthetype, verbose_name="Архетип", on_delete=models.CASCADE)
    url = models.CharField("Ссылка на видео", max_length=100)
    player = models.ForeignKey(Player, verbose_name="Игрок", on_delete=models.CASCADE)
    image = models.ImageField("Изображение", upload_to="deck/")
    review = models.ForeignKey(Deck_Review, verbose_name="Опсание колоды", on_delete=models.CASCADE, default="Пусто")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Колода"
        verbose_name_plural = "Колоды"


class Deck_Picture(models.Model):
    image = models.ImageField("Скриншот колоды", upload_to="deck_picture/")
    name = models.CharField("Название", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Изображение класса"
        verbose_name_plural = "Изображения классов"
