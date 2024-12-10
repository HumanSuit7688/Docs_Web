from contextlib import nullcontext
from .models import Order


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