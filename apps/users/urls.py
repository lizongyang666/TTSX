from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^register$', views.register, name="register")
    # 使用as_view方法，将类视图转换为函数
    url(r'^register$', views.RegisterView.as_view(), name="register"),
    url(r'^active/(?P<user_token>.+)$', views.UserActiveView.as_view(), name="active"),
    url(r'^login$', views.LoginView.as_view(), name="login"),
    url(r'^logout$', views.LogoutView.as_view(), name="logout"),
    url(r'^address$', views.AddressView.as_view(), name="address"),
]
