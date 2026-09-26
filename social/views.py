from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Post, Like, Comment, Follow, Notification


def home(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        content = request.POST.get('content')

        if content:
            Post.objects.create(
                content=content,
                user=request.user
            )

        return redirect('home')

    posts = Post.objects.all().order_by('-created_at')

    if request.user.is_authenticated:
        people = User.objects.exclude(id=request.user.id)

        following_ids = Follow.objects.filter(
            follower=request.user
        ).values_list('following_id', flat=True)
    else:
        people = User.objects.all()
        following_ids = []

    return render(request, 'home.html', {
        'posts': posts,
        'people': people,
        'following_ids': following_ids,
    })


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')


        if username and password:
            User.objects.create_user(
                username=username,
                password=password
            )
            return redirect('login')

    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')


        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'login.html')


def logout_view(request):
  logout(request)
  return redirect('home')


def like_post(request, post_id):
    if not request.user.is_authenticated:
        return redirect('login')

    post = Post.objects.get(id=post_id)

    existing_like = Like.objects.filter(
        user=request.user,
        post=post
    ).first()

    if existing_like:
        existing_like.delete()
    else:
        Like.objects.create(
            user=request.user,
            post=post
        )

        Notification.objects.create(
            user=post.user,
            message=f"{request.user.username} liked your post"
        )

    return redirect('home')




def add_comment(request, post_id):
    if not request.user.is_authenticated:
       return redirect('login')


    post = Post.objects.get(id=post_id)

    if request.method == 'POST':
         content = request.POST.get('comment')

         if content:
            Comment.objects.create(
               user=request.user,
               post=post,
               content=content
            )
            Notification.objects.create(
                 user=post.user, 
                 message=f"{request.user.username} commented on your post" 
            )

    return redirect('home')

def edit_post(request, post_id):
    if not request.user.is_authenticated:
        return redirect('login')

    post = Post.objects.get(id=post_id)

    if post.user != request.user:
        return redirect('home')

    if request.method == 'POST':
        content = request.POST.get('content')

        if content:
            post.content = content
            post.save()

        return redirect('home')

    return render(request, 'edit_post.html', {
        'post': post,
    })


def delete_post(request, post_id):
    if not request.user.is_authenticated:
        return redirect('login')

    post = Post.objects.get(id=post_id)

    if post.user != request.user:
        return redirect('home')

    post.delete()

    return redirect('home')




def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')


    user_posts = Post.objects.filter(
    user=request.user
       ).order_by('-created_at')

    post_count = user_posts.count()
    like_count = Like.objects.filter(
    user=request.user
     ).count()

    return render(request, 'profile.html', {
    'user_posts': user_posts,
    'post_count': post_count,
    'like_count': like_count,
})

def user_profile(request, user_id):
    if not request.user.is_authenticated:
        return redirect('login')

    user = User.objects.get(id=user_id)

    user_posts = Post.objects.filter(
        user=user
    ).order_by('-created_at')

    post_count = user_posts.count()

    follower_count = Follow.objects.filter(
        following=user
    ).count()

    following_count = Follow.objects.filter(
        follower=user
    ).count()

    is_following = Follow.objects.filter(
        follower=request.user,
        following=user
    ).exists()

    return render(request, 'user_profile.html', {
        'profile_user': user,
        'user_posts': user_posts,
        'post_count': post_count,
        'follower_count': follower_count,
        'following_count': following_count,
        'is_following': is_following,
    })



def follow_user(request, user_id):
    if not request.user.is_authenticated:
        return redirect('login')

    user_to_follow = User.objects.get(id=user_id)

    existing_follow = Follow.objects.filter(
        follower=request.user,
        following=user_to_follow
    ).first()

    if existing_follow:
        existing_follow.delete()
    else:
        Follow.objects.create(
            follower=request.user,
            following=user_to_follow
        )

        Notification.objects.create(
            user=user_to_follow,
            message=f"{request.user.username} started following you"
        )

    return redirect('home')

def notifications(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user_notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')


    return render(request, 'notifications.html', {
        'notifications': user_notifications,
    })


def search_users(request):
    if not request.user.is_authenticated:
        return redirect('login')

    query = request.GET.get('q', '')

    users = User.objects.filter(
        username__icontains=query
    ).exclude(
        id=request.user.id
    )

    return render(request, 'search_results.html', {
        'users': users,
        'query': query,
    })


