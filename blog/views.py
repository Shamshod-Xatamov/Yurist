from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import BlogPost, Category, Comment


def blog_list(request):
    # 1. Hamma postlarni bazadan olish
    all_posts = BlogPost.objects.all().order_by('-published_date', '-id')

    # 2. Parametrlarni olish
    search_query = request.GET.get('q', '')
    cat_id = request.GET.get('cat', '')

    # 3. Filterlash
    if search_query:
        all_posts = all_posts.filter(
            Q(title__icontains=search_query) |
            Q(excerpt__icontains=search_query)
        )

    if cat_id:
        all_posts = all_posts.filter(category_id=cat_id)

    # 4. ASOSIY MANTIQ SHU YERDA 🔥
    featured_post = None
    # Sahifalash uchun ishlatiladigan ro'yxat (Default: hamma filterlanganlar)
    list_for_pagination = all_posts

    # Agar qidiruv ham, kategoriya filteri ham bo'lmasa - ENG YANGISINI AJRATAMIZ
    if not search_query and not cat_id:
        if all_posts.exists():
            featured_post = all_posts[0]          # Katta karta uchun
            list_for_pagination = all_posts[1:]   # Qolganlari sahifalash uchun
    else:
        # Qidiruv yoki Filter bo'lsa, featured_post None bo'lib qoladi
        list_for_pagination = all_posts

    # 5. PAGINATION (Sahifalash)
    paginator = Paginator(list_for_pagination, 6) # Har sahifada 6 ta post
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 6. CONTEXT
    categories = Category.objects.all()
    context = {
        'posts': page_obj,           # HTMLda posts.paginator... deb ishlatiladi
        'featured_post': featured_post,
        'categories': categories,
        'search_query': search_query,
    }
    return render(request, 'blog/index.html', context)


from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import BlogPost, Comment


def blog_detail(request, post_uuid):
    post = get_object_or_404(BlogPost, uuid=post_uuid)

    # --- VIEWS LOGIC (UNIQUE) ---
    session_key_view = f"viewed_post_{post.uuid}"
    if not request.session.get(session_key_view):
        if not request.user.is_staff:
            post.views += 1
            post.save(update_fields=['views'])
            request.session[session_key_view] = True

    # --- LIKE HOLATINI TEKSHIRISH (YANGI QISM) ---
    # Bu postga ushbu foydalanuvchi like bosganmi?
    session_key_like = f"liked_post_{post.uuid}"
    is_liked = request.session.get(session_key_like, False)

    # --- COMMENTS LOGIC ---
    if request.method == "POST":
        author_name = request.POST.get('author_name')
        content = request.POST.get('content')
        if author_name and content:
            Comment.objects.create(post=post, author_name=author_name, content=content)
            return redirect('blog_detail', post_uuid=post_uuid)

    # Contextga 'is_liked' ni qo'shamiz
    return render(request, 'blog/detail.html', {
        'post': post,
        'is_liked': is_liked
    })


# --- LIKES LOGIC (BAZAGA SAQLASH) ---
def like_post(request, post_uuid):
    if request.method == "POST":
        post = get_object_or_404(BlogPost, uuid=post_uuid)
        session_key = f"liked_post_{post.uuid}"

        if not request.session.get(session_key):
            # Like bosdi
            post.likes += 1
            post.save(update_fields=['likes'])
            request.session[session_key] = True
            return JsonResponse({'likes': post.likes, 'status': 'liked'})
        else:
            # Like qaytarib oldi
            # HIMOYA: Agar like 0 dan katta bo'lsagina ayiramiz
            if post.likes > 0:
                post.likes -= 1
            else:
                post.likes = 0  # Har ehtimolga qarshi

            post.save(update_fields=['likes'])
            del request.session[session_key]
            return JsonResponse({'likes': post.likes, 'status': 'unliked'})

    return JsonResponse({'error': 'Xato so\'rov'}, status=400)