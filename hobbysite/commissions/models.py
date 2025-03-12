from django.db import models

class Commission(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    peopleRequired = models.PositiveIntegerField()
    createdOn = models.DateTimeField(auto_now_add=True)
    updatedOn = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['createdOn']

class Comment(models.Model):
    commission = models.ForeignKey(Commission, on_delete=models.CASCADE, related_name='comments')
    entry = models.TextField()
    createdOn = models.DateTimeField(auto_now_add=True)
    updatedOn = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.commission.title} comment - {self.createdOn.strftime('%d-%m-%y')}"
    
    class Meta:
        ordering = ['-createdOn']



