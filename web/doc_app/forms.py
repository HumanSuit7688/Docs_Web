from django import forms
from django.core.validators import RegexValidator
from django.template.defaultfilters import default
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model


class Doc1_Form(forms.Form):
    russian_letters_validator = RegexValidator(
        r'^[А-Яа-яЁёs]+$',  # Разрешаем только русские буквы и пробелы
        'Введите только русские буквы.'
    )

    Surname = forms.CharField(label='Фамилия', max_length=50, validators=[russian_letters_validator], widget=forms.TextInput(attrs={'maxlength': '50'}))
    Name = forms.CharField(label= 'Имя', max_length=50, validators=[russian_letters_validator], widget=forms.TextInput(attrs={'maxlength': '50'}))
    Patronymic = forms.CharField(label='Отчество', max_length=50, validators=[russian_letters_validator], widget=forms.TextInput(attrs={'maxlength': '50'}), required=False)
    Grade_c = forms.ChoiceField(label='Класс (цифра)', choices=((None, None), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11)), initial='')
    Grade_b = forms.ChoiceField(label='Класс (буква)', choices=((None, None), ("А", "А"), ("Б", "Б"), ("В", "В"), ("Г", "Г")), initial='')
    Email = forms.EmailField(label='Электронная почта', required=False)


User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")