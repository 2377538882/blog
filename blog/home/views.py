from django.shortcuts import render

# Create your views here.

from django.views import View
from home.models import ArticleCategory,Article,Comment
from django.http import HttpResponseNotFound
from django.shortcuts import render,redirect,reverse
from django.core.paginator import Paginator,EmptyPage

class IndexView(View):
    """首页广告"""

    def get(self, request):

        #?cat_id=xxx&page_num=xxx&page_size=xxx
        # cat_id=1&page_size=10&page_num=2
        cat_id=request.GET.get("cat_id",1)

        #print(cat_id)
        page_num = request.GET.get("page_num", 1)
        page_size = request.GET.get("page_size", 10)
        #判断分类id
        try:
            category = ArticleCategory.objects.get(id=cat_id)
            #print(type(cat_id))
        except ArticleCategory.DoesNotExist:
            return HttpResponseNotFound('没有此分类')

        # 获取博客分类信息
        categories = ArticleCategory.objects.all()

        #分页数据
        articles = Article.objects.filter(
            category=category
        )

        # 创建分页器：每页N条记录
        paginator = Paginator(articles, page_size)
        # 获取每页商品数据
        try:
            page_articles = paginator.page(page_num)
        except EmptyPage:
            # 如果没有分页数据，默认给用户404
            return HttpResponseNotFound('empty page')
        # 获取列表页总页数
        total_page = paginator.num_pages

        context = {
            'categories':categories,
            'category':category,
            'articles': page_articles,
            'page_size': page_size,
            'total_page': total_page,
            'page_num': page_num,
            #'cat_id':cat_id
        }

        return render(request, 'index.html',context=context)



"""
    def get(self, request):
        #提供首页广告界面
        #?cat_id=xxx&page_num=xxx&page_size=xxx
        # 1.获取所有分类信息
        categories=ArticleCategory.objects.all()
        # 2.接收用户点击的分类id
        cat_id=request.GET.get('cat_id',1)

        # 3.根据分类id进行分类查询
        try:
            category = ArticleCategory.objects.get(id=cat_id)
        except ArticleCategory.DoesNotExist:
            return HttpResponseNotFound('没有此分类')
        # 4.获取分页参数
        page_num=request.GET.get("page_num",1)
        page_size=request.GET.get("page_size",10) #10默认值
        # 5.根据分类信息查询文章数据
        articles = Article.objects.filter(
            category=category
        )

        # 6.创建分页器：每页N条记录
        paginator = Paginator(articles, page_size)
        # 获取每页商品数据
        try:
            page_articles = paginator.page(page_num)
        except EmptyPage:
            # 如果没有分页数据，默认给用户404
            return HttpResponseNotFound('empty page')
        # 7.获取列表页总页数
        total_page = paginator.num_pages

        context = {
            'categories': categories,
            'category': category,
            'articles': page_articles,
            'page_size': page_size,
            'total _page': total_page,
            'page_num': page_num,
        }
        # 8.组织数据传递给模板
        return render(request, 'index.html',context=context)

"""
class DetailView(View):

    def get(self, request):
        # detail/?id=xxx&page_num=xxx&page_size=xxx
        # 1.获取文档id
        id = request.GET.get('id')


        # 2.获取博客分类信息
        categories = ArticleCategory.objects.all()
        # 3. 根据文章id进行文章数据的查询
        try:
            article = Article.objects.get(id=id)
        except Article.DoesNotExist:
            return render(request, '404.html')
        else:
            article.total_views += 1
            article.save()

        # 获取热点数据,降序，前十名
        hot_articles = Article.objects.order_by('-total_views')[:9]

        # 4.获取分页请求参数
        page_size=request.GET.get("page_size",10)
        page_num=request.GET.get("page_num",1)
        # 5.根据文章信息查询评论数据
        comments = Comment.objects.filter(
            article=article
        ).order_by('-created')
        # 获取评论数
        total_count = comments.count()
        # 6.创建分页器
        paginator = Paginator(comments, page_size)
        # 7.进行分页处理
        try:
            page_comments = paginator.page(page_num)
        except EmptyPage:
            # 如果page_num不正确，默认给用户404
            return HttpResponseNotFound('empty page')
            # 获取列表页总页数
        total_page = paginator.num_pages

        context = {
            'categories': categories,
            'category': article.category,
            'article': article,
            'hot_articles': hot_articles,
            'total_count': total_count,
            'comments': page_comments,
            'page_size': page_size,
            'total_page': total_page,
            'page_num': page_num,
        }

        return render(request, 'detail.html', context=context)

    def post(self, request):
        #1. 先接收用户信息
        user = request.user

        #2. 判断用户是否登录
        if user and user.is_authenticated:
            # 3. 登录用户可以接收form数据
            # 3.1接收评论数据
            id = request.POST.get('id')
            content = request.POST.get('content')

            # 3.2判断文章是否存在
            try:
                article = Article.objects.get(id=id)
            except Article.DoesNotExist:
                return HttpResponseNotFound('没有此文章')

            # 3.3 保存评论数据
            Comment.objects.create(
                content=content,
                article=article,
                user=user
            )
            # 3.4 修改文章评论数量
            article.comments_count += 1
            article.save()
            # 刷新当前页面（重定向），拼接路由
            path = reverse('home:detail') + '?id={}'.format(article.id)
            return redirect(path)
        else:
            # 没有登录则跳转到登录页面
            return redirect(reverse('users:login'))




