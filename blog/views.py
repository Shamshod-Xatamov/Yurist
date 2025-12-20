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
def blog_detail(request, post_uuid):  # pk emas, post_uuid bo'lishi kerak
    # Blog emas, BlogPost bo'lishi kerak. pk=pk emas, uuid=post_uuid bo'lishi kerak
    post = get_object_or_404(BlogPost, uuid=post_uuid)

    # Ko'rishlar sonini oshirish (xohlasangiz qo'shing)
    session_key = f"viewed_article_{post.uuid}"

    # 1. Agar foydalanuvchi bu maqolani oldin ochmagan bo'lsa (sessionda yo'q bo'lsa)
    if not request.session.get(session_key, False):

        # 2. (Ixtiyoriy) Admin yoki o'zingiz kirsangiz sanamasligi uchun:
        # Agar bu qatorni olib tashlasangiz, o'zingiznikini ham sanaydi
        if not request.user.is_staff:
            post.views += 1
            post.save()

            # 3. Sessiyaga "o'qildi" deb yozib qo'yamiz
            request.session[session_key] = True

    if request.method == "POST":
        author_name = request.POST.get('author_name')
        content = request.POST.get('content')

        if author_name and content:
            Comment.objects.create(
                post=post,
                author_name=author_name,
                content=content
            )
            # Redirect qilganda ham post_uuid ni ishlatish kerak
            return redirect('blog_detail', post_uuid=post_uuid)

    return render(request, 'blog/detail.html', {'post': post})