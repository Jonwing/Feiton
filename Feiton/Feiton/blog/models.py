from django.db import models
from DjangoUeditor.models import UEditorField


class Author(models.Model):
    name = models.CharField(u"作者姓名", max_length=50)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    def __unicode__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(u"标签", max_length=30)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


class Catagory(models.Model):
    name = models.CharField(u"分类", max_length=50)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


class Artilces(models.Model):
    caption = models.CharField(u"标题", max_length=30)
    subcaption = models.CharField(u"副标题", max_length=30)
    publish_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author)
    catagory = models.ForeignKey(Catagory)
    tags = models.ManyToManyField(Tag)
    content = UEditorField(
        u"内容", width=600, height=300, toolbars="full",
        imagePath="images/", filePath="add_on_files/",
        upload_settings={"imageMaxSize": 1204000},
        command=None, blank=True
        )
    abstract = models.TextField(blank=True)

    def __unicode__(self):
        return self.caption


class Statistics(models.Model):
    article = models.OneToOneField(Artilces)
    visits = models.IntegerField()
    comments = models.IntegerField()
    likes = models.IntegerField()

    def __unicode__(self):
        return u"blog statistics"
