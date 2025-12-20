from django.utils.translation import gettext_lazy as _

# Xavfsiz import (agar baza bo'sh bo'lsa xato bermasligi uchun)
try:
    from blog.models import BlogPost

    post_count = BlogPost.objects.count()
except:
    post_count = 0


def dashboard_callback(request, context):
    # 1. Standart ro'yxatni TOZALAYMIZ (Qizil xato chiqmasligi uchun shu kerak)
    context["app_list"] = []

    # 2. O'rtaga o'zimizning statistika va tugmalarni joylaymiz
    context.update({
        "kpi": [
            {
                "title": "Jami Maqolalar",
                "metric": post_count,
                "footer": "Blogdagi postlar soni",
                "icon": "article",
            },
        ],
        "navigation": [
            {
                "title": _("Tezkor Harakatlar"),
                "items": [
                    {
                        "title": _("Yangi Maqola Yozish"),
                        "icon": "edit_note",
                        "link": "/dashboard/blog/new/",
                        "description": "Blog uchun yangi maqola yaratish",
                    },
                    {
                        "title": _("Saytni Ko'rish"),
                        "icon": "public",
                        "link": "/",
                        "description": "Asosiy sahifaga o'tish",
                    },
                    {
                        "title": _("Statistika"),
                        "icon": "bar_chart",
                        "link": "/dashboard/",
                        "description": "To'liq statistikani ko'rish",
                    },
                ],
            },
        ]
    })

    return context