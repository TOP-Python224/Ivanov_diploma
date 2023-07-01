from django.contrib.auth.forms import UserCreationForm
from django import forms
from models.models import *


class CommentsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.args = args

    def clean_text(self):
        text = self.cleaned_data['text']
        if len(text) > 200:
            raise forms.ValidationError('Длинна должна быть не более 200 символов')
        return text

    class Meta:
        model = Comments
        fields = ['text']
        widgets = {
            'articl' : forms.HiddenInput,
            'author' : forms.HiddenInput,
            'text' : forms.Textarea(attrs={'cols' : 60, 'rows' : 10}),
        }

class ArticlesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Категория не выбрана'

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise forms.ValidationError('Длинна должна быть не более 50 символов')
        return title

    class Meta:
        model = Articles
        fields = ['title', 'text', 'author', 'slug', 'photo', 'is_published', 'cat']
        widgets = {
            'author' : forms.HiddenInput,
            'title' : forms.TextInput(attrs={'class' : 'form-input'}),
            'content' : forms.Textarea(attrs={'cols' : 60, 'rows' : 10}),
        }


class RegisterViewForm(UserCreationForm):
    username = forms.CharField(label='Логин')
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Пороль 1')
    password2 = forms.CharField(label='Пороль 2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_count = User.objects.filter(email=email).count()
        if user_count != 0:
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class FeedbackForm(forms.Form):
    email = forms.HiddenInput
    title = forms.CharField(label='Тема')
    text = forms.CharField(label='Текст', widget=forms.Textarea)

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise forms.ValidationError('Длинна должна быть не более 50 символов')
        return title
    
    def clean_text(self):
        text = self.cleaned_data['text']
        if len(text) > 500:
            raise forms.ValidationError('Длинна должна быть не более 500 символов')
        return text

    
