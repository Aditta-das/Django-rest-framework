from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.http import Http404
#	Writing regular Django views using our Serializer

#	Let's see how we can write some API views using our new Serializer class. For the moment we won't use any of REST framework's other features, we'll just write the views as regular Django views.


#	Note that because we want to be able to POST to this view from clients that won't have a CSRF token we need to mark the view as csrf_exempt. This isn't something that you'd normally want to do, and REST framework views actually use more sensible behavior than this, but it'll do for our purposes right now.


#	Adding optional format suffixes to our URLs

#	To take advantage of the fact that our responses are no longer hardwired to a single content type let's add support for format suffixes to our API endpoints. Using format suffixes gives us URLs that explicitly refer to a given format, and means our API will be able to handle URLs such as http://example.com/api/items/4.json.

#################################### FUNCTION BASED ###########################################
# @csrf_exempt
# @api_view(['GET', 'POST'])
# def snippet_list(request, format=None):
# 	if request.method == "GET":
# 		snippets = Snippet.objects.all()
# 		serializer = SnippetSerializer(snippets, many=True)
# 		return JsonResponse(serializer.data, safe=False)

# 	elif request.method == "POST":
# 		data = JSONParser().parse(request)
# 		serializer = SnippetSerializer(data=request.data)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
# 		return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # @csrf_exempt
# @api_view(['GET', 'PUT', 'DELETE'])
# def snippet_detail(request, pk, format=None):
# 	try:
# 		snippet = Snippet.objects.get(pk=pk)

# 	except Exception as e:
# 		return HttpResponse(status=status.HTTP_404_NOT_FOUND)

# 	if request.method == "GET":
# 		serializer = SnippetSerializer(snippet)
# 		return JsonResponse(serializer.data)

# 	elif request.method == "PUT":
# 		data = JSONParser().parse(request)
# 		serializer = SnippetSerializer(snippet, data=request.data)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return JsonResponse(serializer.data)
# 		return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
# 	elif request.method == "DELETE":
# 		snippet.delete()
# 		return HttpResponse(status=status.HTTP_204_NO_CONTENT)


################################# CLASS BASED ############################################

# class SnippetList(APIView):
# 	def get(self, request, format=None):
# 		snippets = Snippet.objects.all()
# 		serializer = SnippetSerializer(snippets, many=True)
# 		return Response(serializer.data)

# 	def post(self, request, format=None):
# 		serializer = SnippetSerializer(data=request.data)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response(serializer.data, status=status.HTTP_201_CREATED)
# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class SnippetDetail(APIView):
# 	def get_objects(self, pk):
# 		try:
# 			return Snippet.objects.get(pk=pk)
# 		except Snippet.DoesNotExist:
# 			return Http404

# 	def get(self, request, pk, format=None):
# 		snippet = self.get_objects(pk)
# 		serializer = SnippetSerializer(snippet)
# 		return Response(serializer.data)

# 	def put(self, request, pk, format=None):
# 		snippet = self.get_objects(pk)
# 		serializer = SnippetSerializer(snippet, data=request.data)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response(serializer.data)
# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 	def delete(self, request, pk, format=None):
# 		snippet = self.get_objects(pk)
# 		snippet.delete()
# 		return Response(status=status.HTTP_204_NO_CONTENT)



# Using mixins

## One of the big wins of using class-based views is that it allows us to easily compose reusable bits of behaviour.

## The create/retrieve/update/delete operations that we've been using so far are going to be pretty similar for any model-backed API views we create. Those bits of common behaviour are implemented in REST framework's mixin classes.

# Let's take a look at how we can compose the views by using the mixin classes. Here's our views.py module again.

# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
# from rest_framework import mixins
# from rest_framework import generics

# class SnippetList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# We'll take a moment to examine exactly what's happening here. We're building our view using GenericAPIView, and adding in ListModelMixin and CreateModelMixin.

# The base class provides the core functionality, and the mixin classes provide the .list() and .create() actions. We're then explicitly binding the get and post methods to the appropriate actions. Simple enough stuff so far.

# class SnippetDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

# Pretty similar. Again we're using the GenericAPIView class to provide the core functionality, and adding in mixins to provide the .retrieve(), .update() and .destroy() actions.

# Using generic class-based views

# Using the mixin classes we've rewritten the views to use slightly less code than before, but we can go one step further. REST framework provides a set of already mixed-in generic views that we can use to trim down our views.py module even more.

from rest_framework import generics
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly


# class SnippetList(generics.ListCreateAPIView):
# 	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
# 	queryset = Snippet.objects.all()
# 	serializer_class = SnippetSerializer

# 	def perform_create(self, serializer):
# 		serializer.save(owner=self.request.user)

# class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
# 	permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
# 	queryset = Snippet.objects.all()
# 	serializer_class = SnippetSerializer

from snippets.serializers import UserSerializer
from django.contrib.auth.models import User


# class UserList(generics.ListAPIView):
# 	queryset = User.objects.all()
# 	serializer_class = UserSerializer

# class UserDetail(generics.RetrieveAPIView):
# 	queryset = User.objects.all()
# 	serializer_class = UserSerializer

# Tutorial 5: Relationships & Hyperlinked APIs

# At the moment relationships within our API are represented by using primary keys. In this part of the tutorial we'll improve the cohesion and discoverability of our API, by instead using hyperlinking for relationships. Creating an endpoint for the root of our API

# Right now we have endpoints for 'snippets' and 'users', but we don't have a single entry point to our API. To create one, we'll use a regular function-based view and the @api_view decorator we introduced earlier. In your snippets/views.py add:

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(['GET'])
def api_root(request, format=None):
	return Response({
		'users' : reverse('user-list', request=request, format=format),
		'snippets': reverse('snippet-list', request=request, format=format)
		})
# Creating an endpoint for the highlighted snippets

# The other obvious thing that's still missing from our pastebin API is the code highlighting endpoints.

# Unlike all our other API endpoints, we don't want to use JSON, but instead just present an HTML representation. There are two styles of HTML renderer provided by REST framework, one for dealing with HTML rendered using templates, the other for dealing with pre-rendered HTML. The second renderer is the one we'd like to use for this endpoint. The other thing we need to consider when creating the code highlight view is that there's no existing concrete generic view that we can use. We're not returning an object instance, but instead a property of an object instance. Instead of using a concrete generic view, we'll use the base class for representing instances, and create our own .get() method. In your snippets/views.py add:

from rest_framework import renderers
from rest_framework.response import Response

# class SnippetHighlight(generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     renderer_classes = [renderers.StaticHTMLRenderer]

#     def get(self, request, *args, **kwargs):
#         snippet = self.get_object()
#         return Response(snippet.higlighted) # highligthed, i wrote 'higlighted' in model

# Refactoring to use ViewSets

# Let's take our current set of views, and refactor them into view sets.

# First of all let's refactor our UserList and UserDetail views into a single UserViewSet. We can remove the two views, and replace them with a single class:

from rest_framework import viewsets
class UserViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer


# Here we've used the ReadOnlyModelViewSet class to automatically provide the default 'read-only' operations. We're still setting the queryset and serializer_class attributes exactly as we did when we were using regular views, but we no longer need to provide the same information to two separate classes.

# Next we're going to replace the SnippetList, SnippetDetail and SnippetHighlight view classes. We can remove the three views, and again replace them with a single class.

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions

class SnippetViewSet(viewsets.ModelViewSet):
	queryset = Snippet.objects.all()
	serializer_class = SnippetSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

	@action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
	def highlight(self, request, *args, **kwargs):
		snippet = self.get_object()
		return Response(snippet.higlighted) # highligthed, i wrote 'higlighted' in model

	def perform_create(self, serialaizer):
		serializer.save(owner=self.request.user)