from django.views.generic import FormView, TemplateView

from .forms import SubscribeForm

class SubscribeView(FormView):
    form_class = SubscribeForm
    template_name = 'emails/subscribe.html'
    success_url = '/success/'
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class SuccessView(TemplateView):
    template_name = 'emails/success.html'
