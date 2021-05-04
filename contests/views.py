from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from pathlib import Path
from django.views.generic.base import View
from .forms import *
from .models import *
from subprocess import *
from users import models as modeluser

def view_contest(request):
    contests = Contest.objects.filter( start__lte=timezone.now() )
    contests2 = Contest.objects.filter(start__gte=timezone.now())
    context = {
        'list_contest': contests,
        'list_contest2': contests2
    }
    return render(request, 'contests/contest.html', context)


def detail(request, contest_id):
    contest = get_object_or_404(Contest, pk=contest_id)
    exercise = contest.exercise_set.all()

    return render(request, "contests/detail.html", {'contest': contest, 'ex': exercise})


def handle_upload_file(file):
    path = Path(__file__)
    root_path = str(path.parent.parent) + '/storage/'
    with open(root_path + str(file), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return solve(root_path + str(file))


def runPy(file):
    s = check_output("python " + file, shell=True)
    return str(s.decode("UTF-8"))


def runC(file):
    s = check_output("gcc " + file + " -o " + "out1" + ";./out1", shell=True)
    return str(s.decode("UTF-8"))


def runCpp(file):
    s = check_output("g++ " + file + " -o " + "out1" + ";./out1", shell=True)
    return str(s.decode("UTF-8"))


def runJava(file):
    s = check_output("javac " + file + ";java " + file, shell=True)
    return str(s.decode("UTF-8"))


def solve(file_name):
    result_answer = ""
    if (file_name.endswith("py")):
        result_answer = runPy(file_name)
    elif (file_name.endswith("c")):
        result_answer = runC(file_name)
    elif (file_name.endswith("cpp")):
        result_answer = runCpp(file_name)
    elif (file_name.endswith("java")):
        result_answer = runJava(file_name)
    return result_answer


def submit_exercise(request, exercise_id):
    form = ExerciseForm()
    exercise = get_object_or_404(Exercise, pk=exercise_id)
    contest_start = exercise.contest.start
    contest_end = exercise.contest.end
    dien_ra = False
    chua_bat_dau = False
    # ket_thuc = False
    if timezone.now() <= contest_end:
        if contest_start <= timezone.now():
            dien_ra = True
        else:
            chua_bat_dau = True
    # else:
    #     ket_thuc = True

    if request.method == "POST":
        print("req", request.FILES.get('file'))
        form = ExerciseForm(request.POST or None, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            instance2 = UserApplyExercise(file=request.FILES.get('file'))
            instance = Exercise(file=request.FILES.get('file'))
            instance2.save()
            instance.save()
            aaa = handle_upload_file(request.FILES.get('file'))
            # print(aaa)
            return HttpResponse("ok")

    form2 = CommentForm()
    dem = exercise.number_of_comments
    if request.method == "POST":
        form2 = CommentForm(request.POST, author=request.user, content=request.POST.get('content'),
                            Exercise_post_connected=exercise)
        if form2.is_valid():
            form2.save()
            # return HttpResponseRedirect(request.path)

    context = {
        'exercise': exercise,
        'q': list(exercise.comments.all())[::-1],
        'form': form,
        'form2': form2,
        'nav': 'job_listing',
        'dem': dem,
        'aaa': 123236,
        'dien_ra': dien_ra,
        'chua_bat_dau': chua_bat_dau,
        # 'ket_thuc': ket_thuc
    }

    return render(request, 'contests/submit_exercise.html', context)


# def submit_exercise(request, exercise_id):
#     aaa = "cdfdf"
#     exercise = get_object_or_404(Exercise, pk=exercise_id)
#     if request.method == 'POST':
#         form = UploadDataTrain(request.POST, request.FILES)
#         if form.is_valid():
#             print("okkkkkkkkkkkk")
#             aaa = handle_upload_file(request.FILES['file'])
#             print(aaa)
#             # return HttpResponseRedirect(request.path)
#     else:
#         form = UploadDataTrain()
#
#     form2 = CommentForm()
#     dem = exercise.number_of_comments
#     if request.method == "POST":
#         form2 = CommentForm(request.POST, author=request.user, content=request.POST.get('content'), Exercise_post_connected=exercise)
#         if form2.is_valid():
#             form2.save()
#             # return HttpResponseRedirect(request.path)
#
#     context = {
#         'exercise': exercise,
#         'q': list(exercise.comments.all())[::-1],
#         'form': form,
#         'form2': form2,
#         'nav': 'job_listing',
#         'dem': dem,
#         'aaa' : aaa
#     }
#
#     return render(request, 'contests/submit_exercise.html', context)

# def create_contest(request):
#     form3 = CreateContestForm()
#     return render(request, 'contests/create_contest.html', {'form3': form3})


class create_contest(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_staff:
                if request.user.is_admin:
                    a = CreateContestForm()
                    return render(request, 'contests/create_contest.html', {'f': a})

        return render(request, 'users/login.html')

    def post(self, request):
        g = CreateContestForm(request.POST)
        if g.is_valid():
            g.save()
            contests = Contest.objects.filter(start__lte=timezone.now())
            contests2 = Contest.objects.filter(start__gte=timezone.now())
            context = {
                'list_contest': contests,
                'list_contest2': contests2
            }
            return render(request, 'contests/contest.html', context)
        else:
            return HttpResponse('Khong duoc validate')
