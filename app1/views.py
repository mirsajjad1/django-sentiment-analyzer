from django.shortcuts import render, redirect
from textblob import TextBlob
from .forms import SentimentForm, ImageAnalysisForm
from .models import SentimentEntry, ImageAnalysis
import imagehash
from PIL import Image
import os


def home(request):
    return render(request, 'app1/home.html')


def analyze_sentiment(request):
    entries = SentimentEntry.objects.all().order_by('-created_at')
    
    if request.method == 'POST':
        form = SentimentForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            # Analyze sentiment using TextBlob
            analysis = TextBlob(entry.text)
            # Get polarity and convert to sentiment label
            if analysis.sentiment.polarity > 0:
                entry.sentiment = 'positive'
            elif analysis.sentiment.polarity < 0:
                entry.sentiment = 'negative'
            else:
                entry.sentiment = 'neutral'
            entry.save()
            return redirect('app1:analyze_sentiment')
    else:
        form = SentimentForm()
    
    return render(request, 'app1/analyze_sentiment.html', {
        'form': form,
        'entries': entries
    })

def analyze_image(request):
    entries = ImageAnalysis.objects.all().order_by('-created_at')
    
    if request.method == 'POST':
        form = ImageAnalysisForm(request.POST, request.FILES)
        if form.is_valid():
            entry = form.save(commit=False)
            
            # Calculate image hash
            img = Image.open(entry.image)
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Calculate various image properties
            width, height = img.size
            aspect_ratio = width / height
            
            # Analyze basic image properties
            properties = []
            
            if aspect_ratio > 1.2:
                properties.append("Landscape")
            elif aspect_ratio < 0.8:
                properties.append("Portrait")
            else:
                properties.append("Square")
                
            if width > 2000 or height > 2000:
                properties.append("High Resolution")
            
            # Get color information
            colors = img.getcolors(img.size[0] * img.size[1])
            if colors:
                dominant_color = max(colors, key=lambda x: x[0])[1]
                r, g, b = dominant_color
                if r > max(g, b):
                    properties.append("Reddish")
                elif g > max(r, b):
                    properties.append("Greenish")
                elif b > max(r, g):
                    properties.append("Bluish")
            
            # Calculate a perceptual hash
            hash_value = str(imagehash.average_hash(img))
            
            entry.result = f"Image Properties: {', '.join(properties)}"
            entry.confidence = 100.0  # Since we're doing direct analysis
            entry.save()
            
            return redirect('app1:analyze_image')
    else:
        form = ImageAnalysisForm()
    
    return render(request, 'app1/analyze_image.html', {
        'form': form,
        'entries': entries
    })
