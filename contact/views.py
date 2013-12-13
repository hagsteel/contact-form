from django.core.urlresolvers import reverse
from django.views.generic import FormView
from ..contact.forms import ContactForm


class ContactView(FormView):
    template_name = 'contact/contact_form.html'
    form_class = ContactForm

    def get_success_url(self):
        return reverse('contact_confirmation')

    def form_valid(self, form):
        form.send_email()
        return super(ContactView, self).form_valid(form)

    def get_initial(self):
        initial = super(ContactView, self).get_initial()
        if self.request.user.is_active:
            initial['name'] = '%s %s' % (self.request.user.first_name, self.request.user.last_name)
            initial['email'] = self.request.user.email
        return initial
