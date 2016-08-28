from django.shortcuts import render
from forum.models import Topic
from forum.serializers import TopicSerializer
from rest_framework import viewsets
from django.http import HttpResponse
from .models import Topic

def index(request):
    latest_topics = Topic.objects.order_by('-date')[:10]
    output = ', '.join([t.name for t in latest_topics])
    return HttpResponse(output)

class TopicViewSet(viewsets.ModelViewSet):
    """
    REST API endpoint for viewing/editing Topics.
    """
    queryset = Topic.objects.all().order_by('date')
    serializer_class = TopicSerializer
