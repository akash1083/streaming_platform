from django.urls import path
from app import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('logout/',views.logout,name='logout'),
    path('add_category/', views.add_category, name='add_category'),
    path("upload_film/", views.upload_film, name="upload_film"),
    path("film/<int:id>/", views.film_details, name="film_details"),
    path("watchlater/add/<int:id>/", views.add_watch_later, name="add_watch_later"),
    path("watchlater/", views.watch_later, name="watch_later"),
    path("watchlater/remove/<int:id>/", views.remove_watch_later, name="remove_watch_later"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("manage_films/", views.manage_films, name="manage_films"),
    path("edit_film/<int:id>/", views.edit_film, name="edit_film"),
    path("delete_film/<int:id>/", views.delete_film, name="delete_film"),
        ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)