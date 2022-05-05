from django.contrib import admin
from .models import *


# Register your models here.
class DepartmentAdmin(admin.ModelAdmin):
    # 定制哪些字段需要展示
    list_display = ('id', 'name', 'picture')

    # sortable_by # 排序

    list_editable = ('name', 'picture',)

    list_per_page = 10

    list_max_show_all = 200  # default

    search_fields = ['title']

    # date_hierarchy = 'create_date'

    '''默认空值'''
    empty_value_display = 'NA'

    '''过滤选项'''
    list_filter = ()


class New_memberAdmin(admin.ModelAdmin):
    # 定制哪些字段需要展示
    list_display = ('id', 'name', 'picture')

    # sortable_by # 排序

    list_editable = ('name', 'picture',)

    list_per_page = 10

    list_max_show_all = 200  # default

    search_fields = ['title']

    # date_hierarchy = 'create_date'

    '''默认空值'''
    empty_value_display = 'NA'

    '''过滤选项'''
    list_filter = ()


admin.site.register(Department, DepartmentAdmin)
admin.site.register(NewMember)
# admin.site.register(EmailVerifyRecord)
