import csv

from django.views.generic import TemplateView, View, ListView, UpdateView, DeleteView, CreateView, FormView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordChangeView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy

from .models import ChatBotSession, ChatBot
from .forms import SignUpForm
#from .utils import generate_ai_response
from .functions import generate_ai_response

class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = SignUpForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)
        
        return super(RegisterView, self).form_valid(form)


def login_page(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f"Welcome {username}!!!")
            return redirect("home")
        else:
            messages.info(request, f"Account does not exist please sign up or check your account details")
    form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})


def logout_page(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("home")


def home(request):
    if request.user.is_authenticated:
        sessions = ChatBotSession.objects.filter(user=request.user).all()
        context = {'sessions': sessions}
        return render(request, 'home.html', context)
    else:
        context = {}
        return render(request, 'home.html', context)


@login_required(login_url="login")
def chatbot_page(request, session_id):
    #check if user is authenticated
    if request.user.is_authenticated:
        session = get_object_or_404(ChatBotSession, id=session_id) 

        if request.method == 'POST':
            #get user input from the form
            user_input = request.POST.get('userInput')
            tone = request.POST.get('tone')
            language = request.POST.get('language')
            bot_response = generate_ai_response(tone, language, user_input)
            
            chatbot = ChatBot.objects.get_or_create(
                chat_session=session,
                message=user_input,
                bot_response=bot_response,
                date=timezone.now(),
            )
            return redirect(request.META['HTTP_REFERER'])
        else:
            #retrieve all messages belong to logged in user
            get_history = ChatBot.objects.filter(user=request.user)
            context = {'get_history':get_history}
            return render(request, 'index.html', context)
    else:
        return redirect("home")
        
def like_message(request):
	pass


def like_view(request, id):
    post = get_object_or_404(ChatBot, id=id)
    liked = False
    if post.feed == True:
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return redirect(request.META.get('HTTP_REFERER', ''))


def export_csv(request, user):
    if request.user.is_authenticated:
        chatbot = ChatBot.objects.filter(user=request.user).all()
        #Create the HttpResponse object with the appropriate CSV header
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="csv_data.csv"'

        writer = csv.writer(response)
        writer.writerow(['chat_session', 'message', 'bot_response', 'feedback', 'date'])

        for record in chatbot:
            writer.writerow([record.chat_session, record.message, record.bot_response, record.feedback, record.date])

        return response
