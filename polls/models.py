import datetime

from django.db import models
from django.utils import timezone
# 创建模型


class Question(models.Model):
    '''	
            问题类
    '''
    question_text = models.CharField(max_length=200)
    pub_date = models.DateField('date published')

    def __str__(self):
        '''
                可以给命令行中带来方便
        '''
        return self.question_text

    def was_published_recently(self):
        '''
                最近提出的新问题
        '''
        # timezone.now() - datetime.timedelta(days=1) 计算时差 获得昨天日期
        # return self.pub_date >= timezone.now().date() -
        # datetime.timedelta(days=1)
        now = timezone.now().date()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    # 后台显示的样式 只针对定义在模型中的方法

    # 支持查询查找以按相关模型上的值排序。此示例在列表显示中包含“最近提出的新问题”列，并允许按时间对其进行排序
    was_published_recently.admin_oreder_fild = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = '最近出版的'


class Choice(models.Model):
    '''
            选择类
    '''
    Question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


'''
	模型数据库操作
	Question.objects.all() # 全部查询
	Question.objects.filter(id=1) # 条件查询
	Question.objects.get(id=1) # 条件查询
	# 两种方法的区别在于 filter 查询没有的键不会抛异常 而get 会抛出异常
	Question.objects.get(pk=1) # 按主键 查找
	primary key 
	# 获得第一个数据对象
	q = Question.objects.filter(id=1)[0]
	# 修改
	q.question_text = "十万个为什么"
	# 保存
	q.save()
	# 查询全部有关的数据
	q.choice_set.all()
	# 统计有关联数据的个数
	q.choice_set.count()

'''
