from django.shortcuts import render
from django.http import JsonResponse
from django.http.response import HttpResponse, HttpResponseRedirectBase, HttpResponseNotFound, HttpResponseNotAllowed
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Annotation
from django.urls import reverse
from django.db.models import Subquery, OuterRef
from student.models import Enroll, StudentGroup
from teacher.models import Classroom
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
        unit = received_annotation['unit']
        del received_annotation['lesson']
        del received_annotation['unit']
        annotation = Annotation(
            user = req.user, 
            lesson = lesson, 
            unit = unit,
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
            del received_annotation['id']
            del received_annotation['lesson']
            del received_annotation['unit']
            annotation.content = received_annotation
            annotation.save()
            response = HttpResponseSeeOtherRedirect(reverse('annotation_get', args=[annotation.id]))
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
    classid = int(req.GET.get('classID', default=0))            # 班級
    groupid = int(req.GET.get('groupID', default=0))            # 分組設定
    group   = int(req.GET.get('group', default=0))              # 組別
    userid  = int(req.GET.get('userid', default=req.user.id))   # 只取個人
    lesson  = int(req.GET.get('lesson', default=0))             # 課程
    unit    = int(req.GET.get('unit', default=0))               # 單元

    if classid == 0:    # 個人
        stuids = [userid]
    else:               # 同組成員或教師查看班上分組
        stuids = []
        # 該班教師或在指定組別裡的成員才可以查看該分組所有人的標註資料
        if Classroom.objects.filter(id=classid, teacher_id=req.user.id).exists() \
            or StudentGroup.objects.filter(
                    group_id = groupid, 
                    group = group, 
                    enroll_id__in = Enroll.objects.filter(student_id=req.user.id).values_list('id', flat=True)
                ).exists():

            if groupid == 0 or group == 0:
                stuids = Enroll.objects.filter(classroom_id=classid).values_list('student_id', flat=True)
            else:
                stuids = StudentGroup.objects.filter(group_id=groupid, group=group).annotate(
                    stuid = Subquery(
                        Enroll.objects.filter(id=OuterRef('enroll_id')).values('student_id')
                    )
                ).values_list('stuid', flat=True)

    annotations = Annotation.objects.filter(lesson=lesson, unit=unit, user_id__in=stuids).annotate(
                      firstname = Subquery(
                          User.objects.filter(id=OuterRef('user_id')).values('first_name')[:1]
                      )
                  ).exclude(content__text='').order_by('id') # 濾掉空白註記
    total = len(annotations)
    rows = []
    for annotation in annotations:
        content = annotation.content
        content['id'] = annotation.id
        content['created'] = annotation.created
        content['updated'] = annotation.updated
        content['user'] = annotation.firstname
        if 'shapes' in content:
            content['ranges'] = [{'start': '', 'end': '', 'startOffset': 0, 'endOffset': 0}]
        rows.append(content)

    data = {
        "total": total, 
        "rows": rows,
    }
    return JsonResponse(data, safe=False)