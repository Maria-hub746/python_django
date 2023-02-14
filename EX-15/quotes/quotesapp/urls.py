from django.urls import path
from . import views

app_name = 'quotesapp'

urlpatterns = [
    path('', views.main, name='main'),
    path('page/<int:page>', views.main, name='mainpage'),
    path('authors/', views.get_authors, name='authors'),
    path('authors/page/<int:page>', views.get_authors, name='authorspage'),
    path('tags/', views.get_tags, name='tags'),
    path('tags/page/<int:page>', views.get_tags, name='tagspage'),
    path('author/<int:author_id>', views.author, name='author'),
    path('removequote/<int:quote_id>', views.remove_quote, name='removequote'),
    path('removetag/<int:tag_id>', views.remove_tag, name='removetag'),
    path('removeauthor/<int:author_id>', views.remove_author, name='removeauthor'),
    path('editauthor/<int:author_id>', views.edit_author, name='editauthor'),
    path('tag/<int:tag_id>', views.tag, name='tag'),
    path('tag/<int:tag_id>/page/<int:page>', views.tag, name='tagpage'),
    path('detail/<int:quote_id>', views.detail, name='detail'),
    path('addauthor/', views.addauthor, name='addauthor'),
    path('addtag/', views.addtag, name='addtag'),
    path('addquote/', views.addquote, name='addquote'),
]