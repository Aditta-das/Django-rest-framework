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

class SnippetList(generics.ListCreateAPIView):
	queryset = Snippet.objects.all()
	serializer_class = SnippetSerializer

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Snippet.objects.all()
	serializer_class = SnippetSerializer