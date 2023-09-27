from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
# from django.contrib.auth import views as auth_views



urlpatterns = [ 
    path('',views.home,name='blog-home'),
    path('about/',views.about,name='blog-about'),
    path('contact/',views.contact,name='blog-contact'),
    path('blog/',views.blog,name='blog-bloges'),
    path('singles/<slug:slug>-<uuid:uuid>/',views.singles,name='blog-detail'),
    path('create/',views.create,name='blog-create'),
    path('update/<slug:slug>-<uuid:uuid>/',views.update_post,name='blog-update'),
    path('singles/<slug:slug>-<uuid:uuid>/delete/',views.delete,name='blog-delete'),
    # path('postComment',views.postComment,name='postComment'),
  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)