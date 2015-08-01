from django.db import models

class Person(models.Model):

    uid = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Part(models.Model):

    uid = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    part = models.CharField(max_length=100)

    @classmethod
    def create(cls, person, part):
        kwargs = {}
        kwargs['uid'] = person.uid
        kwargs['name'] = person.name
        kwargs['email'] = person.email
        kwargs['part'] = part
        return cls(**kwargs)
