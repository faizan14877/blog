from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Contact
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from blog.models import Post
# Create your views here.

#HTML PAGES

def home(request):
    allPost = Post.objects.all()
    context = {'allPost': allPost}

    return render(request, 'home/home.html', context)



def about(request):
    return render(request, 'home/about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        description = request.POST.get('content')
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(description)<4:
            messages.error(request, 'PLease fill the form correctly')
        else:
            contact = Contact(name=name, email=email, phone=phone, description=description)
            contact.save()
            messages.success(request, 'Youe message has been sent successfully')

    return render(request, 'home/contact.html')

def search(request):
    query = request.GET['query']

    if len(query) > 78:
        allPost = []
        messages.warning(request, 'Enter a valid query with chars less than 70')
    elif len(query)==0:
        allPost = []
        messages.warning(request, 'Enter a valid query')
    else:
        allpostTitle = Post.objects.filter(title__icontains=query)
        allpostContent = Post.objects.filter(content__icontains=query)
        allpostAuthor = Post.objects.filter(author__icontains=query)
        allPost = allpostTitle.union(allpostContent, allpostAuthor)

    # if len(allPost) == 0:
    #     messages.warning(request, 'No search results found.')

    context = {'allPost': allPost}
    return render(request, 'home/search.html', context)

# AUTHENTICATIONS APIS

def signUp(request):
    if request.method == 'POST':
        #Get the post parameters
        username = request.POST['username'].lower()
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        #Check the form data
        #username should be under 10 chars
        if len(username) > 10:
            messages.error(request, 'username must be less than 10 chars')
            return redirect('home')

        #username should be alphanumeric
        if not username.isalnum():
            messages.error(request, 'Username should only contain letters and numbers')
            return redirect('home')

        #passwords should match
        if pass1!=pass2:
            messages.error(request, 'Passwords do not match')
            return redirect('home')

        #Create user
        myUser = User.objects.create_user(username, email, pass1)
        myUser.first_name = fname
        myUser.last_name = lname
        print(lname)
        myUser.save()
        messages.success(request, 'Your account has been created.')
        return redirect('home')
    else:
        return HttpResponse('404 -Error')


def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']

        user = authenticate(username=loginusername, password=loginpass)

        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in')
            return redirect('home')
        else:
            message.error(request, 'Invalid credentails')
            return redirect('home')
    else:
        return HttpResponse('404 -Error')

def handleLogout(request):
    logout(request)
    messages.success(request, 'Logged out')
    return redirect('home')

    