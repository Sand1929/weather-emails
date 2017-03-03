from django import forms
from .models import Subscriber, City

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class SubscribeForm(forms.ModelForm):
    # customize city field
    city = forms.ModelChoiceField(label="Location", queryset=City.objects.all(), empty_label="Where do you live?")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # edit labels
        self.fields['email'].label = "Email Address"

        self.helper = FormHelper(self)
        self.helper.form_id = "subscribe-form"
        
        # add a submit button
        self.helper.layout.append(Submit('subscribe', 'Subscribe'))

    class Meta:
        model = Subscriber
        fields = ['email', 'city']
