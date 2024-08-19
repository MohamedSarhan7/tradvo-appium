from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.utils.translation import gettext_lazy as _

class App(models.Model):
  name = models.CharField(max_length=255)
  uploaded_by =models.ForeignKey(User, related_name='apps', on_delete=models.CASCADE,verbose_name=_("uploaded_by"))
  apk_file_path=models.FileField(verbose_name=_("apk_file_path"), upload_to="media/%Y/%m/%d", max_length=100)
  first_screenshot_path=models.FileField(verbose_name=_("first_screenshot_path"), upload_to="media/%Y/%m/%d", max_length=100,blank=True,null=True)
  second_screenshot_path=models.FileField(verbose_name=_("second_screenshot_path"), upload_to="media/%Y/%m/%d", max_length=100,blank=True,null=True)
  video_recording_path=models.FileField(verbose_name=_("video_recording_path"), upload_to="media/%Y/%m/%d", max_length=100,blank=True,null=True)
  ui_hierarchy = models.CharField(max_length=255,blank=True,null=True)
  screen_changed=models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self) -> str:
    return self.name
  
  