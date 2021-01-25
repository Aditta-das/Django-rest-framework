from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


# In the same way that Django provides both Form classes and ModelForm classes, REST framework includes both Serializer classes, and ModelSerializer classes.


# class SnippetSerializer(serializers.Serializer):
# 	id = serializers.IntegerField(read_only=True)
# 	title = serializers.CharField(required=False, allow_blank=True, max_length=100)
# 	code = serializers.CharField(style={'base_template': 'textarea.html'})
# 	linenos = serializers.BooleanField(required=False)
# 	language = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

# 	def create(self, validate_data):
# 		return Snippet.objects.create(**validate_data)

# 	def update(self, instance, validate_data):
# 		instance.title = validate_data.get('title', instance.title)
# 		instance.code = validate_data.get('code', instance.code)
# 		instance.linenos = validate_data.get('linenos', instance.linenos)
# 		instance.language = validate_data.get('language', instance.language)
# 		instance.style = validate_data.get('style', instance.style)
# 		instance.save()
# 		return instance	

###################################### ModelSerializer ############################################
class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ['url', 'id', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style']


# It's important to remember that ModelSerializer classes don't do anything particularly magical, they are simply a shortcut for creating serializer classes:

	#     An automatically determined set of fields.
	#     Simple default implementations for the create() and update() methods.


# Adding endpoints for our User models

# Now that we've got some users to work with, we'd better add representations of those users to our API. Creating a new serializer is easy. In serializers.py add:

from django.contrib.auth.models import User
from rest_framework import generics


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'snippets']

# Because 'snippets' is a reverse relationship on the User model, it will not be included by default when using the ModelSerializer class, so we needed to add an explicit field for it.

# We'll also add a couple of views to views.py. We'd like to just use read-only views for the user representations, so we'll use the ListAPIView and RetrieveAPIView generic class-based views.