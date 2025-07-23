from django.db import models


class Review(models.Model):
    full_name = models.CharField("ФИО", max_length=100)
    city = models.CharField("Город", max_length=50)
    slogan = models.CharField("Слоган", max_length=100)
    text = models.TextField("Основной текст отзыва")
    photo = models.ImageField("Фотография", upload_to="reviews/")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.city})"
