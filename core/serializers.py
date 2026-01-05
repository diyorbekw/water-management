from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from .models import *


class BannerSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Banner
        fields = '__all__'
    
    @extend_schema_field(OpenApiTypes.URI)
    def get_image_url(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class StatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistics
        fields = '__all__'


class UsefulLinkSerializer(serializers.ModelSerializer):
    icon_url = serializers.SerializerMethodField()
    
    class Meta:
        model = UsefulLink
        fields = '__all__'
    
    @extend_schema_field(OpenApiTypes.URI)
    def get_icon_url(self, obj):
        if obj.icon and hasattr(obj.icon, 'url'):
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.icon.url)
            return obj.icon.url
        return None


class NewsSerializer(serializers.ModelSerializer):
    views_count = serializers.SerializerMethodField()
    main_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = News
        fields = '__all__'
    
    @extend_schema_field(OpenApiTypes.INT)
    def get_views_count(self, obj):
        return obj.get_views_count()
    
    @extend_schema_field(OpenApiTypes.URI)
    def get_main_image_url(self, obj):
        if obj.main_image and hasattr(obj.main_image, 'url'):
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.main_image.url)
            return obj.main_image.url
        return None


class AboutSerializer(serializers.ModelSerializer):
    hudud_display = serializers.SerializerMethodField()
    
    class Meta:
        model = About
        fields = '__all__'
    
    @extend_schema_field(OpenApiTypes.STR)
    def get_hudud_display(self, obj):
        return obj.get_hudud_display_uz()


class LeadershipSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Leadership
        fields = '__all__'
    
    @extend_schema_field(OpenApiTypes.URI)
    def get_image_url(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class JobVacancyDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobVacancyDepartment
        fields = '__all__'


class TypeOfWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeOfWork
        fields = '__all__'


class JobVacancySerializer(serializers.ModelSerializer):
    leadership_name = serializers.CharField(source='leadership.full_name', read_only=True)
    department_name = serializers.CharField(source='department.title', read_only=True)
    type_of_work_name = serializers.CharField(source='type_of_work.title', read_only=True)
    
    class Meta:
        model = JobVacancy
        fields = '__all__'
        read_only_fields = ('leadership_name', 'department_name', 'type_of_work_name')


class InteractiveServiceSerializer(serializers.ModelSerializer):
    views_count = serializers.SerializerMethodField()
    
    class Meta:
        model = InteractiveService
        fields = '__all__'
    
    @extend_schema_field(OpenApiTypes.INT)
    def get_views_count(self, obj):
        return obj.get_views_count()


class DecisionSerializer(serializers.ModelSerializer):
    views_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Decision
        fields = '__all__'
    
    @extend_schema_field(OpenApiTypes.INT)
    def get_views_count(self, obj):
        return obj.get_views_count()


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
        read_only_fields = ('is_read',)


class ContactCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['full_name', 'phone_number', 'email', 'message']