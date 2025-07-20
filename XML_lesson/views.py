import os
from xml.etree import ElementTree
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Student


def import_students(request):
    try:
        xml_path = os.path.join(settings.BASE_DIR, "XML_lesson", 'data', 'students.xml')

        tree = ElementTree.parse(xml_path)
        root = tree.getroot()

        for stu_el in root.findall('student'):
            first = stu_el.find('fist_name').text
            ext_id = stu_el.get('id')
            last = stu_el.find('last_name').text
            enroll_text = stu_el.find('enrollment_date').text
            enrollment_date = enroll_text if enroll_text else None

            Student.objects.update_or_create(
                external_id=ext_id,
                defaults={
                    'first_name': first,
                    'last_name': last,
                    'enrollment_date': enrollment_date
                }
            )

        return HttpResponse("Імпорт студентів пройшов успішно")
    except Exception as e:
        return HttpResponse(e)

def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'student_detail.html', {'student': student})
