# from django.contrib.auth.views import LoginView
from django.urls import path
from django.contrib.auth import views as auth_views


from . import views
from .views import LoginUser

urlpatterns = [
    path('', views.doc1_page, name = 'home'),
    # path('login', LoginUser.as_view(), name = 'login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('seccretary', views.secretery, name='secretary'),
    path('secсretary/create_documentik/<int:order_type>/<int:order_id>', views.make_doc_procces),
    path('secсretary/delete_orderik/<int:order_id>/', views.delete_order, name = 'secretary/delete_order'),
    path('doc1/process/', views.doc1_form_active, name = 'doc1_process'),
]
