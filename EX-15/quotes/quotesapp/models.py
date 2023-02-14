from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Authors(models.Model):
    fullname = models.CharField(max_length=150, null=False, unique=True)
    born_date = models.DateTimeField()
    born_location = models.CharField(max_length=150)
    description = models.CharField(max_length=5000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'fullname'], name='author of username')
        ]

    def __str__(self):
        return f"{self.fullname} {self.born_date} {self.born_location}"

class Tags(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='tag of username')
        ]

    def __str__(self):
        return f"{self.name}"

class Quotes(models.Model):
    quote = models.CharField(max_length=5000, null=False)
    tags = models.ManyToManyField(Tags)
    author = models.ForeignKey(Authors, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.quote}"