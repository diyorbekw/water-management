from rest_framework import viewsets, filters, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.core.cache import cache
from django.db.models import Q
import logging

from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import *
from .serializers import *
from .utils import send_telegram_message

logger = logging.getLogger(__name__)


# 1. Banner CRUD
class BannerViewSet(viewsets.ModelViewSet):
    """
    Bannerlar uchun to'liq CRUD amallari
    """
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    
    def get_permissions(self):
        """Faqat list va retrieve uchun ruxsat, qolganlari admin uchun"""
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        """Barcha bannerlarni olish"""
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        """Yangi banner yaratish"""
        return super().create(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        """Bitta bannerni olish"""
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """Bannerni yangilash"""
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """Bannerni qisman yangilash"""
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Bannerni o'chirish"""
        return super().destroy(request, *args, **kwargs)


# 2. Statistics CRUD
class StatisticsViewSet(viewsets.ModelViewSet):
    """
    Statistika ma'lumotlari uchun to'liq CRUD amallari
    """
    queryset = Statistics.objects.all()
    serializer_class = StatisticsSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    @method_decorator(cache_page(60 * 60))
    def list(self, request, *args, **kwargs):
        """Eng oxirgi statistikani olish"""
        latest_stats = self.queryset.last()
        if latest_stats:
            serializer = self.get_serializer(latest_stats)
            return Response(serializer.data)
        return Response({})
    
    def create(self, request, *args, **kwargs):
        """Yangi statistika yaratish"""
        return super().create(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        """Statistikani olish"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        """Statistikani yangilash"""
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """Statistikani qisman yangilash"""
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Statistikani o'chirish"""
        return super().destroy(request, *args, **kwargs)


# 3. UsefulLink CRUD
class UsefulLinkViewSet(viewsets.ModelViewSet):
    """
    Foydali havolalar uchun to'liq CRUD amallari
    """
    queryset = UsefulLink.objects.all()
    serializer_class = UsefulLinkSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'name_ru', 'name_uz_cyrl']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def list(self, request, *args, **kwargs):
        """Barcha foydali havolalarni olish"""
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        """Yangi foydali havola yaratish"""
        return super().create(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        """Foydali havolani olish"""
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """Foydali havolani yangilash"""
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """Foydali havolani qisman yangilash"""
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Foydali havolani o'chirish"""
        return super().destroy(request, *args, **kwargs)


# 4. News CRUD
class NewsViewSet(viewsets.ModelViewSet):
    """
    Yangiliklar uchun to'liq CRUD amallari
    """
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'title_ru', 'title_uz_cyrl', 'content', 'content_ru', 'content_uz_cyrl', 'category', 'category_ru', 'category_uz_cyrl']
    ordering_fields = ['created_date', 'title', 'minutes_to_read']
    filterset_fields = ['category']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'increment_views']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    @method_decorator(cache_page(60 * 30))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        """Barcha yangiliklarni olish"""
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        """Yangi yangilik yaratish"""
        return super().create(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        """Bitta yangilikni olish"""
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """Yangilikni yangilash"""
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """Yangilikni qisman yangilash"""
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Yangilikni o'chirish"""
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=True, methods=['get'])
    def increment_views(self, request, pk=None):
        """Ko'rishlar sonini oshirish"""
        news = self.get_object()
        hit_count = HitCount.objects.get_for_object(news)
        hit_count.hit()
        return Response({'views': hit_count.hits})


# 5. About CRUD
class AboutViewSet(viewsets.ModelViewSet):
    """
    Tashkilot haqida ma'lumot uchun to'liq CRUD amallari
    """
    queryset = About.objects.all()
    serializer_class = AboutSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    @method_decorator(cache_page(60 * 60 * 24))
    def list(self, request, *args, **kwargs):
        """Eng oxirgi tashkilot haqida ma'lumotni olish"""
        latest_about = self.queryset.last()
        if latest_about:
            serializer = self.get_serializer(latest_about)
            return Response(serializer.data)
        return Response({})
    
    def create(self, request, *args, **kwargs):
        """Yangi tashkilot haqida ma'lumot yaratish"""
        return super().create(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        """Tashkilot haqida ma'lumotni olish"""
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """Tashkilot haqida ma'lumotni yangilash"""
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """Tashkilot haqida ma'lumotni qisman yangilash"""
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Tashkilot haqida ma'lumotni o'chirish"""
        return super().destroy(request, *args, **kwargs)


# 6. Leadership CRUD
class LeadershipViewSet(viewsets.ModelViewSet):
    """
    Rahbariyat uchun to'liq CRUD amallari
    """
    queryset = Leadership.objects.all()
    serializer_class = LeadershipSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['full_name', 'full_name_ru', 'full_name_uz_cyrl', 'position', 'position_ru', 'position_uz_cyrl']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    @method_decorator(cache_page(60 * 60))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        """Barcha rahbarlarni olish"""
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        """Yangi rahbar yaratish"""
        return super().create(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        """Bitta rahberni olish"""
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """Rahbarni yangilash"""
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """Rahbarni qisman yangilash"""
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Rahbarni o'chirish"""
        return super().destroy(request, *args, **kwargs)


# 7. JobVacancyDepartment CRUD
class JobVacancyDepartmentViewSet(viewsets.ModelViewSet):
    """
    Ish o'rinlari bo'limlari uchun to'liq CRUD amallari
    """
    queryset = JobVacancyDepartment.objects.all()
    serializer_class = JobVacancyDepartmentSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def list(self, request, *args, **kwargs):
        """Barcha bo'limlarni olish"""
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        """Yangi bo'lim yaratish"""
        return super().create(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        """Bitta bo'limni olish"""
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """Bo'limni yangilash"""
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """Bo'limni qisman yangilash"""
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Bo'limni o'chirish"""
        return super().destroy(request, *args, **kwargs)


# 8. TypeOfWork CRUD
class TypeOfWorkViewSet(viewsets.ModelViewSet):
    """
    Ish turlari uchun to'liq CRUD amallari
    """
    queryset = TypeOfWork.objects.all()
    serializer_class = TypeOfWorkSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def list(self, request, *args, **kwargs):
        """Barcha ish turlarini olish"""
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        """Yangi ish turi yaratish"""
        return super().create(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        """Bitta ish turini olish"""
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """Ish turini yangilash"""
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """Ish turini qisman yangilash"""
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Ish turini o'chirish"""
        return super().destroy(request, *args, **kwargs)


# 9. JobVacancy CRUD
class JobVacancyViewSet(viewsets.ModelViewSet):
    """
    Ish o'rinlari uchun to'liq CRUD amallari
    """
    queryset = JobVacancy.objects.all()
    serializer_class = JobVacancySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'title_ru', 'title_uz_cyrl', 'description', 'description_ru', 'description_uz_cyrl']
    ordering_fields = ['created_date', 'title']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """Filterlash imkoniyatlari"""
        queryset = super().get_queryset()
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
    
    def list(self, request, *args, **kwargs):
        """Barcha ish o'rinlarini olish"""
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        """Yangi ish o'rini yaratish"""
        return super().create(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        """Bitta ish o'rinini olish"""
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """Ish o'rinini yangilash"""
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """Ish o'rinini qisman yangilash"""
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Ish o'rinini o'chirish"""
        return super().destroy(request, *args, **kwargs)


# 10. InteractiveService CRUD
class InteractiveServiceViewSet(viewsets.ModelViewSet):
    """
    Interaktiv xizmatlar uchun to'liq CRUD amallari
    """
    queryset = InteractiveService.objects.all()
    serializer_class = InteractiveServiceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'title_ru', 'title_uz_cyrl', 'about', 'about_ru', 'about_uz_cyrl']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'increment_views']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def list(self, request, *args, **kwargs):
        """Barcha interaktiv xizmatlarni olish"""
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        """Yangi interaktiv xizmat yaratish"""
        return super().create(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        """Bitta interaktiv xizmatni olish"""
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """Interaktiv xizmatni yangilash"""
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """Interaktiv xizmatni qisman yangilash"""
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Interaktiv xizmatni o'chirish"""
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=True, methods=['get'])
    def increment_views(self, request, pk=None):
        """Ko'rishlar sonini oshirish"""
        service = self.get_object()
        hit_count = HitCount.objects.get_for_object(service)
        hit_count.hit()
        return Response({'views': hit_count.hits})


# 11. Decision CRUD
class DecisionViewSet(viewsets.ModelViewSet):
    """
    Qarorlar uchun to'liq CRUD amallari
    """
    queryset = Decision.objects.all()
    serializer_class = DecisionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'title_ru', 'title_uz_cyrl', 'content', 'content_ru', 'content_uz_cyrl']
    ordering_fields = ['created_date', 'title']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'increment_views']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def list(self, request, *args, **kwargs):
        """Barcha qarorlarni olish"""
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        """Yangi qaror yaratish"""
        return super().create(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        """Bitta qarorni olish"""
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """Qarorni yangilash"""
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """Qarorni qisman yangilash"""
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Qarorni o'chirish"""
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=True, methods=['get'])
    def increment_views(self, request, pk=None):
        """Ko'rishlar sonini oshirish"""
        decision = self.get_object()
        hit_count = HitCount.objects.get_for_object(decision)
        hit_count.hit()
        return Response({'views': hit_count.hits})


# 12. Contact CRUD
class ContactViewSet(viewsets.ModelViewSet):
    """
    Murojaatlar uchun to'liq CRUD amallari
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    
    def get_permissions(self):
        """Yaratish hammaga ochiq, qolganlari admin uchun"""
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """Yaratish va boshqalarga alohida serializer"""
        if self.action == 'create':
            return ContactCreateSerializer
        return ContactSerializer
    
    def list(self, request, *args, **kwargs):
        """Barcha murojaatlarni olish (admin)"""
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        """Yangi murojaat yaratish (hamma uchun)"""
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
    
    def retrieve(self, request, *args, **kwargs):
        """Bitta murojaatni olish (admin)"""
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """Murojaatni yangilash (admin)"""
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """Murojaatni qisman yangilash (admin)"""
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Murojaatni o'chirish (admin)"""
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=True, methods=['patch'])
    def mark_as_read(self, request, pk=None):
        """Murojaatni o'qilgan deb belgilash"""
        contact = self.get_object()
        contact.is_read = True
        contact.save()
        return Response({'status': 'Murojaat o\'qilgan deb belgilandi'})