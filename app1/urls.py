from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import home, analyze_sentiment, analyze_image

app_name = "app1"
urlpatterns = [
    path('', home, name='home'),
    path('analyze/', analyze_sentiment, name='analyze_sentiment'),
    path('analyze-image/', analyze_image, name='analyze_image'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

