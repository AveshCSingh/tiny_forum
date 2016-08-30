from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from forum.serializers import TopicSerializer, ThreadSerializer, PostSerializer, UserSerializer
from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny,DjangoModelPermissionsOrAnonReadOnly
from .models import Topic, Thread, Post
from django.contrib.auth.models import User


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
        latest_threads = topic.thread_set.order_by('-date')[:10]
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

    def retrieve(self, request, pk=None):
        thread = get_object_or_404(Thread, pk=pk)
        posts = thread.post_set.order_by('-date')
        return render(request, 'forum/thread.html', {'thread' : thread, 'posts' : posts})

class PostViewSet(viewsets.ModelViewSet):
    """
    REST API endpoint for viewing/editing Threads.
    """
    queryset = Post.objects.all().order_by('-date')
    serializer_class = PostSerializer

    def perform_create(self, serializer):
#        import pdb; pdb.set_trace()
        serializer.save(user=self.request.user)


#     # def list(self, request):


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
        

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

