import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GoITeens.settings')
django.setup()


from Market.models import Rubric, GoITeen, Spare, Machine, Product2, Order2


def create_records():

    r1 = Rubric()
    r1.name = 'Vacuum Mega '
    r1.save()
    print('Rubric created successfully: ', r1)

    r2 = Rubric(name='Cleaner Mega ')
    r2.save()
    print('Rubric created successfully: ', r2)

    r3 = Rubric.objects.create(name='Spray Mega')
    print('Rubric created successfully: ', r3)


def update_records():
    rubric = Rubric.objects.first()
    if not rubric:
        rubric = Rubric.objects.create(name='Default Mega rubric')

    goi, created = GoITeen.objects.get_or_create(
        title='Title Mega ',
        defaults={'content': 'initial content', "price": 10, 'rubric': rubric}
    )
    print('Перед оновленням: ', goi.title, goi.content, goi.price)

    goi.title = 'New title Mega '
    goi.content = 'New content Mega '
    goi.price = 1000
    goi.save()


def get_update_or_create():
    rubric_obj, created = Rubric.objects.get_or_create(name='Unique Mega rubric')
    print('get_or_create: Rubric = ', rubric_obj.name, "Create = ", created)

    rubric_obj, created = Rubric.objects.update_or_create(
        name='Flowers Mega',
        defaults={'name': 'Plants Mega'}
    )

    print('update_or_create: Rubric = ', rubric_obj, 'Update = ', created)


def bulk_operations():

    rubric, _ = Rubric.objects.get_or_create(name='Bulk  Mega rubric')

    new_goiteens = [
        GoITeen(title='Bulk Title 1', content='Content 1', price=60, rubric=rubric),
        GoITeen(title='Bulk Title 2', content='Content 2', price=20, rubric=rubric),
        GoITeen(title='Bulk Title 3', content='Content 3', price=90, rubric=rubric),
        GoITeen(title='Bulk Title 4', content='Content 4', price=440, rubric=rubric)
    ]

    GoITeen.objects.bulk_create(new_goiteens)

    goiteens = list(GoITeen.objects.filter(title__startswith='Bulk  Mega Title'))
    for goi in goiteens:
        goi.price += 10

    GoITeen.objects.bulk_update(goiteens, ['price'])
    print('Bulk Updated (Price) ')

    for goi in goiteens:
        print(goi.title, 'Новий price= ', goi.price)


def m2m_operations():
    spare1 = Spare.objects.create(name='Bolt')
    spare2 = Spare.objects.create(name='Crew')
    spare3 = Spare.objects.create(name='Hummer')

    machine = Machine.objects.create(name='Initial Machine')

    machine.spares.add(spare1, spare2)
    print('Після add(): ', list(machine.spares.all()))

    machine.spares.set([spare2, spare3])
    print('Після set(): ', list(machine.spares.all()))

    machine.spares.remove(spare2)
    print('Після remove(): ', list(machine.spares.all()))

    machine.spares.clear()
    print('Після clear(): ', list(machine.spares.all()))


# if __name__ == '__main__':
#     print('Демонстрація створення записів:')
#     create_records()
#
#     print('\nДемонстрація оновлення записів GoiTeen:')
#     update_records()
#
#     print('\nДемонстрація get_or_create: ')
#     get_update_or_create()
#
#     print('\nДемонстрація bulk_operations')
#     bulk_operations()
#
#     print('\nДемонстрація m2m_operations')
#     m2m_operations()

# rubrics = Rubric.objects.all()
#
# for rubric in rubrics:
#     print(rubric.name, end='\n')
#
# print('---')
#
# goiteen = GoITeen.objects.get(pk=1)
# goiteen2 = GoITeen.objects.get(title='Updated Title')
# print(goiteen.title, end='\n')
# print(goiteen2.title, end='\n')
#
# print('---')
#
# rubric_ordered = Rubric.objects.order_by('name')
# for rubric in rubric_ordered:
#     print(rubric.name, end='\n')
#
# print('---')
#
# goiteens = GoITeen.objects.order_by('rubric__name', 'price')
# for goi in goiteens:
#     print(goi.title, end='\n')


def create_tests_data():
    for i in range(1, 6):
        product = Product2.objects.create(
            name=f"Product {i}",
            description=f"Description for Product {i}",
            price=10 * i
        )
        for j in range(1, 4):
            Order2.objects.create(
                product=product,
                quantity=j,
                status='completed'
            )


create_tests_data()
