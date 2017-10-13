from django.core.mail import send_mail
from django.template.loader import render_to_string

from django_avancado.settings import MAIL_REPLY


class Mailable:
    def sendMail(self, from_email, to, subject, template, context=None):
        if context is None:
            context = {}
        html = render_to_string(template, context)
        send_mail(
            from_email=from_email,
            recipient_list=(to,),
            subject=subject,
            message=subject,
            html_message=html
        )


class StockGreaterMax(Mailable):
    def __init__(self, product):
        self.product = product

    def send(self, to):
        super().sendMail(
            from_email=MAIL_REPLY,
            to=to,
            subject='Estoque de Produto %s está acima do máximo' % self.product.name,
            template='emails/stock-greater-max.html',
            context={'product': self.product}
        )
