from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from blog.models import Post,Comment
from django.views.generic import ListView
from .forms import CommentForm, EmailPostForm
from django.core.mail import send_mail


class PostListView(ListView):
    queryset=Post.published.all()
    context_object_name='posts'
    paginate_by=3
    template_name = "blog/post/list.html"






# Create your views here.


# def post_list(request):
#     object_list = Post.published.all()
#     paginator = Paginator(object_list, 3) # 3 posts in each page
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         # If page is not an integer deliver the first page
#         posts = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range deliver last page of results
#         posts = paginator.page(paginator.num_pages)
#     return render(request,
#                     'blog/post/list.html',
#         {'page': page, 'posts': posts})







def share_post(request,post_id):
#    try:
        post = get_object_or_404(Post,id=post_id,status="publish")
        sent = False
        if request.POST:
            form = EmailPostForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                # sending emails 
                post_url = request.build_absolute_uri(
                   post.get_absolute_url())
                subject = f"{cd['name']} recommends you read " \
                         f"{post.title}"
                message = f"Read {post.title} at {post_url}\n\n" \
                         f"{cd['name']}\'s comments: {cd['comments']}"
                send_mail(subject, message, 'admin@myblog.com',
                         [cd['to']])
                sent = True
        else:
            form = EmailPostForm()

        return render(request, "blog/post/share.html" ,{'form':form,'post':post,'sent':sent})
    # except err



def post_detail(request,year,month,day,post):
    post = get_object_or_404(Post,slug=post,publish__year=year
                                            ,publish__month=month
                                            ,publish__day=day)

    new_comment = None
    comment_form=None
    comments = Comment.objects.filter(active=True)

    if request.method=="POST":
        comment_form=CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post=post
            new_comment.save()
    else:
        comment_form = CommentForm()


    return render(request,"blog/post/detail.html",{'post':post,'new_comment':new_comment,'comments':comments,'comment_form':comment_form})