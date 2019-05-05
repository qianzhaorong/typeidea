from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def post_list(request, category_id=None, tag_id=None):
    content = 'post list category={category_id}, tag_id={tag_id}'.format(
        category_id=category_id,
        tag_id=tag_id,
    )
    return HttpResponse(content=content)


def post_detail(request, post_id):
    return HttpResponse('detail')