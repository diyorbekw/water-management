from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from ckeditor.fields import RichTextField  # O'ZGARTIRILDI: tinymce -> ckeditor
from ckeditor_uploader.fields import RichTextUploadingField  # YANGI: Rasm yuklash uchun
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation

class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

# 1. Banner modeli
class Banner(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Sarlavha")
    title_ru = models.CharField(max_length=255, verbose_name="Заголовок", blank=True, null=True)
    title_uz_cyrl = models.CharField(max_length=255, verbose_name="Сарлавҳа (Кирилл)", blank=True, null=True)
    image = models.ImageField(upload_to='banners/', verbose_name="Rasm")
    
    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Bannerlar"
        ordering = ['-created_date']
    
    def __str__(self):
        return self.title
    
    def get_translated_title(self, language_code='uz'):
        """Til bo'yicha tarjima qilingan sarlavha"""
        if language_code == 'ru':
            return self.title_ru or self.title
        elif language_code == 'uz-cyrl':
            return self.title_uz_cyrl or self.title
        return self.title

# 2. Statistics modeli
class Statistics(BaseModel):
    korsatilayotgan_xizmatlar = models.IntegerField(verbose_name="Ko'rsatilayotgan xizmatlar soni", default=0)
    hududiy_boshqarmalar_soni = models.IntegerField(verbose_name="Hududiy boshqarmalar soni", default=0)
    nasos_stansiyalar_soni = models.IntegerField(verbose_name="Nasos stansiyalari soni", default=0)
    xodimlar = models.IntegerField(verbose_name="Xodimlar soni", default=0)
    
    class Meta:
        verbose_name = "Statistika"
        verbose_name_plural = "Statistika ma'lumotlari"
    
    def __str__(self):
        return f"Statistika: {self.created_date.strftime('%d.%m.%Y')}"

# 3. Useful Links modeli
class UsefulLink(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Nomi")
    name_ru = models.CharField(max_length=255, verbose_name="Название", blank=True, null=True)
    name_uz_cyrl = models.CharField(max_length=255, verbose_name="Номи (Кирилл)", blank=True, null=True)
    link = models.URLField(verbose_name="Havola")
    icon = models.ImageField(upload_to='links_icons/', verbose_name="Ikona")
    
    class Meta:
        verbose_name = "Foydali havola"
        verbose_name_plural = "Foydali havolalar"
        ordering = ['-created_date']
    
    def __str__(self):
        return self.name

# 4. News modeli
class News(BaseModel, HitCountMixin):
    title = models.CharField(max_length=255, verbose_name="Sarlavha")
    title_ru = models.CharField(max_length=255, verbose_name="Заголовок", blank=True, null=True)
    title_uz_cyrl = models.CharField(max_length=255, verbose_name="Сарлавҳа (Кирилл)", blank=True, null=True)
    main_image = models.ImageField(upload_to='news/', verbose_name="Asosiy rasm")
    
    # YANGI: Category field qo'shildi (varchar)
    category = models.CharField(
        max_length=100, 
        verbose_name="Kategoriya",
        blank=True,
        null=True
    )
    category_ru = models.CharField(
        max_length=100, 
        verbose_name="Категория",
        blank=True,
        null=True
    )
    category_uz_cyrl = models.CharField(
        max_length=100, 
        verbose_name="Категория (Кирилл)",
        blank=True,
        null=True
    )
    
    # YANGI: O'qish vaqti (daqiqalarda)
    minutes_to_read = models.PositiveIntegerField(
        verbose_name="O'qish vaqti (daqiqa)",
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(60)]
    )
    
    content = RichTextUploadingField(verbose_name="Matn")
    content_ru = RichTextUploadingField(verbose_name="Текст", blank=True, null=True)
    content_uz_cyrl = RichTextUploadingField(verbose_name="Матн (Кирилл)", blank=True, null=True)
    
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    views_count = GenericRelation(HitCount, object_id_field='object_pk')
    
    class Meta:
        verbose_name = "Yangilik"
        verbose_name_plural = "Yangiliklar"
        ordering = ['-created_date']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{timezone.now().strftime('%Y%m%d%H%M')}")
        super().save(*args, **kwargs)
    
    def get_views_count(self):
        return self.views_count.count()
    
    def get_translated_title(self, language_code='uz'):
        """Til bo'yicha tarjima qilingan sarlavha"""
        if language_code == 'ru':
            return self.title_ru or self.title
        elif language_code == 'uz-cyrl':
            return self.title_uz_cyrl or self.title
        return self.title
    
    def get_translated_content(self, language_code='uz'):
        """Til bo'yicha tarjima qilingan matn"""
        if language_code == 'ru':
            return self.content_ru or self.content
        elif language_code == 'uz-cyrl':
            return self.content_uz_cyrl or self.content
        return self.content
    
    def get_translated_category(self, language_code='uz'):
        """Til bo'yicha tarjima qilingan kategoriya"""
        if language_code == 'ru':
            return self.category_ru or self.category
        elif language_code == 'uz-cyrl':
            return self.category_uz_cyrl or self.category
        return self.category

# Viloyatlar ro'yxati
REGION_CHOICES = [
    ('toshkent_shahri', 'Toshkent shahri'),
    ('toshkent_viloyati', 'Toshkent viloyati'),
    ('andijon_viloyati', 'Andijon viloyati'),
    ('buxoro_viloyati', 'Buxoro viloyati'),
    ('fargona_viloyati', 'Farg\'ona viloyati'),
    ('jizzax_viloyati', 'Jizzax viloyati'),
    ('xorazm_viloyati', 'Xorazm viloyati'),
    ('namangan_viloyati', 'Namangan viloyati'),
    ('navoiy_viloyati', 'Navoiy viloyati'),
    ('qashqadaryo_viloyati', 'Qashqadaryo viloyati'),
    ('qoraqalpogiston', 'Qoraqalpog\'iston Respublikasi'),
    ('samarqand_viloyati', 'Samarqand viloyati'),
    ('sirdaryo_viloyati', 'Sirdaryo viloyati'),
    ('surxondaryo_viloyati', 'Surxondaryo viloyati'),
]

# 5. About modeli
class About(BaseModel):
    inn = models.CharField(max_length=25, verbose_name="INN")
    qisqacha_nomlanishi = models.CharField(max_length=255, verbose_name="Qisqacha nomlanishi")
    qisqacha_nomlanishi_ru = models.CharField(max_length=255, verbose_name="Краткое наименование", blank=True, null=True)
    qisqacha_nomlanishi_uz_cyrl = models.CharField(max_length=255, verbose_name="Қисқача номланиши (Кирилл)", blank=True, null=True)
    
    tashkiliy_huquqiy_shakli = models.CharField(max_length=100, verbose_name="Tashkiliy-huquqiy shakli")
    tashkiliy_huquqiy_shakli_ru = models.CharField(max_length=100, verbose_name="Организационно-правовая форма", blank=True, null=True)
    tashkiliy_huquqiy_shakli_uz_cyrl = models.CharField(max_length=100, verbose_name="Ташкилий-ҳуқуқий шакли (Кирилл)", blank=True, null=True)
    
    tashkilot_faoliyatining_holati = models.CharField(max_length=255, verbose_name="Tashkilot faoliyatining holati")
    tashkilot_faoliyatining_holati_ru = models.CharField(max_length=255, verbose_name="Состояние деятельности организации", blank=True, null=True)
    tashkilot_faoliyatining_holati_uz_cyrl = models.CharField(max_length=255, verbose_name="Ташкилот фаолиятининг ҳолати (Кирилл)", blank=True, null=True)
    
    tasischi = models.CharField(max_length=255, verbose_name="Tasischi")
    tasischi_ru = models.CharField(max_length=255, verbose_name="Учредитель", blank=True, null=True)
    tasischi_uz_cyrl = models.CharField(max_length=255, verbose_name="Тасисчи (Кирилл)", blank=True, null=True)
    
    hudud = models.CharField(max_length=50, choices=REGION_CHOICES, verbose_name="Hudud")
    tuman = models.CharField(max_length=255, verbose_name="Tuman")
    tuman_ru = models.CharField(max_length=255, verbose_name="Район", blank=True, null=True)
    tuman_uz_cyrl = models.CharField(max_length=255, verbose_name="Туман (Кирилл)", blank=True, null=True)
    
    manzil = models.CharField(max_length=255, verbose_name="Manzil")
    manzil_ru = models.CharField(max_length=255, verbose_name="Адрес", blank=True, null=True)
    manzil_uz_cyrl = models.CharField(max_length=255, verbose_name="Манзил (Кирилл)", blank=True, null=True)
    
    davlat_ulishi = models.FloatField(
        verbose_name="Davlat ulushi (%)",
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    xojalik_ulishi = models.FloatField(
        verbose_name="Xo'jalik ulushi (%)",
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    class Meta:
        verbose_name = "Tashkilot haqida"
        verbose_name_plural = "Tashkilot haqida"
    
    def __str__(self):
        return self.qisqacha_nomlanishi
    
    def get_hudud_display_uz(self):
        hudud_map = {
            'toshkent_shahri': 'Toshkent shahri',
            'toshkent_viloyati': 'Toshkent viloyati',
            'andijon_viloyati': 'Andijon viloyati',
            'buxoro_viloyati': 'Buxoro viloyati',
            'fargona_viloyati': 'Farg\'ona viloyati',
            'jizzax_viloyati': 'Jizzax viloyati',
            'xorazm_viloyati': 'Xorazm viloyati',
            'namangan_viloyati': 'Namangan viloyati',
            'navoiy_viloyati': 'Navoiy viloyati',
            'qashqadaryo_viloyati': 'Qashqadaryo viloyati',
            'qoraqalpogiston': 'Qoraqalpog\'iston Respublikasi',
            'samarqand_viloyati': 'Samarqand viloyati',
            'sirdaryo_viloyati': 'Sirdaryo viloyati',
            'surxondaryo_viloyati': 'Surxondaryo viloyati',
        }
        return hudud_map.get(self.hudud, self.hudud)

# 6. Leadership modeli
class Leadership(BaseModel):
    full_name = models.CharField(max_length=255, verbose_name="To'liq ism")
    full_name_ru = models.CharField(max_length=255, verbose_name="Полное имя", blank=True, null=True)
    full_name_uz_cyrl = models.CharField(max_length=255, verbose_name="Тўлиқ исм (Кирилл)", blank=True, null=True)
    
    position = models.CharField(max_length=255, verbose_name="Lavozim")
    position_ru = models.CharField(max_length=255, verbose_name="Должность", blank=True, null=True)
    position_uz_cyrl = models.CharField(max_length=255, verbose_name="Лавозим (Кирилл)", blank=True, null=True)
    
    # YANGI: Rasm maydoni qo'shildi
    image = models.ImageField(upload_to='leadership/', verbose_name="Rasm", blank=True, null=True)
    
    reception_time = models.CharField(max_length=255, verbose_name="Qabul vaqtlari")
    reception_time_ru = models.CharField(max_length=255, verbose_name="Время приема", blank=True, null=True)
    reception_time_uz_cyrl = models.CharField(max_length=255, verbose_name="Қабул вақтлари (Кирилл)", blank=True, null=True)
    
    phone_number = models.CharField(max_length=255, verbose_name="Telefon raqam")
    about = RichTextField(verbose_name="Umumiy ma'lumot")  # O'ZGARTIRILDI: TextField -> RichTextField
    about_ru = RichTextField(verbose_name="Общая информация", blank=True, null=True)  # O'ZGARTIRILDI
    about_uz_cyrl = RichTextField(verbose_name="Умумий маълумот (Кирилл)", blank=True, null=True)  # O'ZGARTIRILDI
    
    labor_activity = RichTextField(verbose_name="Mehnat faoliyati")  # O'ZGARTIRILDI: TextField -> RichTextField
    labor_activity_ru = RichTextField(verbose_name="Трудовая деятельность", blank=True, null=True)  # O'ZGARTIRILDI
    labor_activity_uz_cyrl = RichTextField(verbose_name="Меҳнат фаолияти (Кирилл)", blank=True, null=True)  # O'ZGARTIRILDI
    
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    
    class Meta:
        verbose_name = "Rahbariyat"
        verbose_name_plural = "Rahbariyat"
        ordering = ['-created_date']
    
    def __str__(self):
        return f"{self.full_name} - {self.position}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.full_name}-{self.position}")
        super().save(*args, **kwargs)

# 7. Job Vacancy Department modeli
class JobVacancyDepartment(BaseModel):
    title = models.CharField(max_length=100, verbose_name="Nomi")
    title_ru = models.CharField(max_length=100, verbose_name="Название", blank=True, null=True)
    title_uz_cyrl = models.CharField(max_length=100, verbose_name="Номи (Кирилл)", blank=True, null=True)
    
    class Meta:
        verbose_name = "Bo'lim"
        verbose_name_plural = "Ish o'rinlari bo'limlari"
    
    def __str__(self):
        return self.title

# 8. Type of Work modeli
class TypeOfWork(BaseModel):
    title = models.CharField(max_length=100, verbose_name="Nomi")
    title_ru = models.CharField(max_length=100, verbose_name="Название", blank=True, null=True)
    title_uz_cyrl = models.CharField(max_length=100, verbose_name="Номи (Кирилл)", blank=True, null=True)
    
    class Meta:
        verbose_name = "Ish turi"
        verbose_name_plural = "Ish turlari"
    
    def __str__(self):
        return self.title

# 9. Job Vacancy modeli
class JobVacancy(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Sarlavha")
    title_ru = models.CharField(max_length=255, verbose_name="Заголовок", blank=True, null=True)
    title_uz_cyrl = models.CharField(max_length=255, verbose_name="Сарлавҳа (Кирилл)", blank=True, null=True)
    
    leadership = models.ForeignKey(
        Leadership, 
        on_delete=models.CASCADE, 
        related_name='vacancies',
        verbose_name="Rahbariyat"
    )
    department = models.ForeignKey(
        JobVacancyDepartment,
        on_delete=models.CASCADE,
        related_name='vacancies',
        verbose_name="Bo'lim"
    )
    location = models.CharField(max_length=255, verbose_name="Manzil")
    location_ru = models.CharField(max_length=255, verbose_name="Адрес", blank=True, null=True)
    location_uz_cyrl = models.CharField(max_length=255, verbose_name="Манзил (Кирилл)", blank=True, null=True)
    
    type_of_work = models.ForeignKey(
        TypeOfWork,
        on_delete=models.CASCADE,
        related_name='vacancies',
        verbose_name="Ish turi"
    )
    description = RichTextField(verbose_name="Tavsif")  # O'ZGARTIRILDI: TextField -> RichTextField
    description_ru = RichTextField(verbose_name="Описание", blank=True, null=True)  # O'ZGARTIRILDI
    description_uz_cyrl = RichTextField(verbose_name="Тавсиф (Кирилл)", blank=True, null=True)  # O'ZGARTIRILDI
    
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    
    class Meta:
        verbose_name = "Ish o'rini"
        verbose_name_plural = "Ish o'rinlari"
        ordering = ['-created_date']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{timezone.now().strftime('%Y%m%d')}")
        super().save(*args, **kwargs)

# 10. Interactive Service modeli
class InteractiveService(BaseModel, HitCountMixin):
    title = models.CharField(max_length=255, verbose_name="Sarlavha")
    title_ru = models.CharField(max_length=255, verbose_name="Заголовок", blank=True, null=True)
    title_uz_cyrl = models.CharField(max_length=255, verbose_name="Сарлавҳа (Кирилл)", blank=True, null=True)
    
    about = RichTextField(verbose_name="Ma'lumot")  # O'ZGARTIRILDI: TextField -> RichTextField
    about_ru = RichTextField(verbose_name="Информация", blank=True, null=True)  # O'ZGARTIRILDI
    about_uz_cyrl = RichTextField(verbose_name="Маълумот (Кирилл)", blank=True, null=True)  # O'ZGARTIRILDI
    
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    views_count = GenericRelation(HitCount, object_id_field='object_pk')
    
    class Meta:
        verbose_name = "Interaktiv xizmat"
        verbose_name_plural = "Interaktiv xizmatlar"
        ordering = ['-created_date']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_views_count(self):
        return self.views_count.count()

# 11. Decision modeli
class Decision(BaseModel, HitCountMixin):
    title = models.CharField(max_length=255, verbose_name="Sarlavha")
    title_ru = models.CharField(max_length=255, verbose_name="Заголовок", blank=True, null=True)
    title_uz_cyrl = models.CharField(max_length=255, verbose_name="Сарлавҳа (Кирилл)", blank=True, null=True)
    
    content = RichTextUploadingField(verbose_name="Matn")  # O'ZGARTIRILDI: HTMLField -> RichTextUploadingField
    content_ru = RichTextUploadingField(verbose_name="Текст", blank=True, null=True)  # O'ZGARTIRILDI
    content_uz_cyrl = RichTextUploadingField(verbose_name="Матн (Кирилл)", blank=True, null=True)  # O'ZGARTIRILDI
    
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    views_count = GenericRelation(HitCount, object_id_field='object_pk')
    
    class Meta:
        verbose_name = "Qaror"
        verbose_name_plural = "Qarorlar"
        ordering = ['-created_date']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{timezone.now().strftime('%Y%m%d')}")
        super().save(*args, **kwargs)
    
    def get_views_count(self):
        return self.views_count.count()

# 12. Contact modeli
class Contact(BaseModel):
    full_name = models.CharField(max_length=255, verbose_name="To'liq ism")
    phone_number = models.CharField(max_length=30, verbose_name="Telefon raqam")
    email = models.EmailField(verbose_name="Email")
    message = models.TextField(verbose_name="Xabar")
    is_read = models.BooleanField(default=False, verbose_name="O'qilgan")
    
    class Meta:
        verbose_name = "Murojaat"
        verbose_name_plural = "Murojaatlar"
        ordering = ['-created_date']
    
    def __str__(self):
        return f"{self.full_name} - {self.created_date.strftime('%d.%m.%Y')}"