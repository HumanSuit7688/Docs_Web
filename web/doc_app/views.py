from Tools.demo.mcast import receiver
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.urls import reverse
from .forms import Doc1_Form
from .db_funcs import get_order_db, get_all_orders_db, create_order_db, delete_order_db, update_order_status
from .microsoft_world import make_doc
import os, datetime
from .models import Order, Student
from .send_email import send_notification


def doc1_page(request):
    userform = Doc1_Form()
    return render(request, "index.html", {"form": userform, "semi_title": "Справка об обучении в Лицее"})


def doc1_form_active(request):
    surname = request.POST.get('Surname')
    name = request.POST.get('Name')
    patronymic = request.POST.get('Patronymic')
    grade_c = request.POST.get('Grade_c')
    grade_b = request.POST.get('Grade_b')
    email = request.POST.get('Email')

    surname = surname.capitalize()
    name = name.capitalize()
    patronymic = patronymic.capitalize()

    print(surname, name, patronymic, grade_c, grade_b, email)
    print(os.listdir())


    create_order_db(doc_type=1, surname=surname, name=name, patronymic=patronymic, grade_c=grade_c, grade_b=grade_b, email=email)


    # error_text = 'ошибка'
    # redirect_order = reverse('home')
    # return render(request, "order_error.html", {"error_text": error_text, "href": redirect_order})

    return render(request, 'order_success.html')

@login_required
def secretery(request):
    orders_list = get_all_orders_db()
    orders = ('<tr> <td><h4>№ Заявки</h4></td>\n'
              '<td><h4>Тип Справки</h4></td>\n'
              '<td><h4>Фамилия</h4></td>\n'
              '<td><h4>Имя</h4></td>\n'
              '<td><h4>Отчество</h4></td>\n'
              '<td><h4>Класс</h4></td>\n'
              '<td><h4>Статус заявки</h4></td>\n'
              '<td><h4>Действие</h4></td>\n'
              '<td><h4>Действие</h4></td>\n </tr>')
    for i in orders_list:
        order_id = i.get('id')
        order_type = i.get('doc_type')
        order_surname = i.get('surname')
        order_name = i.get('name')
        order_patronymic = i.get('patronymic')
        order_grade = str(i.get('grade_c')) + i.get('grade_b')
        order_status = i.get('status')
        color = ''
        if order_status == False:
            order_status = 'Не обработана'
            corol = '"background-color: yellow;"'
            href = f'<td><a href="secсretary/create_documentik/{order_type}/{order_id}">Принять</a></td>\n<td><a href="secсretary/delete_orderik/{order_id}">Отклонить</a></td> </tr>\n'
        else:
            order_status = 'Обработана'
            corol = '"background-color: green;"'
            href = f'<td></td><td><a href="secсretary/delete_orderik/{order_id}">Удалить</a></td> </tr>\n'
        order_tr = f'<tr> <td>{order_id}</td>\n<td>{order_type}</td>\n<td>{order_surname}</td>\n<td>{order_name}</td>\n<td>{order_patronymic}</td>\n<td>{order_grade}</td>\n<td>{order_status}</td>\n'
        order_tr += href
        orders += order_tr
    body_orders = f'<table align=center border="1", style="text-align: center;"> {orders} </table>'

    print(request.user)

    return render(request, 'secretary.html', {"body_orders" : body_orders})


@login_required
def make_doc_procces(request, order_type, order_id):
    order = get_order_db(order_id)
    name = order.get('name')
    surname = order.get('surname')
    patronymic = order.get('patronymic')
    grade_c = order.get('grade_c')
    grade_b = order.get('grade_b')
    email = order.get('email')

    make_doc(surname, name, patronymic, grade_c, grade_b)

    date_now = datetime.date.today()
    day = date_now.strftime('%d')
    month = date_now.strftime('%m')

    file_path = os.path.join('new_docs', f"new_{surname}_{name}_{day}_{month}.docx")
    response = FileResponse(open(file_path, 'rb'), as_attachment=True)

    update_order_status(order_id)

    # send_notification(email, name, surname)

    return response


@login_required
def delete_order(request, order_id):
    delete_order_db(order_id)
    return render(request, 'delete_order.html',
                  {'order_number' : order_id})


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'registration/login'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))