from modeltranslation.translator import translator, TranslationOptions
from .models import (
    Banner, UsefulLink, News, About, Leadership, 
    JobVacancyDepartment, TypeOfWork, JobVacancy,
    InteractiveService, Decision
)

class BannerTranslationOptions(TranslationOptions):
    fields = ('title',)

class UsefulLinkTranslationOptions(TranslationOptions):
    fields = ('name',)

class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'content')

class AboutTranslationOptions(TranslationOptions):
    fields = (
        'qisqacha_nomlanishi',
        'tashkiliy_huquqiy_shakli',
        'tashkilot_faoliyatining_holati',
        'tasischi',
        'tuman',
        'manzil'
    )

class LeadershipTranslationOptions(TranslationOptions):
    fields = ('full_name', 'position', 'reception_time', 'about', 'labor_activity')

class JobVacancyDepartmentTranslationOptions(TranslationOptions):
    fields = ('title',)

class TypeOfWorkTranslationOptions(TranslationOptions):
    fields = ('title',)

class JobVacancyTranslationOptions(TranslationOptions):
    fields = ('title', 'location', 'description')

class InteractiveServiceTranslationOptions(TranslationOptions):
    fields = ('title', 'about')

class DecisionTranslationOptions(TranslationOptions):
    fields = ('title', 'content')

# Tarjimalarni ro'yxatdan o'tkazish
translator.register(Banner, BannerTranslationOptions)
translator.register(UsefulLink, UsefulLinkTranslationOptions)
translator.register(News, NewsTranslationOptions)
translator.register(About, AboutTranslationOptions)
translator.register(Leadership, LeadershipTranslationOptions)
translator.register(JobVacancyDepartment, JobVacancyDepartmentTranslationOptions)
translator.register(TypeOfWork, TypeOfWorkTranslationOptions)
translator.register(JobVacancy, JobVacancyTranslationOptions)
translator.register(InteractiveService, InteractiveServiceTranslationOptions)
translator.register(Decision, DecisionTranslationOptions)