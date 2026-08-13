from django.db import models

# Create your models here.
class Register(models.Model):
    choices=(
    ("admin","Admin"),
    ("user","User"),
    )
    username=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=100)
    phone_no=models.BigIntegerField()
    role=models.CharField(max_length=100,choices=choices,default="user")
    class Meta:
        db_table='register'

class Category(models.Model):
    category_name = models.CharField(max_length=100)

    class Meta:
        db_table = "category"

    def __str__(self):
        return self.category_name


class ShortFilm(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    youtube_link = models.URLField()
    thumbnail = models.ImageField(upload_to="thumbnails/", blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "shortfilm"

class WatchLater(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    shortfilm = models.ForeignKey(ShortFilm, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "watch_later"
        unique_together = ("user", "shortfilm")
