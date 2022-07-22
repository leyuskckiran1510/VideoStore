from django.shortcuts import render, redirect, Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from video.models import Video
from video.forms import VideoForm, UserForm
import json
import hashlib
import cv2
import os


def index(request):
    videos = Video.objects.all()
    return render(request, 'video/index.html', {'videos': videos})


def video_check(file):
    """
    Returns the length of the video in seconds.
    referenced from
    site :- stackoverflow.com
    url:- https://stackoverflow.com/questions/3844430/how-to-get-the-duration-of-a-video-in-python/61572332#61572332

    Charges : 5$ for video below 500MB and 12.5$ above 500MB.
    Additional 12.5$ if the video is under 6 minutes 18 second and
    20$ if above 6 minutes 18 seconds.

    """
    cost = 0
    if file.size < 520000000:  # 500MB
        cost += 5
    else:
        cost += 12.5

    with open("./videos/temp.mp4", "wb") as f:
        f.write(file.read())
    video = cv2.VideoCapture("./videos/temp.mp4")
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = video.get(cv2.CAP_PROP_FPS)
    lis = [frame_count / fps, frame_count]
    if lis[0] > 600:
        return {"e": "Video Length Exceeds 10minutes"}
    elif lis[0] < 378:
        cost += 12.5
    elif lis[0] > 378:
        cost += 20
    # remove temp file
    os.remove("./videos/temp.mp4")
    return {"cost": cost}


@login_required
def video_new(request):
    form = VideoForm()
    if request.method == "POST" and request.FILES['file']:
        if request.FILES['file'].size > 1070000000:
            return render(request, 'video/video_new.html', {'form': form, 'error': 'file size is too large.'})
        else:
            res = video_check(request.FILES['file'])
            if 'e' in res.keys():
                form = VideoForm()
                return render(request, 'video/video_new.html', {'form': form, 'error': res['e']})
        if request.FILES['file'].content_type != 'video/mp4':
            return render(request, 'video/video_new.html', {'form': form, 'error': 'file type is not mp4.'})
        request.FILES['file'].name = hashlib.md5(request.FILES['file'].name.encode()
                                                 ).hexdigest() + '.' + request.FILES['file'].name.split('.')[-1]
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            print(request.FILES)
            form.save(request.user)
            return render(request, 'video/video.html', {'form': form, 'success': 'video uploaded successfully.',
                                                        'cost': res['cost']}
                          )

    return render(request, 'video/video.html', {'form': form})


@login_required
def video_list(request):
    if request.method == "GET":
        videos = Video.objects.filter(author=request.user)
    else:
        videos = ""
    return render(request, 'video/video_list.html', {'videos': videos})


@login_required
def video_list_json(request):
    videos = Video.objects.filter(author=request.user)
    if not videos:
        response = {'OOPS': 'NO Videos associated with this user.'}
        return HttpResponse(json.dumps(response), content_type='application/json')
    response = {}
    for n, i in enumerate(videos):
        response[n] = {'year': i.created_at.year,
                       'month': i.created_at.month,
                       'day': i.created_at.day,
                       'filename': i.title,
                       'url': i.file.url}
        print(n, i)
    print(response)
    # returning json response
    return HttpResponse(json.dumps(response), content_type='application/json')


# get object list or 404
def get_object_or_404(model, **kwargs):
    obj = model.objects.filter(**kwargs)
    if not obj:
        raise Http404()
    return obj


# Every USer Get's The list of their videos in JSON
@login_required
def video_dump(request, year=None, month=None, day=None, filename=None):
    user = request.user
    if year and month and day and filename:
        video = get_object_or_404(Video, created_at__year=year, created_at__month=month,
                                  created_at__day=day, filename=filename, author=user)
    elif year and month and day:
        video = get_object_or_404(Video, created_at__year=year, created_at__month=month,
                                  created_at__day=day, author=user)
    elif year and month:
        video = get_object_or_404(Video, created_at__year=year, created_at__month=month, author=user)
    elif year:
        video = get_object_or_404(Video, created_at__year=year, author=user)
    else:
        video = get_object_or_404(Video, filename=filename, author=user)
    response = {}
    for n, i in enumerate(video):
        response[n] = {'year': i.created_at.year,
                       'month': i.created_at.month,
                       'day': i.created_at.day,
                       'filename': i.title,
                       'url': i.file.url}
        print(n, i)
    print(response)
    # returning json response
    return HttpResponse(json.dumps(response), content_type='application/json')


@login_required
def charge(request):
    return render(request, 'video/charge.html')


# signup
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('list')
    else:
        form = UserForm()
    return render(request, 'video/signup.html', {'form': form})


# login and logout using django.contrib.auth
def login_view(request):
    print(request.user.is_authenticated * 10)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('list')
        else:
            return render(request, 'video/login.html', {'error': 'username or password is incorrect.'})
    else:
        return render(request, 'video/login.html')


def logout_view(request):
    logout(request)
    return redirect('index')
