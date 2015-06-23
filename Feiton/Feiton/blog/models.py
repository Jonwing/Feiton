from django.db import models


class Artilces(models.Model):
    caption = models.CharField(max_length=30)
    subcaption = models.CharField(max_length=30)
    publish_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author)
    catagory = models.ForeignKey(Catagory)
    tags = models.ForeignKey(Tag, blank=True)
    content = RichTextField()
    abstract = RichTextField(blank=True)


class Author(models.Model):
    pass


class Tag(models.Model):
    pass


class Catagory(models.Model):
    pass
