from rest_framework import serializers
from forum.models import Topic, Thread, Post, Follow

class TopicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Topic
        fields = ('name', 'date')

# TODO(avesh): Add Thread, Post, and Follow to API
