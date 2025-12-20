from django.db import models


# 1. HERO SECTION
class HeroSection(models.Model):
    badge = models.CharField(max_length=100, default="YURIDIK XIZMATLAR")
    title = models.CharField(max_length=200, default="Professional Yuridik Yordam")
    description = models.TextField(default="Biz sizning huquqlaringizni himoya qilamiz.")
    button_text = models.CharField(max_length=50, default="Bepul Konsultatsiya")
    image = models.ImageField(upload_to='hero/', blank=True, null=True)

    # Stats (Trust Badges)
    stat_1_label = models.CharField(max_length=50, default="Tajriba")
    stat_1_sublabel = models.CharField(max_length=50, default="15 Yil")
    stat_2_label = models.CharField(max_length=50, default="Mijozlar")
    stat_2_sublabel = models.CharField(max_length=50, default="500+")
    stat_3_label = models.CharField(max_length=50, default="Yutuqlar")
    stat_3_sublabel = models.CharField(max_length=50, default="98%")

    def __str__(self):
        return "Hero Section Sozlamalari"


# 2. ABOUT SECTION
class AboutSection(models.Model):
    badge = models.CharField(max_length=100, default="BIZ HAQIMIZDA")
    title = models.CharField(max_length=200, default="Tajribali Advokatlar Jamoasi")
    # Paragraflarni oddiy text sifatida saqlaymiz (yoki JSONField ishlatsa bo'ladi)
    content = models.TextField(help_text="Paragraflarni yangi qator bilan ajrating")

    # Stats
    experience_value = models.CharField(max_length=50, default="15+")
    experience_label = models.CharField(max_length=50, default="Yillik Tajriba")
    cases_value = models.CharField(max_length=50, default="1000+")
    cases_label = models.CharField(max_length=50, default="Yutuqli Ishlar")
    clients_value = models.CharField(max_length=50, default="500+")
    clients_label = models.CharField(max_length=50, default="Mamnun Mijozlar")
    awards_value = models.CharField(max_length=50, default="25+")
    awards_label = models.CharField(max_length=50, default="Mukofotlar")


# 3. CONTACT & SETTINGS
class ContactSettings(models.Model):
    badge = models.CharField(max_length=100, default="ALOQA")
    title = models.CharField(max_length=200, default="Biz Bilan Bog'laning")
    subtitle = models.CharField(max_length=200, default="Sizga yordam berishga tayyormiz")

    map_url = models.TextField(help_text="Google Maps Embed URL")

    # Ish vaqtlari
    work_days = models.CharField(max_length=100, default="Dushanba - Juma")
    work_hours = models.CharField(max_length=100, default="09:00 - 18:00")
    saturday_text = models.CharField(max_length=100, default="Shanba")
    saturday_hours = models.CharField(max_length=100, default="10:00 - 14:00")
    sunday_text = models.CharField(max_length=100, default="Yakshanba")
    sunday_hours = models.CharField(max_length=100, default="Yopiq")

    def __str__(self):
        return "Aloqa Sozlamalari"

class PracticeArea(models.Model):
    icon = models.CharField(max_length=50, default="Briefcase", help_text="Lucide icon nomi (masalan: Shield, Scale)")
    title = models.CharField(max_length=100)
    description = models.TextField()
    # Mutaxassisliklarni oddiy vergul bilan saqlaymiz
    specialties = models.TextField(help_text="Mutaxassisliklarni vergul bilan ajratib yozing", blank=True)

    def __str__(self):
        return self.title


# 5. CASE STUDIES (Bajarilgan ishlar)
class CaseStudy(models.Model):
    category = models.CharField(max_length=100, default="Yuridik Himoya")
    title = models.CharField(max_length=200)
    description = models.TextField()
    outcome = models.CharField(max_length=200, help_text="Natija (masalan: $2M Undirildi)")
    year = models.CharField(max_length=4, default="2024")

    def __str__(self):
        return self.title


# 6. TESTIMONIALS (Mijozlar fikrlari)
class Testimonial(models.Model):
    quote = models.TextField(verbose_name="Fikr matni")
    author = models.CharField(max_length=100, verbose_name="Mijoz ismi")
    role = models.CharField(max_length=100, verbose_name="Lavozimi/Kompaniyasi")
    # Initials shart emas, ismdan o'zimiz yasab olamiz template-da

    def __str__(self):
        return self.author