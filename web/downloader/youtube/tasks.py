from __future__ import absolute_import, unicode_literals
from celery import shared_task
import logging
import youtube_dl
from downloader.youtube.models import UserRequests
import os
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)


def my_hook(d):
    if d['status'] == 'finished':
        file_tuple = os.path.split(os.path.abspath(d['filename']))
        print("Done downloading {}".format(file_tuple[1]))
    if d['status'] == 'downloading':
        print(d['filename'], d['_percent_str'], d['_eta_str'])


@shared_task
def extract_mp3(url, email):
    with youtube_dl.YoutubeDL() as ydl:
        info_dict = ydl.extract_info(url, download=False)
    if info_dict:
        formats = info_dict['formats'][0]
        video_title = info_dict.get('title')
        video_size = formats.get('filesize')
        video_url = formats.get('url')
        UserRequests.objects.create(
            url=url,
            title=video_title,
            size=video_size,
            email=email,
            download_url=video_url)

        send_email.delay()


@shared_task
def send_email(email, video_title, video_url):
    subject = 'Download ' + video_title
    message = video_url
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email,]

    send_mail(subject, message, email_from, recipient_list)
