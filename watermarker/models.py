from django.db import models


class VideoFile(models.Model):
    WAITING = "WAITING"
    CODING = "CODING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"
    STATUS_CHOICES = (
        (WAITING, "等待转码"),
        (CODING, "转码中"),
        (COMPLETE, "完成"),
        (FAILED, "转码失败")
    )
    vid = models.CharField(max_length=36, unique=True, verbose_name="视频ID")
    filename = models.CharField(max_length=100, verbose_name="文件名")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=WAITING, verbose_name="状态")
    # duration = models.FloatField(verbose_name="时长")

    up_date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def to_dict(self):
        return {
            "vid": self.vid,
            "filename": self.filename,
            "status": self.get_status_display(),
            "up_date": self.up_date.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
            "video_lst": [video.to_dict() for video in self.transcodingvideo_set.all()],
        }


class TranscodingVideo(models.Model):
    clarity = models.PositiveSmallIntegerField(verbose_name="清晰度")
    width = models.PositiveSmallIntegerField(verbose_name="宽")
    height = models.PositiveSmallIntegerField(verbose_name="高")

    video_file = models.ForeignKey(VideoFile, on_delete=models.DO_NOTHING, verbose_name="视频文件")

    path = models.CharField(max_length=150, unique=True, verbose_name="文件路径")

    def to_dict(self):
        return {
            "clarity": self.clarity,
            "width": self.width,
            "height": self.height,
        }
