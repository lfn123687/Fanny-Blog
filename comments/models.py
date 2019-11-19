from django.db import models
from django.utils import timezone

class Comment(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    url = models.URLField(blank=True)
    text = models.TextField()
    created_time = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE)

    def __str__(self):
        return '{}: {}'.format(self.name, self.text[:20])

    class Meta:
        ordering = ['-created_time']

