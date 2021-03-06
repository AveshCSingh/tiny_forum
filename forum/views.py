from .models import Topic, Thread, Post, Follow
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.dates import DayArchiveView
from forum.serializers import TopicSerializer, ThreadSerializer, PostSerializer, UserSerializer, FollowSerializer
from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, DjangoModelPermissionsOrAnonReadOnly


def index(request):
    """
    Renders the homepage.
    """
    topics = Topic.objects.order_by('-name')
    context = {'topics': topics, }
    return render(request, 'forum/index.html',
                  {'topics': topics})


class BaseRedirectListViewSet(viewsets.ModelViewSet):
    """
    A base class that redirects list and create calls to the homepage.
    """

    def list(self, request):
        return redirect('/')

    def create(self, request):
        viewsets.ModelViewSet.create(self, request)
        return redirect('/')


class TopicViewSet(BaseRedirectListViewSet):
    """
    REST API endpoint for viewing/editing Topics.
    Inherits from BaseRedirectViewSet as topics are listed on the homepage.
    """
    queryset = Topic.objects.all().order_by('-name')
    serializer_class = TopicSerializer

    def retrieve(self, request, pk=None):
        topic = get_object_or_404(Topic, pk=pk)
        latest_threads = topic.thread_set.order_by('-date')[:10]
        return render(request, 'forum/topic.html',
                      {'topic': topic,
                       'latest_threads': latest_threads})


class ThreadViewSet(viewsets.ModelViewSet):
    """
    REST API endpoint for viewing/editing Threads.
    """
    queryset = Thread.objects.all().order_by('-date').reverse()
    serializer_class = ThreadSerializer

    def create(self, request):
        viewsets.ModelViewSet.create(self, request)
        return redirect(request.data['topic'])

    def retrieve(self, request, pk=None):
        thread = get_object_or_404(Thread, pk=pk)
        posts = thread.post_set.order_by('-date').reverse()
        return render(request, 'forum/thread.html', {'thread': thread,
                                                     'posts': posts})


class PostViewSet(BaseRedirectListViewSet):
    """
    REST API endpoint for viewing/editing Threads.
    Inherits from BaseRedirectViewSet as listing all posts regardless of thread should not be possible.
    """
    queryset = Post.objects.all().order_by('-date')
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request):
        viewsets.ModelViewSet.create(self, request)
        return redirect(request.data['thread'])


class FollowViewSet(BaseRedirectListViewSet):
    """
    REST API endpoint for viewing/editing Follows.
    """
    queryset = Follow.objects.all().order_by('-created_at')
    serializer_class = FollowSerializer

    def perform_create(self, serializer):
        serializer.save(source=self.request.user)


class UserList(generics.ListAPIView):
    """
    Provides GET handler for listing Users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    """
    Proves GET handler for single-user details
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        return render(request, 'forum/user.html', {'user': user})


def summary(request, year, month, day):
    """
    Provides summary information on the forum on a particularly day:
      -Total of posts
      -Number of posts per user
    """
    posts = Post.objects.filter(
        Q(date__year=year) & Q(date__month=month) & Q(date__day=day))

    user_post_count = {}
    for p in posts:
        user_post_count[p.user] = user_post_count.get(p.user, 0) + 1

    sorted_user_post_counts = []
    for user, count in user_post_count.items():
        sorted_user_post_counts.append((count, user.username))
    sorted_user_post_counts.sort()

    return render(request, 'forum/summary.html',
                  {'user_post_counts': sorted_user_post_counts[:5],
                   'num_posts': len(posts)})
