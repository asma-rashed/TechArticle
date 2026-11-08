from django.shortcuts import get_object_or_404, render,redirect
from django.contrib import messages
from .models import *
import bcrypt
from django.urls import reverse

def login_needed(view):
    def wrapper(request, *args, **kwargs):
        if 'loginID' not in request.session:
            messages.error(request, "يجب عليك تسجيل الدخول اولا")
            return redirect('/index')
        return view(request, *args, **kwargs)
    return wrapper

# Create your views here.
def towelcome(request):
    return redirect("/welcome")
def index(request):
    return render(request,"index.html")
def welcome(request):
    return render(request,"welcome.html")

def register(request):
    if request.method == "POST":
    #check for errors
        errors=Users.objects.validatorRe(request.POST)
        if len(errors) > 0:
            for key ,value in errors.items():
                messages.error(request,value)
            return redirect("/index") # idf ther is any error redirect me to the registeraion forms page
        
        else:
            First_Name=request.POST['First_Name']
            Last_Name=request.POST['Last_Name']
            Email=request.POST['Email']
            Password=request.POST['Password']
            #use "bcrypt" to hash password
            pwHash=bcrypt.hashpw(Password.encode(),bcrypt.gensalt()).decode()

            #create user 
            newUser =Users.objects.create(First_Name=First_Name,Last_Name=Last_Name,Email=Email,Password=pwHash)
            newUser.save()

            #(save user id in session to access to user ) 
            request.session.cycle_key()
            request.session['loginID']=newUser.id
        return redirect("/dashboard")
    else:
        return redirect('/index')


def login(request):
    if request.method == "POST":
        #check for errors 
        errors=Users.objects.validatorLo(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request,value)
            return redirect("/index")
        #fetching for the id to redirect user to success page.
        request.session.cycle_key()
        request.session['loginID'] = Users.objects.get(Email__iexact=request.POST['Email']).id
        return redirect('/dashboard')
    return redirect('/index')

def dashboard(request):
    try:
        id = request.session['loginID']   
    except:
        messages.error(request, "Need to login first")
        return render(request,'dashboard.html')
    context={
    'loginUser':Users.objects.get(id=request.session['loginID']),
    'users':Users.objects.all(),
    'articles':Articles.objects.all().order_by('-createdAt'),
    'tags': Tags.objects.all()
    }
    return render(request,"dashboard.html",context)

def logout (request):
    request.session.pop('loginID', None)
    return redirect('/index')
@login_needed
def adding(request):
    return render(request,"create.html")

@login_needed   
def add_article(request):
    if request.method == 'POST':
        errors =Articles.objects.validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/dashboard')
        else:
            user = Users.objects.get(id=request.session['loginID'])
            title = request.POST['title']
            body = request.POST['body']
            tags = request.POST["tags"]
            tags_list = tags.split(",")
            newArticle =Articles.objects.create(title=title,user=user,body=body)
            for tagName in tags_list:
                tag = Tags.objects.filter(tag_name=tagName)
                if tag.exists():
                    newArticle.tags.add(tag[0])
                else:
                    newTag = Tags.objects.create(tag_name=tagName)
                    newArticle.tags.add(newTag)
            #newArticle.users_wish.add(user) auto make each Article that user create in his/her wish list.
            # newArticle.save()
            messages.success(request,"the Article successfully added!")
            return redirect('/dashboard')
    return redirect('/dashboard')
   

@login_needed
def show_article(request,id):
    # give 404 if the id is wrong or not exist
    article = get_object_or_404(Articles, id=id)
    context = {
        "article": article,
        "user": Users.objects.get(id=request.session['loginID']),
    }
    return render(request, 'article.html', context)

@login_needed
def comment(request):
    if request.method == 'POST':
        article = get_object_or_404(Articles, id=request.POST['msg_id'])
        comment = Comment.objects.create(comment = request.POST['comment'], user_id = Users.objects.get(id = request.session['loginID']), message_id = article)
        # return redirect("/dashboard")
        return redirect(f"/show_article/{article.id}")
    return redirect("/dashboard")

@login_needed
def edit(request,id):#for edit btn 
    article = get_object_or_404(Articles, id=id)
    if article.user_id != request.session['loginID']:
        messages.error(request, "You are not allowed to edit this article.")
        return redirect(f'/show_article/{article.id}')
    context={
        "article":article,
    }

    if request.method == "POST": #check for post method 
        errors = Articles.objects.validator(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request,value)
            return redirect(f'/editarticle/{id}')
        else:
        #if one field changed| no need for change the old value
            article.title= request.POST.get('title') if request.POST.get('title')  else article.title
            article.body=request.POST.get('body') if request.POST.get('body') else article.body
            article.save()
        return redirect(f"/show_article/{article.id}")
    return render(request,'edit.html',context)


@login_needed
def delete(request,id):
    article= get_object_or_404(Articles, id=id)
    if article.user_id != request.session['loginID']:
        messages.error(request, "You are not allowed to delete this article.")
        return redirect(f'/show_article/{article.id}')
    if request.method == "POST":
        article.delete()
    return redirect("/dashboard")

def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        results = Articles.objects.filter(title__contains=searched)
        context={
            'searched' : searched,
            'results': results,
        }
        return render(request,'search.html',context)
    return redirect('/dashboard')

def tag(request,id):
    
    context = {
        "tag": get_object_or_404(Tags, id=id),
        "articles": Articles.objects.exclude(),
        
    }
    return render(request, "tags.html", context)

# def addtag(request,id):
#     if request.method == "POST":
#         tagId=request.post.get("tag")
#         tag=Tags.objects.get(id=int(tagId))
#         article= Articles.objects.get(id=id)
#         article.tags.add(tag)
#         return redirect(f'/article/{id}')

# def addtagspage(request):
#     return render(request,'tags.html')
#----------------likes-------------------------

@login_needed
def like_article(request):
    if request.method == "POST":
        article = get_object_or_404(Articles, id=request.POST.get('article_id'))
        user = Users.objects.get(id=request.session['loginID'])
        if user in article.liked.all():#means the user liked the article already then remove from many to many
            article.liked.remove(user)
        else:
            article.liked.add(user)
        return redirect(f"/show_article/{ article.id}")

    return redirect("/dashboard")
