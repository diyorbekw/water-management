# core/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'banners', views.BannerViewSet)
router.register(r'statistics', views.StatisticsViewSet)
router.register(r'useful-links', views.UsefulLinkViewSet)
router.register(r'news', views.NewsViewSet)
router.register(r'about', views.AboutViewSet)
router.register(r'leadership', views.LeadershipViewSet)
router.register(r'job-vacancy-departments', views.JobVacancyDepartmentViewSet)
router.register(r'type-of-works', views.TypeOfWorkViewSet)
router.register(r'job-vacancies', views.JobVacancyViewSet)
router.register(r'interactive-services', views.InteractiveServiceViewSet)
router.register(r'decisions', views.DecisionViewSet)
router.register(r'contacts', views.ContactViewSet)

urlpatterns = [
    path('', include(router.urls)),
]