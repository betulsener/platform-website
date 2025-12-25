from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.utils.text import slugify
from taggit.managers import TaggableManager
from django.utils.html import mark_safe
from django.contrib.auth.models import User



class About(models.Model):
    title=models.CharField(max_length=200, verbose_name="Başlık")
    content=RichTextField(verbose_name="İçerik")
    image=models.ImageField(upload_to='about', verbose_name="Görsel")
    image2=models.ImageField(upload_to='about', verbose_name="Görsel2")


class Slider(models.Model):
    title=models.CharField(max_length=200, verbose_name="Başlık")
    image=models.ImageField(upload_to='slider', verbose_name="Görsel")


    
class Input(models.Model):
    title = models.CharField(max_length=200, verbose_name="Başlık")
    full_name = models.CharField(max_length=100, verbose_name="Ad Soyad")
    job = models.CharField(max_length=100, verbose_name="Meslek")
    email = models.EmailField()
    message = models.TextField(verbose_name="İleti")
    views = models.IntegerField(default=0, verbose_name="Görüntülenme Sayısı")
    slug = models.SlugField(max_length=200, unique=True, blank=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    tags=TaggableManager()
    keywords = models.CharField(max_length=200, verbose_name="Anahtar Kelimeler", blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.title)
        super(Input, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class Analysis(models.Model):
    wordcloud=models.ImageField(upload_to='analysis', verbose_name='Kelime Bulutu')
    keywords=models.CharField(max_length=255, verbose_name="Anahtar Kelimeler")
    def wordcloud_image(self, obj):
        if obj.wordcloud:
            return mark_safe(f'<img src="{obj.wordcloud.url}" width="100" height="100" />')
        return 'No Image'

    wordcloud_image.short_description = 'Wordcloud'
    wordcloud_image.allow_tags = True


class Setting(models.Model):
    logo_1 = models.ImageField(upload_to='dimg', null=True, blank=True)
    logo_2 = models.ImageField(upload_to='dimg', null=True, blank=True)
    title = models.CharField(max_length=255, verbose_name="Başlık")
    description = models.CharField(max_length=255, verbose_name="Açıklama")
    keywords = models.CharField(max_length=255, verbose_name="Anahtar kelimeler")
    phone = models.CharField(max_length=15, verbose_name="Telefon numarası")
    address=models.TextField(verbose_name="Adres")
    mail = models.EmailField(verbose_name="Mail adresi")
    other_url=models.URLField(max_length=255, verbose_name="Resmi web sitesi")

class Page(models.Model):
    title = models.CharField(max_length=200, verbose_name="Başlık")
    content = RichTextField(verbose_name="İçerik")
    slug = models.SlugField(max_length=200, blank=True, editable=False)

    def get_absolute_url(self):
        return reverse('page-detail', kwargs={'slug':self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.title)
        super(Page, self).save(*args, **kwargs)

class Scenario(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    pdf = models.FileField(upload_to='scenarios/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



