from django.shortcuts import render
from forum.models import Topic
from forum.serializers import TopicSerializer
from rest_framework import viewsets

class TopicViewSet(viewsets.ModelViewSet):
    """
    REST API endpoint for viewing/editing Topics.
    """
    queryset = Topic.objects.all().order_by('date')
    serializer_class = TopicSerializer
