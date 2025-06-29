from django.db import models

# Create your models here.

class todos(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank =True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"

class Comment(models.Model):
    todo = models.ForeignKey(todos, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment on "{self.todo.title}"'