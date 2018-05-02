from __future__ import absolute_import, unicode_literals
from celery import shared_task
import logging
import youtube_dl
from downloader.youtube.models import UserRequests
import os
from django.core.mail import send_mail
from django.conf import settings
from django.core.files import File

logger = logging.getLogger(__name__)


@shared_task
def extract_mp3(url, email):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'media/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url)
    if info_dict:
        formats = info_dict['formats'][0]
        video_title = info_dict.get('title')
        video_size = formats.get('filesize')
        video_url = formats.get('url')
        ur = UserRequests.objects.create(
            url=url,
            title=video_title,
            size=video_size,
            email=email,
            download_url=video_url)
        ur.media = ydl.download([url])
        ur.save()

        send_email.delay(ur.email, ur.title, ur.media.url)


@shared_task
def send_email(email, video_title, video_url):
    subject = 'Download ' + video_title
    message = video_url
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]

    send_mail(subject, message, email_from, recipient_list)
