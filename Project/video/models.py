from django.db import models
from django.urls import reverse


class Video(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    url = models.URLField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('auth.User', related_name='videos', on_delete=models.CASCADE)
    file = models.FileField(upload_to='videos/%Y/%m/%d', blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('video:video_detail', args=[self.id])

    def get_update_url(self):
        return reverse('video:video_update', args=[self.id])

    def get_delete_url(self):
        return reverse('video:video_delete', args=[self.id])

    # delete video file from dir when video is deleted
    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)

    # get video file name
    def get_file_name(self):
        return self.file.name.split('/')[-1]

