from django.shortcuts import render, redirect
from downloader.youtube.forms import DownloadForm
from downloader.youtube.tasks import extract_mp3


def link_enter_page(request):
    form = DownloadForm(None or request.POST)
    if request.method == 'POST':
        if form.is_valid():
            extract_mp3.delay(
                form.cleaned_data['url'],
                form.cleaned_data['email'])
            return redirect('success')
    return render(request, 'youtube/link_enter.html', {})


def success_page(request):
    return render(request, 'youtube/success.html', {})
