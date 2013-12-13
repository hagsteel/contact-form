import floppyforms as forms
from ..core import sendmail


class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        if self.initial.get('name'):
            self.fields['name'].widget.attrs['value'] = self.initial['name']
        if self.initial.get('email'):
            self.fields['email'].widget.attrs['value'] = self.initial['email']

        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['message'].widget.attrs['class'] = 'form-control'

    def send_email(self):
        name = self.cleaned_data.get('name')
        email = self.cleaned_data.get('email')
        message = self.cleaned_data.get('message')
        sendmail.send_contact_mail(name, email, message)
