from django.shortcuts import get_object_or_404, render
from forum.serializers import TopicSerializer
from rest_framework import viewsets
from .models import Topic

def index(request):
    latest_topics = Topic.objects.order_by('-name')
    context = {
        'latest_topics': latest_topics,
    }
    return render(request, 'forum/index.html', {'latest_topics': latest_topics})

def topic(request, id):
    topic = get_object_or_404(Topic, pk=id)
    return render(request, 'forum/topic.html', {'topic': topic})

class TopicViewSet(viewsets.ModelViewSet):
    """
    REST API endpoint for viewing/editing Topics.
    """
    queryset = Topic.objects.all().order_by('-name')
    serializer_class = TopicSerializer
