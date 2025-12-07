from django.db import models

# Create your models here.
class SentimentEntry(models.Model):
    text = models.TextField()
    sentiment = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sentiment}: {self.text[:50]}"

class ImageAnalysis(models.Model):
    image = models.ImageField(upload_to='images/')
    result = models.TextField()
    confidence = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image Analysis: {self.result} ({self.confidence:.2f}%)"