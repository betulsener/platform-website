from django.urls import path
from .views import IndexView, AboutView, AnalysisView, BlogView, ContactView, BlogDetailView, TagDetailView, BlogSearchView, PageDetailView
from . import views


urlpatterns = [
   path('',IndexView.as_view(), name='index'),
   path('abouts',AboutView.as_view(), name='abouts'),
   path('analysis',AnalysisView.as_view(), name='analysis'),
   path('blog',BlogView.as_view(), name='blog'),
   path('blogs/<slug:slug>/', BlogDetailView.as_view(), name='blog-detail'),
   path('search/', BlogSearchView.as_view(), name='blog-search'),
   path('input',ContactView.as_view(), name='input'),
   path('tags/<str:tag_name>/', TagDetailView.as_view(), name='tag-detail'),
   path('pages/<slug:slug>/', PageDetailView.as_view(), name='page-detail' ),
   path('scenarios/', views.scenario_page, name='scenario_page'),
   ]
