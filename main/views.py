from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile,Post,Like,Followers
# Create your views here.
def index(request):
    all_posts=Post.objects.all()
    user_object=User.objects.get(username=request.user.username)
    user_profile=Profile.objects.get(user=user_object)
    return render(request,'index.html',{'user_profile': user_profile,'all_posts':all_posts})

def signup(request):
    if request.method == "POST":
        #name = request.POST['name']
        #lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            user = User.objects.create_user(username=username,email=email,password=password)
            user.save()
            user_login=auth.authenticate(username=username,password=password)
            auth.login(request,user_login)

            user_model = User.objects.get(username=username)
            newpro = Profile.objects.create(user=user_model,id_user=user_model.id)
            newpro.save()
            return redirect('accounts')
        else:
            messages.info(request,'password does not match!! please try again.')
            return redirect('signup')
    else:
        return render(request,'signup.html')

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user= auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'username or password is incorrect')
            return redirect('signin')

    return render(request,'signin.html')


@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def accounts(request):
    user_profile= Profile.objects.get(user=request.user)
    if request.method == 'POST':
       if request.FILES.get('image')==None:
            image=user_profile.pro_photo
            bio=request.POST['bio']


            user_profile.pro_photo=image
            user_profile.bio=bio
            user_profile.save()
       if request.FILES.get('image') !=None:
            image=request.FILES.get('image')
            bio = request.POST['bio']
            user_profile.pro_photo = image
            user_profile.bio = bio
            user_profile.save()
       return redirect('accounts')



    return render(request,'accounts.html',{'user_profile': user_profile})


@login_required(login_url='signin')
def post(request):
    if request.method=='POST':
        user= request.user.username
        content = request.FILES.get('upload_post')
        captions = request.POST['captions']
        NewPost=Post.objects.create(user=user,content=content,captions=captions)
        NewPost.save()
        return redirect('index')
    else:
        return redirect('index')

@login_required(login_url='signin')
def like(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)
    filtred_likes=Like.objects.filter(post_id=post_id,username=username).first()

    if filtred_likes == None:
        new_like=Like.objects.create(post_id=post_id,username=username)
        new_like.save()
        post.no_likes += 1
        post.save()
        return redirect('index')
    else:
        filtred_likes.delete()
        post.no_likes -=1
        post.save()
        return redirect('index')
def profile(request,pk):
    user_object=User.objects.get(username=pk)
    user_profile=Profile.objects.get(user=user_object)
    user_posts=Post.objects.filter(user=pk)


    context={
        'user_object':user_object,
        'user_profile': user_profile,
        'user_posts':user_posts
    }
    return render(request,'profile.html',context)


def follow(request):
    if request.method =='POST':
        follower=request.POST['follower']
        user = request.POST['user']
        if Followers.objects.filter(follower=follower, user=user).first():
            delete_follower=Followers.objects.get(follower=follower,user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower=Followers.objects.create(follower=follower,user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('index')

def search(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        username_profile_list = []

        username_objects = User.objects.filter(username__icontains=username)

        for user in username_objects:
            profile = Profile.objects.filter(user=user).first()
            if profile:
                username_profile_list.append(profile)

        return render(request, 'search.html', {'username_profile_list': username_profile_list})
    else:
        return render(request, 'search.html')
