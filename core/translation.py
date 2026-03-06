from modeltranslation.translator import translator, TranslationOptions
from .models import (
    Banner, UsefulLink, News, About, Leadership, 
    JobVacancyDepartment, TypeOfWork, JobVacancy,
    InteractiveService, Decision, CentralOffice,
    RegionalDepartment, TaskFunction, Law,
    Document, OpenData
)

class BannerTranslationOptions(TranslationOptions):
    fields = ('title',)

class UsefulLinkTranslationOptions(TranslationOptions):
    fields = ('name',)

class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'content', 'category')

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

# -------------------- YANGI TARJIMALAR --------------------

class CentralOfficeTranslationOptions(TranslationOptions):
    fields = ('name', 'leader', 'position', 'description', 'phone', 'reception_days')

class RegionalDepartmentTranslationOptions(TranslationOptions):
    fields = ('name', 'address', 'leader', 'phone')

class TaskFunctionTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

class LawTranslationOptions(TranslationOptions):
    fields = ('title', 'number')

class DocumentTranslationOptions(TranslationOptions):
    fields = ('title',)

class OpenDataTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

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

# -------------------- YANGI REGISTRATION --------------------
translator.register(CentralOffice, CentralOfficeTranslationOptions)
translator.register(RegionalDepartment, RegionalDepartmentTranslationOptions)
translator.register(TaskFunction, TaskFunctionTranslationOptions)
translator.register(Law, LawTranslationOptions)
translator.register(Document, DocumentTranslationOptions)
translator.register(OpenData, OpenDataTranslationOptions)