import time

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import Stuff, Bucket, Order, OrderItem
from django.contrib import messages
from .forms import CustomUserCreationForm, StuffForm, RatingForm, FeedBackForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.core.cache import cache
from django.views.decorators.cache import cache_page


def index(request):
    counter = int(request.COOKIES.get('counter', 0)) + 1

    context = {'counter': counter}

    response = render(request, 'index.html', context)

    response.set_cookie(
        'counter',
        counter,
        max_age=10,
        path='/',
        httponly=True
    )

    return response


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Реєстрація успішна! Тепер ви можете увійти!')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def stuff_list(request):
    stuffs = Stuff.objects.all()
    return render(request, 'shop/stuff_list.html', {'stuffs': stuffs})


@login_required
def add_stuff(request):
    if request.method == "POST":
        form = StuffForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Товар успішно додано!')
            return redirect('stuff_list')
    else:
        form = StuffForm()
    return render(request, 'shop/add_stuff.html', {'form': form})


def stuff_detail(request, pk):
    stuff = get_object_or_404(Stuff, pk=pk)
    ratings = stuff.rating.all().order_by('-created_at')
    user_rating = None

    if request.user.is_authenticated:
        user_rating = ratings.filter(user=request.user).first()

    if request.method == "POST" and request.user.is_authenticated:
        form = RatingForm(request.POST, instance=user_rating)
        if form.is_valid():
            new_rating = form.save(commit=False)
            new_rating.stuff = stuff
            new_rating.user = request.user
            new_rating.save()
            messages.success(request, 'Ваш рейтинг додано!')

    else:
        form = RatingForm(instance=user_rating)

    context = {
        'stuff': stuff,
        'rating': ratings,
        'form': form,
        'user_rating': user_rating,
    }

    return render(request, 'shop/stuff_detail.html', context)


def session_demo(request):
    context = {}

    count = request.session.get('view_count', 0)
    count += 1
    request.session['view_count'] = count
    context['view_count'] = count

    if 'flush' in request.GET:
        request.session.flush()
        return redirect('session_demo')

    if 'clear' in request.GET:
        request.session.clear()
        return redirect('session_demo')

    request.session.set_test_cookie()

    if request.session.test_cookie_worked():
        context['test_cookie'] = 'Test cookie is wroking'
        request.session.delete_test_cookie()
    else:
        context['test_cookie'] = 'Cookie dead'

    return render(request, 'shop/session_demo.html', context)


@login_required
def add_to_cart(request, stuff_id):
    stuff = get_object_or_404(Stuff, pk=stuff_id)
    bucket_item, created = Bucket.objects.get_or_create(
        user = request.user,
        stuff = stuff
    )

    if not created:
        bucket_item.count += 1
        bucket_item.save()
    messages.success(request, f'Товар "{stuff.stuff_name}" додано в кошик')
    return redirect('view_cart')


@login_required
def view_cart(request):
    items = Bucket.objects.filter(user=request.user).select_related('stuff')
    total = sum(item.get_total_price() for item in items)
    return render(request, 'shop/cart.html', {'items': items, 'total': total})


@login_required
def remove_from_cart(request, stuff_id):
    bucket_item = get_object_or_404(Bucket, user=request.user, stuff_id=stuff_id)
    bucket_item.delete()
    messages.success(request, 'Товар видалено із кошика')
    return redirect('view_cart')


@login_required
def update_cart(request, stuff_id):
    if request.method == "POST":
        bucket_item = get_object_or_404(Bucket, user=request.user, stuff_id=stuff_id)
        count = request.POST.get('count', '1')

        try:
            count = int(count)
        except (ValueError, TypeError):
            messages.error(request, 'Неправильна кількість')
            return redirect('view_cart')
        
        if count > 0:
            bucket_item.count = count
            bucket_item.save()
            messages.success(request, 'Кількість оновлено')
        elif count == 0:
            bucket_item.delete()
            messages.success(request, 'Товар видалено із кошика!')
        else:
            messages.error(request, 'Кількість не може бути від\'ємною')
    
    return redirect('view_cart')


def send_feedback(request):
    if request.method == "POST":
        form = FeedBackForm(request.POST)
        if form.is_valid():
            subject =  form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = form.cleaned_data['from_email']

            try:
                send_mail(
                    subject=f"[Feedback] {subject}",
                    message=f"[Повідомлення від]: {from_email}\n\n{message}",
                    from_email="jetcraker@ukr.net",
                    recipient_list=["jetcraker@ukr.net"],
                    fail_silently=False,
                    html_message=f'''
                        <div>
                        <p>Повідомлення від <strong>{from_email}</strong></p>
                        <p><strong>Тема:</strong> {subject}</p>
                        <hr>
                        <p>{message}</p>
                        </div>
                    '''
                )
                messages.success(request, 'Ваше повідомлення було надіслано. Дякуємо за ваш відгук!')
                return redirect('stuff_list')
            except BadHeaderError:
                messages.error(request, 'Недопустимий заголовок!')
            except Exception as e:
                messages.error(request, f'Some error: {e}')
        else:
            messages.error(request, 'Перевірте правильність заповнення форми!')
    else:
        form = FeedBackForm()
    return render(request, 'shop/feedback.html', {'form': form})


@login_required
@require_http_methods(['GET'])
def order_history(request):
    user_id = request.user.id
    cache_key = f'order_history_{user_id}'

    data = cache.get(cache_key)

    if not data:
        orders = Order.objects.filter(user_id=user_id).order_by('-created_at')

        data = [{
            "date": order.created_at.strftime('%Y-%m-%d %H:%M'),
            "status": order.status,
            "total": order.total,
            "shipping_address": order.shipping_address,
            "created_at": order.created_at,
            "updated_at": order.updated_at
        } for order in orders
        ]

        cache.set(cache_key, data, timeout=60*10)
    return JsonResponse({'orders': data})


@login_required
@require_http_methods(['GET'])
def order_detail(request, order_id):

    order = get_object_or_404(Order, id=order_id, user=request.user)

    cache_key = f'order_detail_{order_id}'

    data = cache.get_or_set(
        cache_key,
        lambda: {
            "id": order.id,
            "date": order.created_at.strftime("%Y-%m-%d %H:%M"),
            "status": order.status,
            "shipping_address": order.shipping_address,
            "items": [
                {
                    "name": item.stuff.stuff_name,
                    "qty": item.quantity,
                    "price": float(item.price),
                    "total": float(item.get_total_price()),
                }
                for item in order.items.select_related('stuff')
            ],
            "total": float(order.total)
        },
        timeout=60 * 15
    )

    return JsonResponse(data)


@cache_page(60 * 5)
@login_required
def orders_page(request):

    context = {
        "page_title": "Історія замовлень"
    }

    return render(request, 'shop/orders.html', context)


def create_test_order(request):
    if request.user.is_authenticated:
        order = Order.objects.create(
            user=request.user,
            total=299.99,
            status='delivered',
            shipping_address='Some test address'
        )

        stuff_items = Stuff.objects.all()[:3]
        for i, stuff in enumerate(stuff_items, 1):
            OrderItem.objects.create(
                order=order,
                stuff=stuff,
                quantity=i,
                price=stuff.price
            )

        total = sum(item.get_total_price() for item in order.items.all())
        order.total = total
        order.save()

        messages.success(request, f'Тестове замовлення #{order.id} створено')

        cache_key = f'order_history_{request.user.id}'
        cache.delete(cache_key)

    return redirect('orders_page')


def test_orders_api(request):
    return render(request, 'shop/test_orders_api.html')


def ajax_data_view(request):
    if request.method == "GET":
        data = {
            "message": "This is AJAX message",
            "timestamp" : time.time()
        }
        return JsonResponse(data)
    return JsonResponse({"error": "Invalid request"}, status=400)


def ajax_page_view(request):
    return render(request, 'ajax_example.html')