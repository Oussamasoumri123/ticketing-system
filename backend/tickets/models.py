from django.db import models
from django.conf import settings
import cloudinary.uploader

class Ticket(models.Model):
    CATEGORY_CHOICES = (
        ('technical', 'Technical'),
        ('financial', 'Financial'),
        ('product', 'Product'),
    )
    
    STATUS_CHOICES = (
        ('new', 'New'),
        ('under_review', 'Under Review'),
        ('resolved', 'Resolved'),
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )
    attachment = models.FileField(
        upload_to='tickets/',
        null=True,
        blank=True
    )
    attachment_url = models.URLField(
        max_length=500,
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tickets'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Upload vers Cloudinary si fichier présent
        if self.attachment and not self.attachment_url:
            try:
                upload_result = cloudinary.uploader.upload(
                    self.attachment,
                    folder="tickets"
                )
                self.attachment_url = upload_result['secure_url']
            except Exception as e:
                print(f"Erreur upload Cloudinary: {e}")
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title} - {self.status}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'


class StatusHistory(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='status_history'
    )
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    changed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.ticket.title}: {self.old_status} → {self.new_status}"
    
    class Meta:
        ordering = ['-changed_at']
        verbose_name = 'Historique de statut'
        verbose_name_plural = 'Historiques de statut'