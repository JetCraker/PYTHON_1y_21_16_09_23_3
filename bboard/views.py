from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Bd, Rubric, GoiTeen
from .forms import BbForm
from django.views import View
from django.views.generic import ListView, TemplateView


class BbIndexView(ListView):
    model = Bd
    template_name = 'index.html'
    context_object_name = 'bbs'
    paginate_by = 5
    queryset = Bd.objects.select_related('rubric').all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['selected_rubric'] = None
        return context


class BbByRubricView(ListView):
    model = Bd
    template_name = 'index.html'
    context_object_name = 'bbs'
    paginate_by = 5

    def get_queryset(self):
        self.rubric = get_object_or_404(Rubric, pk=self.kwargs['rubric_id'])
        return Bd.objects.filter(rubric=self.rubric).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['selected_rubric'] = self.rubric
        return context


def add_and_save(request):
    if request.method == "POST":
        form = BbForm(request.POST)
        if form.is_valid():
            obj = form.save()
            return redirect(reverse("bboard:by_rubric", kwargs={"rubric_id": obj.rubric.pk}))
    else:
        form = BbForm()
    return render(request, "create.html", {'form': form})


@login_required
def dashboard(request):
    return HttpResponse(f"Привіт, {request.user.username}")


class HelloView(View):
    def get(self, request):
        return render(request, 'hello.html')

    def post(self, request):
        return redirect('index.html')


class HomePageView(TemplateView):
    template_name = 'index2.html'


class AboutPageView(TemplateView):
    template_name = 'about.html'


class DataPageView(TemplateView):
    template_name = 'data.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = [
            {'name': 'Some name1', 'worth': '324435345'},
            {'name': 'Some name2', 'worth': '436743534'}
        ]
        return context


def goiteen_list_view(request):
    item_list = Bd.objects.all().order_by('-created_at')

    paginator = Paginator('item_list', 2)
    page_num = request.GET.get('page', 1)

    try:
        page = paginator.get_page(page_num)
    except PageNotAnInteger:
        page = paginator.get_page(1)
    except EmptyPage:
        page = paginator.get_page(paginator.num_pages)

    contex = {
        'page': page,
        'GoiTeen': page.object_list
    }

    return render(request, 'item_list.html', contex)
