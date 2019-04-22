from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from.models import Post
from users.models import CustomUsers
from django.http import HttpResponseRedirect


def home(request):
    context = {
        'posts': Post.objects.filter(is_active=True),
        'users': CustomUsers.objects.filter(is_active=False),
        'unapproved_post': Post.objects.filter(is_active=False)
    }
    return render(request,'member/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'member/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(is_active=True)
    
    def get_context_data(self,**kwargs):
        context = super(PostListView,self).get_context_data(**kwargs)
        context['users'] = CustomUsers.objects.filter(is_active=False)[:5]
        context['unapproved_post'] = Post.objects.filter(is_active=False)[:5]

        return context  

class UserPostListView(ListView):
    model = Post
    template_name = 'member/home.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(CustomUsers, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('date_posted')

    def get_context_data(self,**kwargs):
        context = super(UserPostListView,self).get_context_data(**kwargs)
        context['users'] = CustomUsers.objects.filter(is_active=False)[:5]
        context['unapproved_post'] = Post.objects.filter(is_active=False)[:5]

        return context  


class PostDetailView(DetailView):
    model = Post
   
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form):
        post = form.save(commit = False)
        post.is_active = False
        post.save()
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False    

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False  

# def about(request):
#     return render(request,'member/about.html', {'title': 'About'})    

# def fitness(request):
#     return render(request,'member/fitness.html',{'title': 'Fitness'})    

def approve_user(request, *args, **kwargs):
    user = CustomUsers.objects.get(pk = kwargs.get('pk'))
    user.is_active = True
    user.save()
    return HttpResponseRedirect('/')  

def approve_post(request, *args, **kwargs):
    post = Post.objects.get(pk = kwargs.get('pk'))
    post.is_active = True
    post.save()
    return HttpResponseRedirect('/')  

def allpost(request):
    unapproved_post = Post.objects.filter(is_active=False)
    return render(request,'member/all_post.html', {'title': 'all-post', 'unapproved_post':unapproved_post})    

def allnewmember(request):
    users = CustomUsers.objects.filter(is_active=False)
    return render(request,'member/all_new_member.html',{'title':'all-new-member', 'users':users})