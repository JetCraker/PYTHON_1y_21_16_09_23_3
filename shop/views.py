from django.shortcuts import render, redirect, get_object_or_404
from .models import Stuff, Bucket
from django.contrib import messages
from .forms import CustomUserCreationForm, StuffForm, RatingForm, FeedBackForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError


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
    rating = stuff.rating.all().order_by('-created_at')
    user_rating = None

    if request.user.is_authenticated:
        user_rating = rating.filter(user=request.user).first()

    if request.method == "POST" and request.user.is_authenticated:
        form = RatingForm(request.POST, instance=user_rating)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.stuff = stuff
            rating.user = request.user
            rating.save()
            messages.success(request, 'Ваш рейтинг додано!')

    else:
        form = RatingForm(instance=user_rating)

    context = {
        'stuff': stuff,
        'rating': rating,
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