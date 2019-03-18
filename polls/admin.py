from django.contrib import admin
from .models import Question, Choice

'''
    在这里注册模型 添加应用功能
'''
# TabularInline 表格样式
# StackedInline 堆放样式
class ChoiceInline(admin.TabularInline):
    # 指定模型
    model = Choice
    # 默认提供三个字段
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    '''
        修改admin中 默认的模样
    '''
    # fields 显示指定的字段 多个时候指定顺序
    # fieldsets 属性，元组中的第一个元素是字段集的标题
    # 添加数据时的样式
    fieldsets = [
        (None,
            {'fields': ['question_text']}
         ),
        ('日期信息',
            {
                'fields': ['pub_date'],
                'classes': ['collapse'] # 添加显示和影藏
            }
         )
    ]
    # 多表呈显示时的样式
    list_display = ('question_text','pub_date', 'was_published_recently',)
    inlines = [ChoiceInline]
    # 添加一个过滤器 
    list_filter= ['pub_date']
    # 添加一个顶部搜索框 根据填入的字段进行搜索
    search_fields = ['question_text']

# 注册功能
admin.site.register(Question, QuestionAdmin)
# https://docs.djangoproject.com/zh-hans/2.1/intro/tutorial07/