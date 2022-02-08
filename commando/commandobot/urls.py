"""commandobot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from commando import views, auth

auth

urlpatterns = [
  path(
    '', 
    views.index
  ),
  path(
    'images/<str:id>/', 
    views.normal_image_render
  ),
  path(
    'images/banners/<str:id>/', 
    views.banner_render
  ),
  path(
    'images/<str:id>/variants/<str:channel>/<str:material>', 
    views.variant_image_render
  ),
  path(
    'admin/', 
    admin.site.urls
  ),
  path(
    'userinfo', 
    views.get_authenticated_user, 
  ),
  path(
    'login', 
    views.discord_login, 
  ),
  path(
    'recieve', 
    views.discord_login_redirect, 
  ),
  path(
    'logout', 
    views.logouts, 
  ),
  path(
    'dash', 
    views.dash, 
  ),
  path(
    "favicon.ico",
    views.render_favicon
  ),
  path(
    "guilds",
    views.guilds
  ),
  path(
    "assets",
    views.asset_render
  ),
  path(
    "pages",
    views.page_render
  ),
  path(
    "html",
    views.dash_i
  ),
  path(
    "files",
    views.files
  )
]
