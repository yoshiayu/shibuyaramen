from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import RamenShop, Review, Likes
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 登録後に自動的にログイン
            return redirect('ramen_app:ramen_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def ramen_list(request):
    query = request.GET.get('q', '')
    if query:
        shops = RamenShop.objects.filter(
            Q(name__icontains=query) |
            Q(category__icontains=query) |
            Q(features__icontains=query)
        )
    else:
        shops = RamenShop.objects.all()
    return render(request, 'ramen_app/ramen_list.html', {'shops': shops, 'query': query})


def ramen_detail(request, shop_id):
    shop = get_object_or_404(RamenShop, id=shop_id)
    is_liked = shop.likes_set.filter(user=request.user).exists() if request.user.is_authenticated else False
    return render(request, 'ramen_app/ramen_detail.html', {'shop': shop, 'is_liked': is_liked})



@login_required
def add_review(request, shop_id):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        # バリデーション
        if not rating or not comment:
            return JsonResponse({'success': False, 'message': '評価とコメントは必須です。'}, status=400)

        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                return JsonResponse({'success': False, 'message': '評価は1から5の間で指定してください。'}, status=400)
        except ValueError:
            return JsonResponse({'success': False, 'message': '評価は数値で指定してください。'}, status=400)

        shop = get_object_or_404(RamenShop, id=shop_id)
        Review.objects.create(
            user=request.user,
            ramen_shop=shop,
            rating=rating,
            comment=comment
        )
        return JsonResponse({'success': True, 'message': 'レビューが投稿されました！'})
    else:
        return JsonResponse({'success': False, 'message': '不正なリクエストです。'}, status=400)


@login_required
def like_shop(request, shop_id):
    shop = get_object_or_404(RamenShop, id=shop_id)
    user = request.user

    if Likes.objects.filter(user=user, ramen_shop=shop).exists():
        Likes.objects.filter(user=user, ramen_shop=shop).delete()
        message = "いいねを解除しました。"
    else:
        Likes.objects.create(user=user, ramen_shop=shop)
        message = "いいねしました！"

    return redirect('ramen_app:ramen_detail', shop_id=shop.id)


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        review.rating = request.POST['rating']
        review.comment = request.POST['comment']
        review.save()
        return redirect('ramen_app:ramen_detail', shop_id=review.ramen_shop.id)
    return render(request, 'ramen_app/edit_review.html', {'review': review})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    shop_id = review.ramen_shop.id
    review.delete()
    return redirect('ramen_app:ramen_detail', shop_id=shop_id)
