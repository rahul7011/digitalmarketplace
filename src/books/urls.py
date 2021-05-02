from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import book_list,book_detail,chapter_detail,exercise_detail

app_name="books"
urlpatterns = [
    path('',book_list,name='book-list'),
    path('<slug>/',book_detail,name='book-detail'),
    path('<book_slug>/<int:chapter_number>',chapter_detail,name='chapter-detail'),
    path('<book_slug>/<int:chapter_number>/<int:exercise_number>',exercise_detail,name='exercise-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)