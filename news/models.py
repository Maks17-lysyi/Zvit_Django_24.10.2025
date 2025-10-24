from django.db import models
from django.utils import timezone
from core.models import League


class Tag(models.Model):
	name = models.CharField(max_length=64, unique=True)

	def __str__(self) -> str:
		return self.name


class News(models.Model):
	title = models.CharField(max_length=200)
	slug = models.SlugField(max_length=220, unique=True)
	summary = models.TextField()
	body = models.TextField(blank=True)
	league = models.ForeignKey(League, on_delete=models.SET_NULL, null=True, blank=True)
	image_url = models.URLField(blank=True)
	created_at = models.DateTimeField(default=timezone.now)
	tags = models.ManyToManyField(Tag, blank=True)
	is_featured = models.BooleanField(default=False)

	class Meta:
		ordering = ['-created_at']

	def __str__(self) -> str:
		return self.title
