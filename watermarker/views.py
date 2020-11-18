from django.core.paginator import Paginator
from django.shortcuts import render
from .tasks import transcoding, yunceh
from django.http import JsonResponse, HttpResponse, FileResponse, Http404
import os
import uuid
import json

from .models import *


def json_response(code, msg, **kwargs):
    res = {
        'code': code,
        'msg': msg,
    }
    res.update(kwargs)
    return JsonResponse(res)


def test_task(req):
    yunceh.delay()
    return HttpResponse("成功")


def index(req):
    return render(req, "index.html", {"title": "视频水印转码"})


def search_video(req):
    filter_kwargs = {}
    title = req.GET.get("title", "")
    if title:
        filter_kwargs["title__contains"] = title
        # filter_kwargs["author__contain"] = query
    page_size = int(req.GET.get("page_size", 15))
    page_num = int(req.GET.get("page_num", 1))
    stat_filter = VideoFile.objects.filter(**filter_kwargs).values("id").distinct().order_by("id")
    p = Paginator(stat_filter, page_size)
    page = p.page(page_num)

    res = []
    for stat_dict in page:
        res.append(VideoFile.objects.get(id=stat_dict["id"]).to_dict())
    return json_response(0, "success", data={
        "total": p.count,
        "list": res
    })


def get_video(req):
    vid = req.GET.get("vid")
    if vid:
        clarity = int(req.GET.get("clarity", 360))
        try:
            t_v = TranscodingVideo.objects.get(video_file__vid=vid, clarity=clarity)
        except TranscodingVideo.DoesNotExist:
            return Http404
        if os.path.exists(t_v.path):
            response = FileResponse(open(t_v.path, 'rb'), content_type='video/mp4')
            # if 'Content-Length' not in response:
            #     response['Content-Length'] = os.path.getsize(filename)
            # if 'Content-Range' not in response:
            #     size = int(response['Content-Length'])
            #     response['Content-Range'] = "bytes 0-%d/%d" % (size-1, size)
            return response
    return Http404


def upload_video(req):
    file = req.FILES.get("video", None)
    if file is None:
        return json_response(-1, "文件不存在")
    # 筛选一下format
    video_format = file.name.split(".")[-1].lower()
    vid = str(uuid.uuid4())
    filename = os.path.join("orgvideofile", "%s.%s" % (vid, video_format))
    with open(filename, "wb") as f:
        for chunk in file.chunks():
            f.write(chunk)
    VideoFile.objects.create(vid=vid, filename=file.name)
    transcoding.delay(filename, vid)

    return json_response(0, "success")
