from Tools.demo.mcast import receiver
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.urls import reverse
from .forms import Doc1_Form
from .db_funcs import get_order_db, get_all_orders_db, create_order_db, delete_order_db, update_order_status, chek_student, get_all_students
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

    check = chek_student(surname, name)
    print(check)


    # error_text = 'ошибка'
    # redirect_order = reverse('home')
    # return render(request, "order_error.html", {"error_text": error_text, "href": redirect_order})


    if check == True:
        create_order_db(doc_type=1, surname=surname, name=name, patronymic=patronymic, grade_c=grade_c, grade_b=grade_b, email=email)
        return render(request, 'order_success.html')
    else:
        return render(request, 'order_error.html')







@login_required
def secretery(request):
    orders_list = get_all_orders_db()
    # Заголовки таблицы
    orders = ('<tr>'
              '<th>№ Заявки</th>'
              '<th>Тип Справки</th>'
              '<th>Фамилия</th>'
              '<th>Имя</th>'
              '<th>Отчество</th>'
              '<th>Класс</th>'
              '<th>Статус заявки</th>'
              '<th colspan="2">Действия</th>'
              '</tr>')

    for i in orders_list:
        order_id = i.get('id')
        order_type = i.get('doc_type')
        order_surname = i.get('surname')
        order_name = i.get('name')
        order_patronymic = i.get('patronymic')
        order_grade = str(i.get('grade_c')) + i.get('grade_b')
        order_status = i.get('status')

        # если заявка ещё не обработана
        if not order_status:
            status_text = 'Не обработана'
            href = (
                f'<td><a class="btn-accept" href="secсretary/create_documentik/{order_type}/{order_id}">Принять</a></td>'
                f'<td>'
                f'<button type="button" class="reject-btn" '
                f'onclick="confirmAction(\'secсretary/delete_orderik/{order_id}\', '
                f'\'Отклонить заявку №{order_id}?\')">Отклонить</button>'
                f'</td>')
        else:
            status_text = 'Обработана'
            href = (
                f'<td>'
                f'</td>'
                f'<td>'
                f'<button type="button" class="delete-btn" '
                f'onclick="confirmAction(\'secсretary/delete_orderik/{order_id}\', '
                f'\'Удалить заявку №{order_id}?\')">Удалить</button>'
                f'</td>'
            )

        # строка таблицы
        order_tr = (f'<tr>'
                    f'<td>{order_id}</td>'
                    f'<td>{order_type}</td>'
                    f'<td>{order_surname}</td>'
                    f'<td>{order_name}</td>'
                    f'<td>{order_patronymic}</td>'
                    f'<td>{order_grade}</td>'
                    f'<td>{status_text}</td>'
                    f'{href}')

        orders += order_tr

    body_orders = f'<table align="center">{orders}</table>'
    return render(request, 'secretary.html', {"body_orders": body_orders})


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

    send_notification(email, name, surname)

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