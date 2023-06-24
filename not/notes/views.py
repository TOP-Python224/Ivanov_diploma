from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView 
from django.contrib.auth import logout, login
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from models.models import Articles, Comments
from .forms import ArticlesForm, RegisterViewForm, CommentsForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

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
            form = CommentsForm()
    else:
        form = CommentsForm(initial=({'author': request.user}))
    return render(request, 'notes/about.html', {'articles' : articles, 'form' : form, 'comment' : commert})

@login_required
def add_an_article(request):
    if request.method == 'POST':
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


class RegisterView(CreateView):
    form_class = RegisterViewForm
    template_name = 'notes/registration.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


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
 







