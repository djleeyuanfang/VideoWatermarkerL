from __future__ import absolute_import, unicode_literals
from celery import shared_task
import time
import os
import traceback

from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
import numpy as np

from .models import VideoFile, TranscodingVideo


@shared_task
def yunceh():
    print("开始")
    time.sleep(5)
    print("结束")


CLARITY = (360, 480, 720, 1080)
# CLARITY = (360,)


def make_log_image():
    name = "用户Cilicili"
    # 文悦新青年体.otf
    font = ImageFont.truetype("static/font/优设标题黑.ttf", 62)
    w, h = font.getsize(name)
    image = Image.new("RGBA", (w, h))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), name, font=font, fill=(255, 255, 255, 170))

    return image


def make_logo_clip(image, bg_size, duration):
    w, h = image.size
    is_h = bg_size[0] >= bg_size[1]
    if is_h:
        base = bg_size[1] / 1080
    else:
        base = bg_size[0] / 1080
    image = image.resize((int(w * base), int(h * base)))
    pos = bg_size[0] - int(40 * base) - image.width, int(30 * base)
    return ImageClip(np.array(image), duration=duration).set_pos(pos)


@shared_task
def transcoding(filename, vid):
    video_file = VideoFile.objects.get(vid=vid)
    video_file.status = VideoFile.CODING
    video_file.save()

    try:
        v = VideoFileClip(filename)
    except:
        traceback.print_exc()
        # 直接失败
        video_file.status = VideoFile.FAILED
        video_file.save()
        return
    min_size = min(v.h, v.w)
    tran_clarity = []
    for c in CLARITY:
        tran_clarity.append(c)
        if min_size <= c:
            break
    tran_size = []
    if v.h > v.w:
        # 竖版
        for c in tran_clarity:
            tran_size.append((c, int(c * v.h / v.w)))
    else:
        for c in tran_clarity:
            tran_size.append((int(c * v.w / v.h), c))

    logo_image = make_log_image()

    for i in range(len(tran_size)):
        # 看一下有没有转过
        if TranscodingVideo.objects.filter(video_file_id=video_file.id, clarity=tran_clarity[i]):
            continue
        # TODO 要分配好位置，确保空间足够等
        des_filename = os.path.join("videofile", "%s_%d.mp4" % (vid, tran_clarity[i]))
        # 开始转码加水印
        r_v = CompositeVideoClip([
            v.resize(tran_size[i]),
            make_logo_clip(logo_image, tran_size[i], v.duration),
        ], tran_size[i])
        try:
            r_v.write_videofile(des_filename, logger=None)
        except:
            traceback.print_exc()
            # TODO 具体分析一些错误
            # 转码失败
            video_file.status = VideoFile.FAILED
            video_file.save()
            return
        TranscodingVideo.objects.create(video_file_id=video_file.id, clarity=tran_clarity[i], width=tran_size[i][0], height=tran_size[i][1], path=des_filename)
    v.close()

    video_file.status = VideoFile.COMPLETE
    video_file.save()
    os.remove(filename)
