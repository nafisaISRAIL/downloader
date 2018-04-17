from django.shortcuts import render, redirect
import youtube_dl
from downloader.youtube.models import UserRequests
from django.core.mail import send_mail
from django.conf import settings


def link_enter_page(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        email = request.POST.get('email')
        if url:
            with youtube_dl.YoutubeDL() as ydl:
                info_dict = ydl.extract_info(url, download=False)
            if info_dict:
                formats = info_dict['formats'][0]
                video_title = info_dict.get('title')
                video_size = formats.get('filesize')
                vidoe_url = formats['url']
                UserRequests.objects.create(
                    url=url, title=video_title, size=video_size)
                return redirect(vidoe_url)
    return render(request, 'youtube/link_enter.html', {})
