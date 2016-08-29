from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from forum.serializers import TopicSerializer, ThreadSerializer, PostSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny,DjangoModelPermissionsOrAnonReadOnly
from .models import Topic, Thread, Post

def index(request):
    latest_topics = Topic.objects.order_by('-name')
    context = {
        'latest_topics': latest_topics,
    }
    return render(request, 'forum/index.html', {'latest_topics': latest_topics})

# def topic(request, id):
    # topic = get_object_or_404(Topic, pk=id)
    # return render(request, 'forum/topic.html', {'topic': topic})

class TopicViewSet(viewsets.ModelViewSet):
    """
    REST API endpoint for viewing/editing Topics.
    """
    queryset = Topic.objects.all().order_by('-name')
    serializer_class = TopicSerializer

    def retrieve(self, request, pk=None):
        topic = get_object_or_404(Topic, pk=pk)
        latest_threads = topic.thread_set.order_by('-date')
#        import pdb; pdb.set_trace()
        return render(request, 'forum/topic.html', {'topic' : topic, 'latest_threads' : latest_threads})

#     def list(self, request):
#         return index(request)

#     def create(self, request):
#         viewsets.ModelViewSet.create(self, request)
#         return index(request)

class ThreadViewSet(viewsets.ModelViewSet):
    """
    REST API endpoint for viewing/editing Threads.
    """
    queryset = Thread.objects.all().order_by('-date')
    serializer_class = ThreadSerializer
        
    def create(self, request):
        viewsets.ModelViewSet.create(self, request)
        return redirect(request.data['topic'])

# class ThreadViewSet(viewsets.ModelViewSet):
#     """
#     REST API endpoint for viewing/editing Threads.
#     """
#     queryset = Post.objects.all().order_by('-date')
#     serializer_class = PostSerializer

#     # def list(self, request):
        
