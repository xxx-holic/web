from django.core.mail import send_mail
from django.conf import settings
from celery import task
@task
def sendmail(user):
    msg='<a href="http://127.0.0.1:8000/user/active/?uid=%d">点击激活</a>'%user.id
    send_mail('激活账户','',settings.EMAIL_FROM,[user.email],html_message=msg)


