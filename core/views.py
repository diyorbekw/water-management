from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.core.cache import cache
from django.db.models import Q
import logging

from .models import *
from .serializers import *
from .utils import send_telegram_message

logger = logging.getLogger(__name__)

class BannerViewSet(viewsets.ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [AllowAny]
    
    @method_decorator(cache_page(60 * 60 * 2))  # 2 soat cache
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class StatisticsViewSet(viewsets.ModelViewSet):
    queryset = Statistics.objects.all()
    serializer_class = StatisticsSerializer
    permission_classes = [AllowAny]
    
    @method_decorator(cache_page(60 * 60))  # 1 soat cache
    def list(self, request, *args, **kwargs):
        # Faqat eng oxirgi statistikani olish
        latest_stats = self.queryset.last()
        if latest_stats:
            serializer = self.get_serializer(latest_stats)
            return Response(serializer.data)
        return Response({})

class UsefulLinkViewSet(viewsets.ModelViewSet):
    queryset = UsefulLink.objects.all()
    serializer_class = UsefulLinkSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'name_ru', 'name_uz_cyrl']

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'title_ru', 'title_uz_cyrl', 'content', 'content_ru', 'content_uz_cyrl', 'category', 'category_ru', 'category_uz_cyrl']
    ordering_fields = ['created_date', 'title', 'minutes_to_read']
    filterset_fields = ['category']
    
    @method_decorator(cache_page(60 * 30))  # 30 daqiqa cache
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @action(detail=True, methods=['get'])
    def increment_views(self, request, pk=None):
        news = self.get_object()
        hit_count = HitCount.objects.get_for_object(news)
        hit_count.hit()
        return Response({'views': hit_count.hits})

class AboutViewSet(viewsets.ModelViewSet):
    queryset = About.objects.all()
    serializer_class = AboutSerializer
    permission_classes = [AllowAny]
    
    @method_decorator(cache_page(60 * 60 * 24))  # 24 soat cache
    def list(self, request, *args, **kwargs):
        # Faqat eng oxirgi ma'lumotni olish
        latest_about = self.queryset.last()
        if latest_about:
            serializer = self.get_serializer(latest_about)
            return Response(serializer.data)
        return Response({})

class LeadershipViewSet(viewsets.ModelViewSet):
    queryset = Leadership.objects.all()
    serializer_class = LeadershipSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['full_name', 'full_name_ru', 'full_name_uz_cyrl', 'position', 'position_ru', 'position_uz_cyrl']
    
    @method_decorator(cache_page(60 * 60))  # 1 soat cache
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class JobVacancyDepartmentViewSet(viewsets.ModelViewSet):
    queryset = JobVacancyDepartment.objects.all()
    serializer_class = JobVacancyDepartmentSerializer
    permission_classes = [AllowAny]

class TypeOfWorkViewSet(viewsets.ModelViewSet):
    queryset = TypeOfWork.objects.all()
    serializer_class = TypeOfWorkSerializer
    permission_classes = [AllowAny]

class JobVacancyViewSet(viewsets.ModelViewSet):
    queryset = JobVacancy.objects.all()
    serializer_class = JobVacancySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'title_ru', 'title_uz_cyrl', 'description', 'description_ru', 'description_uz_cyrl']
    ordering_fields = ['created_date', 'title']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Filterlash imkoniyatlari
        leadership = self.request.query_params.get('leadership', None)
        department = self.request.query_params.get('department', None)
        type_of_work = self.request.query_params.get('type_of_work', None)
        
        if leadership:
            queryset = queryset.filter(leadership_id=leadership)
        if department:
            queryset = queryset.filter(department_id=department)
        if type_of_work:
            queryset = queryset.filter(type_of_work_id=type_of_work)
        
        return queryset

class InteractiveServiceViewSet(viewsets.ModelViewSet):
    queryset = InteractiveService.objects.all()
    serializer_class = InteractiveServiceSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'title_ru', 'title_uz_cyrl', 'about', 'about_ru', 'about_uz_cyrl']
    
    @action(detail=True, methods=['get'])
    def increment_views(self, request, pk=None):
        service = self.get_object()
        hit_count = HitCount.objects.get_for_object(service)
        hit_count.hit()
        return Response({'views': hit_count.hits})

class DecisionViewSet(viewsets.ModelViewSet):
    queryset = Decision.objects.all()
    serializer_class = DecisionSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'title_ru', 'title_uz_cyrl', 'content', 'content_ru', 'content_uz_cyrl']
    ordering_fields = ['created_date', 'title']
    
    @action(detail=True, methods=['get'])
    def increment_views(self, request, pk=None):
        decision = self.get_object()
        hit_count = HitCount.objects.get_for_object(decision)
        hit_count.hit()
        return Response({'views': hit_count.hits})

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ContactCreateSerializer
        return ContactSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Telegramga xabar yuborish
        try:
            contact = serializer.instance
            message = f"📩 Yangi murojaat!\n\n👤 Ism: {contact.full_name}\n📞 Telefon: {contact.phone_number}\n📧 Email: {contact.email}\n✉️ Xabar: {contact.message}\n⏰ Vaqt: {contact.created_date.strftime('%d.%m.%Y %H:%M')}"
            send_telegram_message(message)
        except Exception as e:
            logger.error(f"Telegramga xabar yuborishda xatolik: {e}")
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            {'message': 'Murojaatingiz qabul qilindi. Tez orada aloqaga chiqamiz.'},
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    @action(detail=True, methods=['patch'])
    def mark_as_read(self, request, pk=None):
        contact = self.get_object()
        contact.is_read = True
        contact.save()
        return Response({'status': 'Murojaat o\'qilgan deb belgilandi'})