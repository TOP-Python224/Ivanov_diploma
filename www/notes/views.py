from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView 
from django.contrib.auth import logout, login
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from models.models import Articles, Comments
from .forms import ArticlesForm, RegisterViewForm, CommentsForm, FeedbackForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from django.contrib.sites.shortcuts import get_current_site 
from django.template.loader import render_to_string 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage, EmailMultiAlternatives
from .token import account_activation_token 
from django.contrib.auth import get_user_model
from config.settings import EMAIL_HOST_USER

def index(request, cats: str=None):
    context = {
        'cats' : cats,
    }
    return render(request, 'notes/index.html', context)

def about(request, slug_name : str):
    articles = get_object_or_404(Articles, slug=slug_name, is_published=True)
    commert = Comments.objects.filter(articl=articles.pk).order_by('-create_data')
    if request.method == 'POST':
        form = CommentsForm(request.POST)
        if form.is_valid():
            comm = Comments(text=request.POST['text'], articl=articles, author=request.user)
            comm.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = CommentsForm(initial=({'author': request.user}))
    return render(request, 'notes/about.html', {'articles' : articles, 'form' : form, 'comment' : commert})

@login_required
def add_an_article(request):
    if request.method == 'POST':
        print(request.FILES)
        form = ArticlesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ArticlesForm(initial={'author' : request.user.pk})
    return render(request, 'notes/add.html', {'form' : form})

@login_required
def my_page(request):
    user_id = request.user.pk
    artic = Articles.objects.filter(author=user_id)
    return render(request, 'notes/my_page.html', {'artic' : artic})



class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'notes/login.html'

    def get_success_url(self):
        return reverse_lazy('home')
    
def logout_user(request):
    logout(request)
    return redirect('login')

def csrf_failure(request, reason=""):
    ctx = {'message': 'Попробуйте еще раз'}
    return render(request, 'notes/csrf_error.html', ctx)

def delete_aricles(request, id):
    Articles.objects.filter(pk=id).delete()
    return redirect('my_page')

def del_com(request, id):
    Comments.objects.filter(id=id).delete()
    if request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect('home')

def correct(request, id):
    artc = Articles.objects.get(pk=id)
    if request.method == 'POST':
        print(request.FILES)
        form = ArticlesForm(request.POST, request.FILES, instance=artc)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ArticlesForm(instance=artc)
    return render(request, 'notes/correction.html', {'form' : form, 'id' : id})

def activate(request, uidb64, token): 
    User = get_user_model() 
    try: 
        uid = force_str(urlsafe_base64_decode(uidb64)) 
        user = User.objects.get(pk=uid) 
    except(TypeError, ValueError, OverflowError, User.DoesNotExist): 
        user = None 
    if user is not None and account_activation_token.check_token(user, token): 
        user.is_active = True 
        user.save() 
        login(request, user)
        return redirect('home')
    else: 
        return HttpResponse('Ссылка для активации недействительна!') 
    
def signup(request): 
        if request.method == 'POST': 
            form = RegisterViewForm(request.POST) 
            if form.is_valid(): 
                user = form.save(commit=False) 
                user.is_active = False 
                user.save() 
                current_site = get_current_site(request) 
                mail_subject = 'Ссылка для активации была отправлена на ваш электронный адрес' 
                message = render_to_string('notes/acc_active_email.html', { 
                    'user': user, 
                    'domain': current_site.domain, 
                    'uidb64':urlsafe_base64_encode(force_bytes(user.pk)), 
                    'token':account_activation_token.make_token(user), 
                }) 
                to_email = form.cleaned_data.get('email') 
                email = EmailMessage( 
                            mail_subject, message, to=[to_email] 
                ) 
                email.send() 
                return render(request, 'notes/activate.html')
        else: 
            form = RegisterViewForm() 
        return render(request, 'notes/registration.html', {'form': form}) 

def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.email = request.user.email
            data = {
                 'text' : form.cleaned_data['text'],
                'title' : form.cleaned_data['title'],
                'email' : form.email,
            }
            html_body = render_to_string('notes/email.html', data)
            msg = EmailMultiAlternatives(subject='Обращение', to=[EMAIL_HOST_USER,])
            msg.attach_alternative(html_body, 'text/html')
            msg.send()
            return render(request, 'notes/mes.html')
    else:
        form = FeedbackForm()
    return render(request, 'notes/feedback.html', {'form' : form})



 







