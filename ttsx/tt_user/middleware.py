
#记录当前地址，登录成功后转回这个地址
class LoginUrlMiddleware:
    def process_view(self,request,view_fun,view_args,views_kwargs):
        urls=['/user/register/',
              '/user/register_handle/',
              '/user/register_uname/',
              '/user/active/',
              '/user/login/',
              '/user/login_handle/',
              '/user/logout/',
              '/user/sheng/',
              '/cart/add/'
              ]
        if request.path not in urls:
            request.session['url']=request.get_full_path()

'''
http://www.itcast.cn/python/?a=10
request.path==>/python/
request.getfullpath()==>/python/?a=10

'''

