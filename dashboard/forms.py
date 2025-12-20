from django import forms
from blog.models import BlogPost
from django_ckeditor_5.widgets import CKEditor5Widget


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        # Hamma maydonlarni sanab o'tishimiz shart
        fields = ['title', 'excerpt', 'content', 'category', 'read_time', 'tags', 'image']

        widgets = {
            # 1. Kategoriya ko'rinishi uchun (Select):
            'category': forms.Select(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-md bg-white text-gray-900 focus:ring-2 focus:ring-yellow-600 focus:outline-none'
            }),

            # 2. CKEditor ulanishi:
            'content': CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"},
                config_name="extends"
            ),

            # 3. Qolgan maydonlar chiroyli chiqishi uchun klasslar:
            'title': forms.TextInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-md'}),
            'excerpt': forms.Textarea(attrs={'class': 'w-full p-3 border border-gray-300 rounded-md', 'rows': 3}),
            'tags': forms.TextInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-md'}),
            'read_time': forms.NumberInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-md'}),
        }