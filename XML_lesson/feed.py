from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Student

class StudentFeed(Feed):
    title = 'Останні студенти'
    link = '/rss/students/'
    description = 'Нові зарахування'

    def items(self):
        return Student.objects.order_by('enrollment_date')[:5]

    def item_title(self, item):
        return f'{item.first_name} {item.last_name}'

    def item_description(self, item):
        return f'Дата зарахування: {item.enrollment_date}'

    def item_link(self, item):
        return reverse('student_detail', args=[item.pk])
