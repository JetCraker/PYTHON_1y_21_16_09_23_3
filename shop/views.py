from django.shortcuts import render, redirect, get_object_or_404
from .models import Stuff
from django.contrib import messages
from .forms import CustomUserCreationForm, StuffForm, RatingForm
from django.contrib.auth.decorators import login_required


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
        request.pop('view_count', None)
        return redirect('session_demo')

    request.session.set_test_cookie()

    if request.session.test_cookie_worked():
        context['test_cookie'] = 'Test cookie is wroking'
        request.session.delete_test_cookie()
    else:
        context['test_cookie'] = 'Cookie dead'

    return render(request, 'shop/session_demo.html', context)

