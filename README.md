## https://www.django-rest-framework.org/tutorial/quickstart/

# Tutorial 1: Serialization

## This tutorial will cover creating a simple pastebin code highlighting Web API. Along the way it will introduce the various components that make up REST framework, and give you a comprehensive understanding of how everything fits together.

## The tutorial is fairly in-depth, so you should probably get a cookie and a cup of your favorite brew before getting started. If you just want a quick overview, you should head over to the quickstart documentation instead.

# Tutorial 2: Requests and Responses

## Request objects

## REST framework introduces a Request object that extends the regular HttpRequest, and provides more flexible request parsing. The core functionality of the Request object is the request.data attribute, which is similar to request.POST, but more useful for working with Web APIs.

***request.POST  # Only handles form data.  Only works for 'POST' method.
request.data  # Handles arbitrary data.  Works for 'POST', 'PUT' and 'PATCH' methods.***

## REST framework also introduces a Response object, which is a type of TemplateResponse that takes unrendered content and uses content negotiation to determine the correct content type to return to the client.

***return Response(data)  # Renders to content type as requested by the client.***

## Using numeric HTTP status codes in your views doesn't always make for obvious reading, and it's easy to not notice if you get an error code wrong. REST framework provides more explicit identifiers for each status code, such as HTTP_400_BAD_REQUEST in the status module. It's a good idea to use these throughout rather than using numeric identifiers.

## Wrapping API views

***REST framework provides two wrappers you can use to write API views.***

    The @api_view decorator for working with function based views.
    The APIView class for working with class-based views.

## These wrappers provide a few bits of functionality such as making sure you receive Request instances in your view, and adding context to Response objects so that content negotiation can be performed.

## The wrappers also provide behaviour such as returning 405 Method Not Allowed responses when appropriate, and handling any ParseError exceptions that occur when accessing request.data with malformed input.

# Tutorial 3: Class-based Views

## We can also write our API views using class-based views, rather than function based views. As we'll see this is a powerful pattern that allows us to reuse common functionality, and helps us keep our code DRY.
Rewriting our API using class-based views

## We'll start by rewriting the root view as a class-based view. All this involves is a little bit of refactoring of views.py.

# Tutorial 4: Authentication & Permissions

## Currently our API doesn't have any restrictions on who can edit or delete code snippets. We'd like to have some more advanced behavior in order to make sure that:

    Code snippets are always associated with a creator.
    Only authenticated users may create snippets.
    Only the creator of a snippet may update or delete it.
    Unauthenticated requests should have full read-only access.
