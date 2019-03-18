# from django.shortcuts import render, get_object_or_404
# from django.http import (
#     HttpResponse,
#     Http404, #
#     HttpResponseRedirect # 重定向
#     )
# from django.template import loader
# from django.urls import reverse

# from .models import Question, Choice


# # 编写视图文件


# def index(request):
#     # 最近添加的列表
#     latest_question_list = Question.objects.order_by('pub_date')
#     # [','.join(q.question_text for q in latest_question_list)]
#     template = loader.get_template('polls/index.html')
#     content = {
#         'latest_question_list': latest_question_list
#     }
#     # return HttpResponse(template.render(content, request))
#     return render(request, 'polls/index.html', content)


# def home(request):
#     return HttpResponse("新主页")


# def datail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})


# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})


# def vote(request, question_id):
#     '''

#     '''
#     question = get_object_or_404(Question, pk=question_id)

#     # import ipdb; ipdb.set_trace()
#     try:
#         # 获取表单参数
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#         # request.POST 的值永远是字符串、
#         # request.GET 用于访问 GET 数据
#     except (KeyError, Choice.DoesNotExist):
#         # 引发异常错误 跳转本页面
#         return render(request, 'polls/detail.html', {
#             'question': question,
#             'error_message': "你还没有选择.",
#         })
#     else:
#         # 这个答案+1 并且重定向到其他页面
#         selected_choice.votes += 1
#         selected_choice.save()
#         # reverse('polls:results', args=(question.id,)) 返回 '/polls/3/results/'
#         # 3 是question.id
# return HttpResponseRedirect(reverse('polls:results',
# args=(question.id,)))


from django.http import HttpResponseRedirect  # 重定向
from django.shortcuts import (
    get_object_or_404,  # 获取对象或者异常
    render  # 渲染
)
from django.urls import reverse  # 反转
from django.views import generic  # 通用类
from django.utils import timezone
# 通用视图 ListView 和 DetailView
# 分别抽象“显示一个对象列表”和“显示一个特定类型对象的详细信息页面”这两种概念
from .models import Choice, Question


class IndexView(generic.ListView):
    '''
        主页
    '''
    # ListView 使用一个叫做 <app name>/<model name>_list.html 的默认模板
    # 使用template_name 属性指定我们的模板 让他不自动生成模板
    template_name = 'polls/index.html'

    # 替换变量名称
    # 自动生成的 context 变量是 question_list
    # 我们提供 context_object_name 属性，表示我们想使用 latest_question_list
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """返回最后发布的五个问题."""
        # 先根据条件查询在进入排序
        return Question.objects.filter(pub_date__lte=timezone.now().date()).order_by('-pub_date')[:5]
        # return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    '''
        详细视图
    '''
    # 通用视图 DetailView 使用一个叫做 <app name>/<model name>_detail.html 的模板

    # question 变量会自动提供—— 因为我们使用 Django 的模型 (Question)
    # Django 能够为 context 变量决定一个合适的名字
    model = Question
    # 使用template_name 属性来指定一个模板名字
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now().date())


class ResultsView(generic.DetailView):
    '''
        数据视图
    '''
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    '''
        投票
    '''
    question = get_object_or_404(Question, pk=question_id)

    # import ipdb; ipdb.set_trace()
    try:
        # 获取表单参数
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        # request.POST 的值永远是字符串、
        # request.GET 用于访问 GET 数据
    except (KeyError, Choice.DoesNotExist):
        # 引发异常错误 跳转本页面
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "你还没有选择.",
        })
    else:
        # 这个答案+1 并且重定向到其他页面
        selected_choice.votes += 1
        selected_choice.save()
        # reverse('polls:results', args=(question.id,)) 返回 '/polls/3/results/'
        # 3 是question.id
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
