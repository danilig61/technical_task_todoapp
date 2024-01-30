from django.contrib.auth.models import User
from django.db import models


class Folder(models.Model):
    name = models.CharField(max_length=255)
    is_public = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Page(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    is_public = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_pages')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_pages')

    def __str__(self):
        return self.name


class Record(models.Model):
    STATUS_CHOICES = [
        ('Выполнено', 'Выполнено'),
        ('В процессе', 'В процессе'),
        ('Отменено', 'Отменено'),
    ]

    text = models.TextField()
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_records')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_records')
    previous_version = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class FolderPermission(models.Model):
    folder = models.ForeignKey('Folder', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    can_read = models.BooleanField(default=False)


class PagePermission(models.Model):
    page = models.ForeignKey('Page', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    can_read = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_create = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)


class RecordPermission(models.Model):
    record = models.ForeignKey('Record', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    can_read = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_create = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
