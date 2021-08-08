"""wordbook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

from app.views import WordViewSet, CourseViewSet
from rest_framework.routers import DefaultRouter


from rest_framework_nested import routers


urlpatterns = [
    path("admin/", admin.site.urls),
]

router = routers.SimpleRouter()
router.register(r"courses", CourseViewSet, basename="courses")

courses_router = routers.NestedSimpleRouter(router, r"courses", lookup="course")
courses_router.register(r"words", WordViewSet, basename="courses-words")


router.register(r"words", WordViewSet, basename="words")


urlpatterns = [
    path("admin/", admin.site.urls),
]

# router = DefaultRouter()
# router.register(r"words", WordViewSet, basename="words")
# router.register(r"courses", CourseViewSet, basename="courses")
# urlpatterns += router.urls

urlpatterns += [
    url(r"^auth/", include("djoser.urls")),
    url(r"^auth/", include("djoser.urls.authtoken")),
]


urlpatterns += [
    path(r"", include(router.urls)),
    path(r"", include(courses_router.urls)),
]
