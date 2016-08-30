from django.contrib.auth.models import User
from forum.models import Topic, Thread, Post, Follow, User
from rest_framework import serializers


class TopicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Topic
        fields = ('name', 'date')


class ThreadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Thread
        fields = ('topic', 'title', 'date')


class PostSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Post
        fields = ('thread', 'content', 'date', 'user')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class FollowSerializer(serializers.ModelSerializer):
    source = serializers.CharField(source='user.pk', read_only=True)

    class Meta:
        model = Follow
        fields = ('source', 'target', 'created_at')
