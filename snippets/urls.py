from django.urls import path
from snippets import views
from rest_framework.urlpatterns import format_suffix_patterns

# Function BAsed
# urlpatterns = [
# 	path('snippets/', views.snippet_list),
# 	path('snippets/<int:pk>/', views.snippet_detail),
# ]

# urlpatterns = format_suffix_patterns(urlpatterns)

# class Based
urlpatterns = [
	path('snippets/', views.SnippetList.as_view()),
	path('snippets/<int:pk>', views.SnippetDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)