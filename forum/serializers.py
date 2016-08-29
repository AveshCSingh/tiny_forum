from rest_framework import serializers
from forum.models import Topic, Thread, Post, Follow

class TopicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Topic
        fields = ('name', 'date')

class ThreadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Thread
        fields = ('topic', 'title', 'date')

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Topic
        fields = ('thread', 'content', 'user')
