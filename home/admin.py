from django.contrib import admin
from .models import (
    HeroSection, AboutSection, ContactSettings,
    PracticeArea, CaseStudy, Testimonial
)

# Singleton modellar uchun (bitta dona bo'lishi kerak bo'lganlar)
class SingletonAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Agar allaqachon bitta yozuv bo'lsa, yangisini qo'shishni taqiqlash
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(HeroSection)
class HeroSectionAdmin(SingletonAdmin):
    list_display = ('title', 'badge')

@admin.register(AboutSection)
class AboutSectionAdmin(SingletonAdmin):
    list_display = ('title', 'badge')

@admin.register(ContactSettings)
class ContactSettingsAdmin(SingletonAdmin):
    list_display = ('title', 'badge')

# Ro'yxatli modellar
@admin.register(PracticeArea)
class PracticeAreaAdmin(admin.ModelAdmin):
    # XATO SHU YERDA EDI: 'icon_name' emas, 'icon' bo'lishi kerak
    list_display = ('title', 'icon')

@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'year', 'outcome')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    # XATO SHU YERDA EDI: 'author_name' emas 'author', 'author_role' emas 'role'
    list_display = ('author', 'role')