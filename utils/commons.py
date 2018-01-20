from django.contrib.auth.decorators import login_required

class LoginRequiredMixin(object):
    """定义的类视图扩展类，向类视图中补充验证用户登录的逻辑"""
    @classmethod
    def as_view(cls, *args, **kwargs):
        # super寻找调用类AddressView的下一个父类的as_view()
        view = super(LoginRequiredMixin, cls).as_view(*args, **kwargs)

        # 使用django认证系统提供的装饰器
        # 如果用户未登录，会将用户引导到settings.LOGIN_URL指明的登录页面
        # 如果用户登录，执行视图函数

        view = login_required(view)

        return view

