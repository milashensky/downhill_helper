"""downhill_helper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.urls import path, include
from races.views import CreateInitialBracketsView, CreateStageBracketsView


admin_urls = (
    [
        path('create_initial_brackets/<int:race_id>/', CreateInitialBracketsView.as_view(), name='create_initial_brackets_view'),
        path('create_stage_brackets/<int:race_id>/', CreateStageBracketsView.as_view(), name='create_stage_brackets_view'),
    ]
    + admin.site.urls[0],
    'admin',
    'admin',
)


urlpatterns = [
    path(settings.BASE_URL, include([
        path('admin/', admin_urls),
        path('api/sensors/', include(('sensors.urls', 'sensors'), namespace='sensors')),
        path('races/', include(('races.urls', 'races'), namespace='races')),
    ])),
]
