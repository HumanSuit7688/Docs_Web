from django.db import models

class Order(models.Model):
    doc_type = models.PositiveSmallIntegerField()
    surname = models.CharField(max_length=50, blank=False)
    name = models.CharField(max_length=50, blank=False)
    patronymic = models.CharField(max_length=50)
    grade_c = models.PositiveSmallIntegerField(blank=False)
    grade_b = models.CharField(max_length=5, blank=False)
    email = models.EmailField()
    status = models.BooleanField(default=0)


# class File(models.Model):
#     title = models.CharField(max_length=150)
#     file = models.FileField(upload_to='')
#
#     def __str__(self):
#         return self.title
