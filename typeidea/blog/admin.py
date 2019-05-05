from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import (
    Post,
    Category,
    Tag,
)
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin


class PostInline(admin.TabularInline):
    fields = ('title', 'desc')
    extra = 1
    model = Post


# Register your models here.
@admin.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline]
    # 控制新增Category后显示的字段
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    # 控制页面上需要填写的字段
    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'



@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')


class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器只展示当前用户分类"""
    title = '分类过滤器'
    parameter_name = 'owner_category'  # 查询时url参数的名字：?owner_category=1

    def lookups(self, request, model_admin):
        """返回要展示的内容和查询用的id"""
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        """根据url查询参数的内容返回列表页的数据，self.value()就得到了查询参数的值（1）"""
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    # 编辑页显示的字段，可以修改
    list_display = [
        'title', 'category', 'status',
        'created_time', 'operator', 'owner',
    ]
    list_display_links = []

    list_filter = [CategoryOwnerFilter]
    search_fields = ['title', 'category__name']

    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面
    save_on_top = True  # 是否在页面顶部展示三个按钮

    # 列表页面展示时显示的字段
    # fields = (
    #     ('category', 'title'),  # 这样写，在显示的时候会在同一行
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )

    # 使用fieldsets可以控制页面布局，可以替换fields
    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status',
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            )
        }),
        ('额外信息', {
            'classes': ('collapse', ),
            'fields': ('tag', ),
        })
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id, ))
        )
    operator.short_description = '操作'

    class Media:
        """这个类可以引入静态资源"""
        css = {
            'all': ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css', ),
        }
        js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js', )