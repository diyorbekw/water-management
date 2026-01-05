from rest_framework import serializers
from .models import *

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'

class StatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistics
        fields = '__all__'

class UsefulLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsefulLink
        fields = '__all__'

class NewsSerializer(serializers.ModelSerializer):
    views_count = serializers.SerializerMethodField()
    translated_title = serializers.SerializerMethodField()
    translated_content = serializers.SerializerMethodField()
    translated_category = serializers.SerializerMethodField()
    
    class Meta:
        model = News
        fields = '__all__'
        read_only_fields = ('translated_title', 'translated_content', 'translated_category')
    
    def get_views_count(self, obj):
        return obj.get_views_count()
    
    def get_translated_title(self, obj):
        request = self.context.get('request')
        language = 'uz'
        if request and hasattr(request, 'GET'):
            language = request.GET.get('language', 'uz')
        return obj.get_translated_title(language)
    
    def get_translated_content(self, obj):
        request = self.context.get('request')
        language = 'uz'
        if request and hasattr(request, 'GET'):
            language = request.GET.get('language', 'uz')
        return obj.get_translated_content(language)
    
    def get_translated_category(self, obj):
        request = self.context.get('request')
        language = 'uz'
        if request and hasattr(request, 'GET'):
            language = request.GET.get('language', 'uz')
        return obj.get_translated_category(language)

class AboutSerializer(serializers.ModelSerializer):
    hudud_display = serializers.SerializerMethodField()
    
    class Meta:
        model = About
        fields = '__all__'
    
    def get_hudud_display(self, obj):
        return obj.get_hudud_display_uz()

class LeadershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leadership
        fields = '__all__'

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
    
    def get_views_count(self, obj):
        return obj.get_views_count()

class DecisionSerializer(serializers.ModelSerializer):
    views_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Decision
        fields = '__all__'
    
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