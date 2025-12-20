from django.db.models import Avg
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from blog.models import BlogPost, Category
from dashboard.forms import BlogPostForm
from home.models import HeroSection, AboutSection, ContactSettings


# Qo'riqchi: Faqat Staff (Admin) kira oladi
def is_admin(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_admin, login_url='/admin/login/')
def dashboard_home(request):
    posts = BlogPost.objects.all().order_by('-published_date', '-id')

    # O'rtacha o'qish vaqtini hisoblash (bazadagi read_time ustunidan)
    avg_time = posts.aggregate(Avg('read_time'))['read_time__avg']

    # Statistikani hisoblash
    stats = {
        'total_posts': posts.count(),
        'total_views': sum(p.views for p in posts),
        'total_comments': sum(p.comments.count() for p in posts),

        # Agar maqolalar bo'lmasa yoki read_time kiritilmagan bo'lsa 0 bo'ladi,
        # aks holda yaxlitlab (round) chiqaradi.
        'avg_read_time': round(avg_time) if avg_time else 0
    }

    return render(request, 'dashboard/index.html', {'posts': posts, 'stats': stats})


@user_passes_test(is_admin)
def blog_create(request):
    if request.method == 'POST':
        # 1. Formaga hamma ma'lumotni (POST) va rasmlarni (FILES) beramiz
        form = BlogPostForm(request.POST, request.FILES)

        if form.is_valid():
            # 2. Bazaga saqlashga shoshilmaymiz (commit=False)
            post = form.save(commit=False)

            # 3. Avtorni qo'shamiz (chunki formadagi fieldlarda author yo'q)
            post.author = request.user

            # 4. Endi bazaga saqlaymiz
            post.save()

            # 5. Muvaffaqiyat xabari
            messages.success(request, "🎉 Maqola muvaffaqiyatli chop etildi!")
            return redirect('blog_list')
        else:
            # Agar xato bo'lsa
            messages.error(request, "Xatolik bor! Iltimos maydonlarni tekshiring.")
            # Xatolarni terminalda ko'rish uchun (debug):
            print(form.errors)
    else:
        # GET so'rov bo'lsa bo'sh forma ochamiz
        form = BlogPostForm()

    # Formani templatega yuboramiz
    return render(request, 'dashboard/blog_editor.html', {
        'form': form
    })


# dashboard/views.py

@user_passes_test(is_admin)
def blog_edit(request, post_uuid):
    post = get_object_or_404(BlogPost, uuid=post_uuid)

    # MUHIM: request.FILES ni qo'shdik (Rasm ishlashi uchun)
    form = BlogPostForm(request.POST or None, request.FILES or None, instance=post)

    if request.method == 'POST':
        if form.is_valid():
            # 2-MUAMMO YECHIMI: O'zgarish borligini tekshiramiz
            if form.has_changed():
                post = form.save(commit=False)
                # Agar kerak bo'lsa qo'shimcha logic shu yerda
                post.save()
                messages.success(request, "🎉 Maqola muvaffaqiyatli yangilandi!")
            else:
                # Agar hech narsa o'zgarmagan bo'lsa
                messages.info(request, "Hech qanday o'zgarish qilinmadi.")

            return redirect('dashboard_home')
        else:
            messages.error(request, "Xatolik! Formani tekshiring.")

    # Agar modelda category bo'lsa, form o'zi oladi, alohida context shart emas aslida
    # lekin dizayningizda ishlatayotgan bo'lsangiz turaversin
    categories = Category.objects.all()

    return render(request, 'dashboard/blog_editor.html', {
        'post': post,
        'categories': categories,
        'form': form
    })


@user_passes_test(is_admin)
def blog_delete(request, post_uuid):
    if request.method == 'POST':
        # Maqolani topamiz va o'chiramiz
        post = get_object_or_404(BlogPost, uuid=post_uuid)
        post.delete()

        # Muvaffaqiyatli xabar qo'shamiz
        messages.success(request, "Maqola muvaffaqiyatli o'chirildi!")

    return redirect('dashboard_home')
