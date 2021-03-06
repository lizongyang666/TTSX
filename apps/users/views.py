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
from django.contrib.auth import authenticate, login, logout
from utils.commons import LoginRequiredMixin
from .models import Address
from django_redis import get_redis_connection
from goods.models import GoodsSKU


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

    def get(self, request):
        return render(request, "login.html")

        # 登录处理，获取参数

    def post(self, request):
        user_name = request.POST.get("username")
        password = request.POST.get("pwd")
        # 校验参数，判断是否为空
        if not all([user_name, password]):
            return render(request, "login.html", {"errmsg": "用户名或密码不能为空"})

        # 判断是否正确，直接用django的认证系统，不正确返回登录页面
        user = authenticate(username=user_name, password=password)
        if user is None:
            # 认证失败
            return render(request, "login.html", {"errmsg": "用户名或密码错误"})
        # 判断激活状态
        if user.is_active is False:
            return render(request, "login.html", {"errmsg": "用户未激活"})
        # 使用django的认证系统记录用户登录
        login(request, user)
        # 判断用户是否勾选记住登录用户名
        remember = request.POST.get("remember")
        if remember == "on":
            # 表示勾选了记录用户名
            # 设置session有效期, None表示使用django的默认session有效期
            request.session.set_expiry(None)
        else:
            # 表示未勾选，浏览器关闭即失效
            request.session.set_expiry(0)
        # 从查询字符串中尝试获取next的参数
        next = request.GET.get("next")
        if next is None:
            next = reverse("goods:index")
        # 登录成功后定向到主页面
        return redirect(next)


class LogoutView(View):
    """用logout退出登录"""
    def get(self, request):
    # 清除用户的登录数据 session
    # 使用django自带认证系统的退出
        logout(request)

    # 退出后，引导到登录页面
        return redirect(reverse("users:login"))



# 用户地址，提供地址页面数据

# 保存用户地址数据
class AddressView(LoginRequiredMixin, View):
    """用户地址"""
    def get(self, request):
        """提供地址页面数据"""
        # 查询数据库，获取用户的地址信息
        # 当前请求的用户
        user = request.user
        try:
            address = user.address_set.latest("update_time")
        except Address.DoesNotExist:
            # 表示数据库中没有这个用户地址数据
            address = None
        return render(request, "user_center_site.html", {"address": address})

    def post(self, request):
        """保存用户地址数据"""
        user = request.user

        try:
            address = user.address_set.latest("update_time")
        except Address.DoesNotExist:
            # 表示数据库中没有这个用户地址数据
            address = None

        receiver_name = request.POST.get("receiver_name")
        new_detail_address = request.POST.get("address")
        zip_code = request.POST.get("zip_code")
        mobile = request.POST.get("mobile")

        if not all([receiver_name, new_detail_address, zip_code, mobile]):
            return render(request, "user_center_site.html", {"address":address})


        Address.objects.create(
            user=user,
            receiver_name=receiver_name,
            receiver_mobile=mobile,
            detail_addr=new_detail_address,
            zip_code=zip_code
        )

        return redirect(reverse("users:address"))


class UserInfoView(LoginRequiredMixin, View):
    """用户基本信息页面"""
    def get(self, request):
        """提供页面"""
        user = request.user
        # 查看基本信息
        try:
            address = user.address_set.latest("update_time")
        except Address.DoesNotExist:
            # 表示数据库中没有这个用户地址数据
            address = None

        # 查看历史记录， redis
        # 获取django_redis 提供的redis连接对象
        redis_conn = get_redis_connection("default")

        # 浏览历史记录在redis中以列表保存
        redis_key = "history_%s" % user.id
        sku_id_list = redis_conn.lrange(redis_key, 0, 4)

        # 根据sku_id查询商品信息
        # select * from df_goods_sku_where id in (1,2,3,4)
        sku_obj_list = GoodsSKU.objects.filter(id_in=sku_id_list)

        sku_obj_list = []
        for sku_id in sku_id_list:
            sku = GoodsSKU.objects.get(id=sku_id)
            sku_obj_list.append(sku)

        context = {
            "address": address,
            "skus": sku_obj_list
        }
        # 返回
        return render(request, "user_center_info.html", context)