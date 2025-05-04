from datetime import datetime
from django.db.models import Min, Max, Avg, Count, Sum
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .models import Order2, Product2

def index(request):
    context = {}
    return render(request, 'index.html', context=context)


def current_datetime(request):
    now = datetime.now()
    html = f""" <html>
                    <body>
                        It is the current date and time : {now}
                    </body>
                </html> """
    return HttpResponse(html, status=418)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ви успішно зареєструвались")
            return redirect('index')
        else:
            messages.error(request, "Будь ласка, виправте помилки у формі")
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            messages.success(request, "Ви увійшли в систему!")
            return redirect('index')
        else:
            messages.error(request, "Невірна дані для входу.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {"form": form})


def product_price_stats(request):
    stats = Product2.objects.aggregate(
        min_price=Min('price'),
        max_price=Max('price'),
        avg_price=Avg('price')
    )
    return JsonResponse(stats)


def product_order_stats(request):
    product = Product2.objects.annotate(
        total_orders=Count('orders'),
        total_quantity=Sum('orders__quantity')
    ).values('name', 'total_orders', 'total_quantity')
    return JsonResponse(list(product), safe=False)


def order_summary(request):
    summary = Order2.objects.filter(status='completed').aggregate(
        total_revenue=Sum('product__price'),
        total_orders=Count('id'),
    )
    return JsonResponse(summary)
