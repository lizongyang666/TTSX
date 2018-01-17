from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
import re
from itsdangerous import SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from users.models import User
from celery_task.tasks import send_active_email
from utils import constants
# from django.core.mail import send_mail

# Create your views here.


# def register(request):
#     """注册"""
#     if request.method == "GET":
#         return render(request, "register.html")
#     else:
#         # poss  接收表单数据
#         pass


# 类视图


class RegisterView(View):
    """注册类视图"""
    def get(self, request):
        """对应get请求方式的逻辑"""
        return render(request, "register.html")

    def post(self, request):
        """对应get请求方式的逻辑"""
        # 获取参数
        # 用户名、密码、确认密码、邮箱、是否同意协议
        user_name = request.POST.get("user_name")
        password = request.POST.get("pwd")
        cpwd = request.POST.get("cpwd")
        email = request.POST.get("email")
        allow = request.POST.get("allow")

        # 校验参数

        # 逻辑判断 0 0.0 "" [] () {} None False 都为假
        # all处理所有的元素，只有所有元素都为真，all函数才会返回真。
        if not all([user_name, password, cpwd, email, allow]):
            # 参数不完整
            url = reverse("users:register")
            return redirect(url)
        # 判断两次密码是否一致
        if password != cpwd:
            return render(request, "register.html", {"errmsg": "两次密码不一致"})
        # 判断邮箱格式是否正确
        if not re.match(r"^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$", email):
            return render(request, "register.html", {"errmsg": "邮箱格式不正确"})
        # 判断是否勾选了协议
        if allow != "on":
            return render(request, "register.html", {"errmsg": "请先同意用户协议"})
        # 业务处理

        # 保存数据到数据库中
        # creat_user 方法是django用户认证系统提供的，
        # 并帮助我们加密密码并保存到数据库中
        try:
            user = User.objects.create_user(user_name, email, password)
        except IntegrityError as e:
            # 出异常则表示用户已注册
            return render(request, "register.html", {"errmsg": "用户名已存在"})

        # 更改用户的激活状态，将默认的已激活改为未激活
        user.is_active = False
        user.save()

        # 生成用户激活的身份token （令牌）
        token = user.generate_active_token()

        # 拼接激活的邮件
        active_url = "http://127.0.0.1:8000/users/active/" + token

        # 异步发送邮件 非阻塞
        send_active_email.delay(user_name, active_url, email)

        # 返回值
        return HttpResponse("这是登陆页面")


# 加密计算过程是不能反推的
# 采用签名序列化

class UserActiveView(View):
    """用户激活视图"""
    def get(self, request, user_token):
        """
        用户激活
        :param request:
        :param user_token: 用户激令牌
        :return:
        """

        # 创建转换工具对象（序列化器）
        s = Serializer(settings.SECRET_KEY, constants.USER_ACTIVE_EXPIRES)
        try:
            data = s.loads(user_token)
        except SignatureExpired:
            # 表示token已过期
            return HttpResponse("链接已过期")

        user_id = data.get("user_id")

        # 更新用户的激活状态
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            # 如果不存在，会抛出这个异常
            return HttpResponse('用户不存在')

        user.is_active = True
        user.save()

        return HttpResponse("激活成功，并返回了登陆页面")


class LoginView(View):
   """提供登录页面"""
   
   # 登录处理，获取参数

   # 校验参数，判断是否为空

   # 判断是否正确，直接用django的认证系统，不正确返回登录页面

   # 判断激活状态

   # 使用django的认证系统记录用户登录

   # 判断用户是否勾选记住登录用户名

   # 登录成功后定向到主页面

   # 用logout退出登录，并充定向到主页

   # 用户地址，提供地址页面数据

   # 保存用户地址数据





