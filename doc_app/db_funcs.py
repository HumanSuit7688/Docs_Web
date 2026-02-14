from contextlib import nullcontext
from .models import Order, Student


def get_order_db(id):
    order = Order.objects.get(id=id)
    doc_type = order.doc_type
    surname = order.surname
    name = order.name
    patronymic = order.patronymic
    grade_c = order.grade_c
    grade_b = order.grade_b
    status = order.status
    email = order.email

    dictionary = {'doc_type' : doc_type,
                  'surname' : surname,
                  'name' : name,
                  'patronymic' : patronymic,
                  'grade_c' : grade_c,
                  'grade_b' : grade_b,
                  'email' : email,
                  'status' : status}

    return dictionary


def get_all_orders_db():
    orders_db = Order.objects.all()
    orders_list = []

    for order in orders_db:
        order_dict = {'id': order.id, 'doc_type': order.doc_type,
                      'surname': order.surname, 'name': order.name, 'patronymic': order.patronymic,
                      'grade_c': order.grade_c, 'grade_b': order.grade_b, 'email' : order.email,
                      'status': order.status}
        orders_list.append(order_dict)

    return orders_list


def create_order_db(doc_type, surname, name, patronymic, grade_c, grade_b, email):
    order = Order(doc_type=doc_type, surname=surname, name=name, patronymic=patronymic, grade_c=grade_c, grade_b=grade_b, email=email)
    order.save()


def delete_order_db(id):
    order = Order
    order.objects.get(id=id).delete()


def update_order_status(id):
    order = Order.objects.get(id=id)
    order.status = True
    order.save()


def get_all_students(var):
    students_db = Student.objects.all()
    if var == 'dict':
        students_dict = {}
        for i in students_db:
            students_dict[i.id] = i.fio

        return students_dict

    elif var == 'list':
        students_list = []
        for i in students_db:
            students_list.append(i.fio)

        return students_list

def chek_student(surname, name):
    state = False
    students = get_all_students('list')
    fio = surname + ' ' + name
    for student in students:
        if fio in student:
            state = True
            break

    return state