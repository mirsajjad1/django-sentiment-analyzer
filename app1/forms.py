from django import forms
from .models import SentimentEntry, ImageAnalysis

class SentimentForm(forms.ModelForm):
    class Meta:
        model = SentimentEntry
        fields = ['text']  # Only include the text field

class ImageAnalysisForm(forms.ModelForm):
    class Meta:
        model = ImageAnalysis
        fields = ['image']
