from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template


class EmailAttachment(object):
    def __init__(self, file_name=None, content=None, mime_type=None):
        self.file_name = file_name
        self.content = content
        self.mime_type = mime_type


def send_contact_mail(name, email, message):
    _send_mail(
        subject='Contact from Hagsteel.com',
        sender=settings.SERVER_EMAIL,
        receiver=settings.SITE_EMAIL_RECIPIENT,
        template_name='contact_form_email',
        context={'name': name, 'email': email, 'message': message},
    )


def _send_mail(**kwargs):
    subject, from_email, to = kwargs.get('subject'), kwargs.get('sender'), kwargs.get('receiver')
    text = get_template('emails/%s.txt' % kwargs.get('template_name'))
    html = get_template('emails/%s.html' % kwargs.get('template_name'))
    context = kwargs.get('context')
    email_context = Context(context)
    text_content = text.render(email_context)
    html_content = html.render(email_context)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    attachments = kwargs.get('attachments')
    if attachments:
        for attachment in attachments:
            msg.attach(attachment.file_name, attachment.content, attachment.mime_type)
    msg.send()
