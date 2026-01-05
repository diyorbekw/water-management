from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'banners', BannerViewSet)
router.register(r'statistics', StatisticsViewSet)
router.register(r'useful-links', UsefulLinkViewSet)
router.register(r'news', NewsViewSet)
router.register(r'about', AboutViewSet)
router.register(r'leadership', LeadershipViewSet)
router.register(r'departments', JobVacancyDepartmentViewSet)
router.register(r'work-types', TypeOfWorkViewSet)
router.register(r'vacancies', JobVacancyViewSet)
router.register(r'interactive-services', InteractiveServiceViewSet)
router.register(r'decisions', DecisionViewSet)
router.register(r'contacts', ContactViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]