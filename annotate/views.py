from django.shortcuts import render
from django.http import JsonResponse
from django.http.response import HttpResponse, HttpResponseRedirectBase, HttpResponseNotFound
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Annotation
from django.urls import reverse
import json

# Create your views here.
class HttpResponseSeeOtherRedirect(HttpResponseRedirectBase):
    status_code = 303

def root(req):
    return JsonResponse({
        "name": "Annotation Store API", 
        "version": "0.1",
    }, safe=False)

def annotations(req):
    if req.method == "POST":
        received_annotation = json.loads(req.body)
        lesson = received_annotation['lesson']
        page = received_annotation['page']
        del received_annotation['lesson']
        del received_annotation['page']
        annotation = Annotation(
            user = req.user, 
            lesson = lesson, 
            page = page, 
            image = received_annotation['img'],
            content = received_annotation,
        )
        annotation.save()
        return HttpResponseSeeOtherRedirect(reverse('annotation_get', args=[annotation.id]))

    # 取得目前使用者所有標註資料。(理論上不會執行到這邊，應該會從 search 取得當前頁面的標註資料)
    annotations = [a for a in Annotation.objects.filter(user=req.user).order_by(id)]
    rows = []
    for annotation in annotations:
        rows.append(json.load(annotation.content))
    return JsonResponse(rows, safe=False)

def get_annotation(req, aid):
    try:
        annotation = Annotation.objects.get(id=aid, user=req.user)
        if req.method == "DELETE":
            result = annotation
            annotation.delete()
            response = HttpResponse(status=204)
        elif req.method == "PUT":   # 修改標註資料
            received_annotation = json.loads(req.body)
            del received_annotation['lesson']
            del received_annotation['page']
            annotation.content = received_annotation
            annotation.save()
            response = HttpResponseSeeOtherRedirect(reverse('annotation_get', args[annotation.id]))
        else:   # GET
            result = annotation.content
            result['id'] = annotation.id
            result['created'] = annotation.created
            result['updated'] = annotation.updated
            response = JsonResponse(result, safe=False)
    except Annotation.DoesNotExist:
        response = HttpResponseNotFound()
    return response

def search(req):
    userid = req.GET.get('userid', default=0)
    image = req.GET.get('img', default='')
    qs = Annotation.objects.filter(image=image)
    if userid == 0:
        pass
    else:
        qs = qs.filter(user__id=userid)
    
    annotations = [a for a in qs.order_by('id')]
    total = len(annotations)
    rows = []
    for annotation in annotations:
        content = annotation.content
        content['id'] = annotation.id
        content['created'] = annotation.created
        content['updated'] = annotation.updated
        if 'shapes' in content:
            content['ranges'] = [{'start': '', 'end': '', 'startOffset': 0, 'endOffset': 0}]
        rows.append(content)
    data = {
        "total": total, 
        "rows": rows,
    }
    return JsonResponse(data, safe=False)