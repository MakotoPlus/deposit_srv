"""deposit_srv URL Configuration

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
from django.urls import include, path
from django.conf.urls import url
from rest_framework import routers
from deposit_srv.quickstart import views
from django.contrib import admin
from deposit.urls import router as deposit_router
import deposit.urls 
#from deposit.urls import urlpatterns as deposit_router
from rest_framework_jwt.views import obtain_jwt_token # JWT認証のために追加


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    #url('', include(deposit_router.urls)),
    url('', include(deposit.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', obtain_jwt_token), # 認証のためのURL    
    url(r'^', include(deposit.urls)),
]
'''
url('', include(deposit_router.urls)),
url(r'^admin/', admin.site.urls),
url(r'^api/', include(deposit_router.urls)),
'''

#urlpatterns = format_suffix_patterns(urlpatterns)
