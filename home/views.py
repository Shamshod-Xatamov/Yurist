from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
import requests
import threading  # Sayt qotib qolmasligi uchun
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from dashboard.views import is_admin
from .models import (
    HeroSection, AboutSection, PracticeArea,
    CaseStudy, Testimonial, ContactSettings
)


def send_telegram(name, phone,subject, message):
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID

    if not token or not chat_id:
        return  # Agar sozlamalar yo'q bo'lsa, hech narsa qilma

    # Xabar matnini chiroyli qilish (HTML formatda)
    text = (
        f"🔔 <b>YANGI MUROJAAT</b>\n\n"
        f"👤 <b>Ism:</b> {name}\n"
        f"📞 <b>Tel:</b> {phone}\n"
        f"📌 <b>Mavzu:</b> {subject}\n\n"
        f"📝 <b>Xabar:</b>\n{message}"
    )

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }

    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Telegramga yuborishda xatolik: {e}")


def home(request):
    if request.method == "POST":
        # Formadan ma'lumotlarni olish
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        user_message = request.POST.get('message')

        # Telegramga yuborish (fon rejimida - sayt tez ishlashi uchun)
        if name and phone:
            send_telegram(name, phone, subject,user_message)

            # Saytda yashil xabar chiqarish
            messages.success(request, "So'rovingiz qabul qilindi! Tez orada aloqaga chiqamiz.", extra_tags='frontend')
        else:
            messages.error(request, "Iltimos, ma'lumotlarni to'liq kiriting.", extra_tags='frontend')

        # O'sha joyga (Contact section) qaytarish
        return redirect('/#contact')
    # Singleton modellardan ma'lumot olamiz (birinchisini)
    hero = HeroSection.objects.first()
    about = AboutSection.objects.first()
    contact = ContactSettings.objects.first()

    # Ro'yxatli ma'lumotlarni hammasini olamiz
    services = PracticeArea.objects.all()
    cases = CaseStudy.objects.all()
    testimonials = Testimonial.objects.all()

    # Barchasini qutiga solamiz (Context)
    context = {
        'hero': hero,
        'about': about,
        'contact': contact,
        'services': services,
        'cases': cases,
        'testimonials': testimonials,
    }

    return render(request, 'home/index.html', context)


from django.shortcuts import render, redirect
from django.contrib import messages
from home.models import HeroSection, AboutSection, ContactSettings


@user_passes_test(is_admin)
def content_manager(request):
    # Bazadan ma'lumotlarni olish (yoki yo'q bo'lsa yaratish)
    hero, _ = HeroSection.objects.get_or_create(id=1)
    about, _ = AboutSection.objects.get_or_create(id=1)
    contact, _ = ContactSettings.objects.get_or_create(id=1)

    if request.method == 'POST':
        # --- HERO SECTION SAVE ---
        hero.badge = request.POST.get('hero_badge')
        hero.title = request.POST.get('hero_title')
        hero.description = request.POST.get('hero_description')
        hero.button_text = request.POST.get('hero_button_text')

        # Rasm yuklash (agar yangisi tanlangan bo'lsa)
        if request.FILES.get('hero_image'):
            hero.image = request.FILES.get('hero_image')

        hero.stat_1_label = request.POST.get('stat_1_label')
        hero.stat_1_sublabel = request.POST.get('stat_1_sublabel')
        # ... qolgan statslar ham shu tartibda ...
        hero.save()

        # --- ABOUT SECTION SAVE ---
        about.badge = request.POST.get('about_badge')
        about.title = request.POST.get('about_title')
        about.content = request.POST.get('about_content')
        about.experience_value = request.POST.get('exp_value')
        about.experience_label = request.POST.get('exp_label')
        about.save()

        # --- CONTACT SECTION SAVE ---
        contact.badge = request.POST.get('contact_badge')
        contact.title = request.POST.get('contact_title')
        contact.map_url = request.POST.get('map_url')
        contact.save()

        messages.success(request, "Barcha o'zgarishlar saqlandi!")
        return redirect('content_manager')

    return render(request, 'dashboard/content_manager.html', {
        'hero': hero,
        'about': about,
        'contact': contact
    })