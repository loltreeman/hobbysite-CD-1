from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.display_name
class Commission(models.Model):
    status_options = [
        ('0', 'Open'),
        ('1', 'Full'),
        ('2', 'Completed'),
        ('3', 'Discontinued')
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=status_options, default = '0')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['status', 'created_on']
        verbose_name = 'Commission'
        verbose_name_plural = 'Commissions'
        

class Job(models.Model):
    job_options = [
        ('0', 'Open'),
        ('1', 'Full'),
    ]
    status = models.CharField(max_length=10, choices=job_options, default = '0')
    commission = models.ForeignKey(Commission, on_delete=models.CASCADE)
    role = models.CharField(max_length=255)
    manpower_required = models.PositiveIntegerField()
    
    class Meta:
        ordering = ['status', '-manpower_required', 'role']
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
    
class JobApplication(models.Model):
    application_options = [
        ('0', 'Pending'),
        ('1', 'Accepted'),
        ('2', 'Rejected'),

    ]
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=application_options, default = '0')
    applied_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['status', '-applied_on']
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'



