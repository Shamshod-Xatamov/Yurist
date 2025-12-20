from django.contrib import admin
from .models import BlogPost, Category, Comment
from django.contrib import admin
from django.contrib.auth.models import Group, User

# 1. Tepadagi va yon tarafdagi yozuvlarni o'zgartirish
admin.site.site_header = "Shohjahon Abdurahimov"  # Chap tepadagi yozuv
admin.site.site_title = "Boshqaruv Paneli"        # Brauzer tabidagi yozuv
admin.site.index_title = "Xush kelibsiz!"         # Asosiy sahifadagi yozuv

# 2. Groups va Users ni butunlay yashirish
admin.site.unregister(Group)
# admin.site.unregister(User) # Agar o'zingni ham yashirib qo'ysang kiralmay qolasan, ehtiyot bo'l :)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'views', 'published_date')
    search_fields = ('title',)
    list_filter = ('category',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'post', 'date')