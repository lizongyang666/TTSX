from django.shortcuts import render
from django.views.generic import View

# Create your views here.


def register(request):
    """注册"""
    if request.method == "GET":
        return render(request, "register.html")
    else:
        # poss  接收表单数据
        pass


# 类视图
class RegisterView(View):
    """注册类视图"""
    # def get(self, request):
        # """对应get请求方式的逻辑"""
        # return render(request, "register.html")


    def post(self, request):
        """对应get请求方式的逻辑"""
        # 获取参数
        # 用户名、密码、确认密码、邮箱、是否同意协议


        # 校验参数

        # 逻辑判断

        # all处理所有的元素，只有所有元素都为真，all函数才会返回真。

        # 判断两次密码是否一致

        # 判断邮箱格式是否正确

        # 判断是否勾选了协议

        # 业务处理

        # 保存数据到数据库中
        # creat_user 方法是django用户认证系统提供的，
        # 并帮助我们加密密码并保存到数据库中

        


