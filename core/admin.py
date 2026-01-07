from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from hitcount.models import HitCount
from .models import *

# Base admin class with common functionality
class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date', 'updated_date')
    list_per_page = 20

# Statistics Admin
@admin.register(Statistics)
class StatisticsAdmin(BaseAdmin):
    list_display = ('korsatilayotgan_xizmatlar', 'hududiy_boshqarmalar_soni', 'nasos_stansiyalar_soni', 'xodimlar', 'created_date')
    fields = ('korsatilayotgan_xizmatlar', 'hududiy_boshqarmalar_soni', 'nasos_stansiyalar_soni', 'xodimlar', 'created_date', 'updated_date')

# Contact Admin
@admin.register(Contact)
class ContactAdmin(BaseAdmin):
    list_display = ('full_name', 'phone_number', 'email', 'created_date', 'is_read')
    list_filter = ('is_read', 'created_date')
    search_fields = ('full_name', 'phone_number', 'email', 'message')
    list_editable = ('is_read',)
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, _("Tanlangan murojaatlar o'qilgan deb belgilandi"))
    mark_as_read.short_description = _("Tanlanganlarni o'qilgan deb belgilash")
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
        self.message_user(request, _("Tanlangan murojaatlar o'qilmagan deb belgilandi"))
    mark_as_unread.short_description = _("Tanlanganlarni o'qilmagan deb belgilash")

# Banner Admin
@admin.register(Banner)
class BannerAdmin(BaseAdmin):
    list_display = ('title', 'title_ru', 'title_uz_cyrl', 'created_date')
    search_fields = ('title', 'title_ru', 'title_uz_cyrl')
    list_filter = ('created_date',)
    fieldsets = (
        ('O\'zbekcha (Lotin)', {
            'fields': ('title', 'image')
        }),
        ('Ruscha', {
            'fields': ('title_ru',),
            'classes': ('collapse',)
        }),
        ('O\'zbekcha (Kirill)', {
            'fields': ('title_uz_cyrl',),
            'classes': ('collapse',)
        }),
    )

# UsefulLink Admin
@admin.register(UsefulLink)
class UsefulLinkAdmin(BaseAdmin):
    list_display = ('name', 'name_ru', 'name_uz_cyrl', 'link', 'created_date')
    search_fields = ('name', 'name_ru', 'name_uz_cyrl', 'link')
    list_filter = ('created_date',)
    fieldsets = (
        ('O\'zbekcha (Lotin)', {
            'fields': ('name', 'link', 'icon')
        }),
        ('Ruscha', {
            'fields': ('name_ru',),
            'classes': ('collapse',)
        }),
        ('O\'zbekcha (Kirill)', {
            'fields': ('name_uz_cyrl',),
            'classes': ('collapse',)
        }),
    )

# News Admin
@admin.register(News)
class NewsAdmin(BaseAdmin):
    list_display = ('title', 'category', 'minutes_to_read', 'get_views_count', 'created_date')
    list_filter = ('category', 'created_date')
    search_fields = ('title', 'title_ru', 'title_uz_cyrl', 'content', 'content_ru', 'content_uz_cyrl', 'category', 'category_ru', 'category_uz_cyrl')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'main_image', 'category', 'minutes_to_read', 'slug')
        }),
        ('Matn - O\'zbekcha (Lotin)', {
            'fields': ('content',)
        }),
        ('Ruscha tarjimalar', {
            'fields': ('title_ru', 'category_ru', 'content_ru'),
            'classes': ('collapse',)
        }),
        ('O\'zbekcha (Kirill) tarjimalar', {
            'fields': ('title_uz_cyrl', 'category_uz_cyrl', 'content_uz_cyrl'),
            'classes': ('collapse',)
        }),
    ) 
    
    def get_views_count(self, obj):
        return obj.views_count.count()
    get_views_count.short_description = _("Ko'rishlar soni")

# About Admin - FIXED VERSION
@admin.register(About)
class AboutAdmin(BaseAdmin):
    list_display = ('qisqacha_nomlanishi', 'hudud', 'tuman', 'created_date')
    list_filter = ('hudud', 'created_date')
    search_fields = ('qisqacha_nomlanishi', 'tasischi', 'tuman', 'inn')
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('inn', 'qisqacha_nomlanishi', 'hudud', 'tuman', 'manzil', 'davlat_ulishi', 'xojalik_ulishi')
        }),
        ('Tashkiliy ma\'lumotlar', {
            'fields': ('tashkiliy_huquqiy_shakli', 'tashkilot_faoliyatining_holati', 'tasischi')
        }),
        ('Ruscha tarjimalar', {
            'fields': ('qisqacha_nomlanishi_ru', 'tashkiliy_huquqiy_shakli_ru', 
                      'tashkilot_faoliyatining_holati_ru', 'tasischi_ru',
                      'tuman_ru', 'manzil_ru'),
            'classes': ('collapse',)
        }),
        ('O\'zbekcha (Kirill) tarjimalar', {
            'fields': ('qisqacha_nomlanishi_uz_cyrl', 'tashkiliy_huquqiy_shakli_uz_cyrl',
                      'tashkilot_faoliyatining_holati_uz_cyrl', 'tasischi_uz_cyrl',
                      'tuman_uz_cyrl', 'manzil_uz_cyrl'),
            'classes': ('collapse',)
        }),
    )

# Leadership Admin
@admin.register(Leadership)
class LeadershipAdmin(BaseAdmin):
    list_display = ('full_name', 'position', 'phone_number', 'created_date')
    search_fields = ('full_name', 'full_name_ru', 'full_name_uz_cyrl', 'position', 'phone_number')
    list_filter = ('created_date',)
    prepopulated_fields = {'slug': ('full_name',)}
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('full_name', 'position', 'image', 'phone_number', 'slug')
        }),
        ('Qabul vaqtlari', {
            'fields': ('reception_time',)
        }),
        ('Ma\'lumot - O\'zbekcha (Lotin)', {
            'fields': ('about', 'labor_activity')
        }),
        ('Ruscha tarjimalar', {
            'fields': ('full_name_ru', 'position_ru', 'reception_time_ru', 
                      'about_ru', 'labor_activity_ru'),
            'classes': ('collapse',)
        }),
        ('O\'zbekcha (Kirill) tarjimalar', {
            'fields': ('full_name_uz_cyrl', 'position_uz_cyrl', 'reception_time_uz_cyrl',
                      'about_uz_cyrl', 'labor_activity_uz_cyrl'),
            'classes': ('collapse',)
        }),
    )

# JobVacancyDepartment Admin
@admin.register(JobVacancyDepartment)
class JobVacancyDepartmentAdmin(BaseAdmin):
    list_display = ('title', 'title_ru', 'title_uz_cyrl', 'created_date')
    search_fields = ('title', 'title_ru', 'title_uz_cyrl')
    fieldsets = (
        ('O\'zbekcha (Lotin)', {
            'fields': ('title',)
        }),
        ('Ruscha', {
            'fields': ('title_ru',),
            'classes': ('collapse',)
        }),
        ('O\'zbekcha (Kirill)', {
            'fields': ('title_uz_cyrl',),
            'classes': ('collapse',)
        }),
    )

# TypeOfWork Admin
@admin.register(TypeOfWork)
class TypeOfWorkAdmin(BaseAdmin):
    list_display = ('title', 'title_ru', 'title_uz_cyrl', 'created_date')
    search_fields = ('title', 'title_ru', 'title_uz_cyrl')
    fieldsets = (
        ('O\'zbekcha (Lotin)', {
            'fields': ('title',)
        }),
        ('Ruscha', {
            'fields': ('title_ru',),
            'classes': ('collapse',)
        }),
        ('O\'zbekcha (Kirill)', {
            'fields': ('title_uz_cyrl',),
            'classes': ('collapse',)
        }),
    )

@admin.register(JobVacancy)
class JobVacancyAdmin(BaseAdmin):
    list_display = ('title', 'get_leadership', 'get_department', 'get_type_of_work', 'created_date')
    list_filter = ('leadership', 'department', 'type_of_work', 'created_date')
    search_fields = ('title', 'title_ru', 'title_uz_cyrl', 'location', 'description')
    # raw_id_fields ni olib tashlang yoki kommentga oling
    # raw_id_fields = ('leadership', 'department', 'type_of_work')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'leadership', 'department', 'type_of_work', 'location', 'slug')
        }),
        ('Tavsif - O\'zbekcha (Lotin)', {
            'fields': ('description',)
        }),
        ('Ruscha tarjimalar', {
            'fields': ('title_ru', 'location_ru', 'description_ru'),
            'classes': ('collapse',)
        }),
        ('O\'zbekcha (Kirill) tarjimalar', {
            'fields': ('title_uz_cyrl', 'location_uz_cyrl', 'description_uz_cyrl'),
            'classes': ('collapse',)
        }),
    )
    
    def get_leadership(self, obj):
        return obj.leadership.full_name
    get_leadership.short_description = "Rahbar"
    get_leadership.admin_order_field = 'leadership'
    
    def get_department(self, obj):
        return obj.department.title
    get_department.short_description = "Bo'lim"
    get_department.admin_order_field = 'department'
    
    def get_type_of_work(self, obj):
        return obj.type_of_work.title
    get_type_of_work.short_description = "Ish turi"
    get_type_of_work.admin_order_field = 'type_of_work'

# InteractiveService Admin
@admin.register(InteractiveService)
class InteractiveServiceAdmin(BaseAdmin):
    list_display = ('title', 'get_views_count', 'created_date')
    search_fields = ('title', 'title_ru', 'title_uz_cyrl', 'about')
    list_filter = ('created_date',)
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'slug')
        }),
        ('Ma\'lumot - O\'zbekcha (Lotin)', {
            'fields': ('about',)
        }),
        ('Ruscha tarjimalar', {
            'fields': ('title_ru', 'about_ru'),
            'classes': ('collapse',)
        }),
        ('O\'zbekcha (Kirill) tarjimalar', {
            'fields': ('title_uz_cyrl', 'about_uz_cyrl'),
            'classes': ('collapse',)
        }),
    )
    
    def get_views_count(self, obj):
        return obj.views_count.count()
    get_views_count.short_description = _("Ko'rishlar soni")

# Decision Admin
@admin.register(Decision)
class DecisionAdmin(BaseAdmin):
    list_display = ('title', 'get_views_count', 'created_date')
    search_fields = ('title', 'title_ru', 'title_uz_cyrl', 'content')
    list_filter = ('created_date',)
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'slug')
        }),
        ('Mazmuni - O\'zbekcha (Lotin)', {
            'fields': ('content',)
        }),
        ('Ruscha tarjimalar', {
            'fields': ('title_ru', 'content_ru'),
            'classes': ('collapse',)
        }),
        ('O\'zbekcha (Kirill) tarjimalar', {
            'fields': ('title_uz_cyrl', 'content_uz_cyrl'),
            'classes': ('collapse',)
        }),
    )
    
    def get_views_count(self, obj):
        return obj.views_count.count()
    get_views_count.short_description = _("Ko'rishlar soni")