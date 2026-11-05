from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from main.models import User, Subtask

class BootstrapFormMixin:
   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, (forms.Select, forms.SelectMultiple)):
                css_class = 'form-select'
            elif isinstance(widget, (forms.CheckboxInput, forms.RadioSelect)):
                css_class = 'form-check-input'
            else:
                css_class = 'form-control'
            existing = widget.attrs.get('class', '')
            widget.attrs['class'] = f'{existing} {css_class}'.strip()


class RegistrationForm(BootstrapFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginForm(BootstrapFormMixin, AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

class SubtaskForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Subtask
        fields = ('title', 'description', 'priority_level', 'dresscode', 'checklist')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
            'checklist': forms.Textarea(attrs={'rows': 3}),
        }