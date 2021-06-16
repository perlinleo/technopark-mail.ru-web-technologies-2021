from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, redirect, reverse
from random import randint
from app.models import Question, Answer, Profile, LikeAnswer, LikeQuestion, Tag
from django.db.models import Count
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from app.forms import *



def getPopularTags():
    popularTags = Tag.objects.order_by('popularity')
    popularTags = popularTags[0:3]
    return popularTags

def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, 5)
    page = request.GET.get('page')
    objects = paginator.get_page(page)

    return objects





def index(request):
    popularTags = getPopularTags()
    questions_page = paginate(Question.objects.all().order_by('-id').annotate(
            answers_amount=Count('answer')
            ), 
            request)
    reacts_page= {}
    liked_questions = {}
    disliked_questions = {}
    try: 
        userProfile = Profile.objects.get(user_id=request.user.id)
    except: 
        userProfile = Profile.objects.get(user_id=1)
    for que in questions_page:
        try:
            rea = LikeQuestion.objects.get(question=que, user=userProfile.id)
            reacts_page[rea.question.id]=rea.opinion
            if(rea.opinion):
                liked_questions[rea.question.id]=True
            else:
                disliked_questions[rea.question.id]=False
        except:
            reacts_page[que.id]="None"

    
    print(reacts_page)
    
    

    return render(request, 'index.html', {
        'liked_questions': liked_questions,
        'disliked_questions': disliked_questions,
        'reacts_page': reacts_page,
        'questions': questions_page,
        'popularTags': popularTags
    })


def hot_questions(request):
        popularTags = getPopularTags()
        questions_page = paginate(
            Question.objects.order_by('-rating').annotate(
                answers_amount=Count('answer')
                ), 
                request)
    
        reacts_page= {}
        liked_questions = {}
        disliked_questions = {}
        try: 
            userProfile = Profile.objects.get(user_id=request.user.id)
        except: 
            userProfile = Profile.objects.get(user_id=1)
        for que in questions_page:
            try:
                rea = LikeQuestion.objects.get(question=que, user=userProfile.id)
                reacts_page[rea.question.id]=rea.opinion
                if(rea.opinion):
                    liked_questions[rea.question.id]=True
                else:
                    disliked_questions[rea.question.id]=False
            except:
                reacts_page[que.id]="None"

        
        print(reacts_page)
        
        

        return render(request, 'hot.html', {
            'liked_questions': liked_questions,
            'disliked_questions': disliked_questions,
            'reacts_page': reacts_page,
            'questions': questions_page,
            'popularTags': popularTags
        })

@login_required
def logout(request):
    django_logout(request)
    previous_page = request.META.get('HTTP_REFERER')
    if previous_page is not None:
        return redirect(previous_page)
    return redirect("/")

def tag_questions(request, name):
    popularTags = getPopularTags()
    questions_page = paginate(Question.objects.filter(tags__name=name).annotate(
            answers_amount=Count('answer')
            ), 
            request)
    reacts_page= {}
    liked_questions = {}
    disliked_questions = {}
    try: 
        userProfile = Profile.objects.get(user_id=request.user.id)
    except: 
        userProfile = Profile.objects.get(user_id=1)
    for que in questions_page:
        try:
            rea = LikeQuestion.objects.get(question=que, user=userProfile.id)
            reacts_page[rea.question.id]=rea.opinion
            if(rea.opinion):
                liked_questions[rea.question.id]=True
            else:
                disliked_questions[rea.question.id]=False
        except:
            reacts_page[que.id]="None"

    
    print(reacts_page)
    
    

    return render(request, 'tag.html', {
        'liked_questions': liked_questions,
        'disliked_questions': disliked_questions,
        'reacts_page': reacts_page,
        'questions': questions_page,
        'popularTags': popularTags
    })


def answers_for_question(request, pk):
    popularTags = getPopularTags()
    current_question = Question.objects.get(id=pk)
    answers_page = paginate(Answer.objects.filter(question=pk).order_by('rating'), request, 5)
        

    if request.method == 'GET':
            form = AnswerForm()
    else:
            if not request.user.is_authenticated:
                return redirect(f"/login/?next={request.get_full_path()}")

            form = AnswerForm(profile_id=request.user.profile.id, question_id=pk, data=request.POST)
            if form.is_valid():
                form.save()
                answers_page = paginate(Answer.objects.filter(question=pk).order_by('rating'), request, 5)
                return redirect(reverse('answers_for_questions', kwargs={'pk': pk}) + f"?page={answers_page.paginator.num_pages}")


    return render(request, 'question.html', {
        'form': form,
        'question': current_question,
        'answers': answers_page,
        'popularTags': popularTags
    })


def login(request):
    if (request.method == 'GET') :
        form = LoginForm()
    else: 
        form = LoginForm(data=request.POST)
        if form.is_valid():
            profile = authenticate(request, **form.cleaned_data)
            if profile is not None:
                django_login(request,profile)
                return redirect(request.POST.get('next','/'))
            else:
                form.add_error("password","Incorrect login or password")
    popularTags = getPopularTags()
    return render(request, 'login.html', {
        'popularTags': popularTags,
        'form': form})
    


def signup(request):
    if request.method == 'GET':
        form = SignupForm()
    else:
        form = SignupForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            user = form.save()
            django_login(request, user)
            return redirect(request.POST.get('next', '/'))
    popularTags = getPopularTags()

    return render(request, 'signup.html', {'popularTags': popularTags, 
    'form': form})

@login_required
def ask(request):
    if request.method == 'GET':
        form = AskForm()
    else:
        form = AskForm(request.user.profile, data=request.POST)
        if form.is_valid():
            question = form.save()
            return redirect(reverse('answers_for_questions', kwargs={'pk': question.pk}))
    popularTags = popularTags = getPopularTags()

    return render(request, 
            'ask.html', {'popularTags': popularTags,
                         'form': form})



@login_required
def settings(request):
    form_updated = False
    if request.method == 'GET':
        form = SettingsForm(initial={'username': request.user.username, 'email': request.user.email})
        profile_picture = ImageForm()
    else:
        form = SettingsForm(user=request.user, data=request.POST)
        profile_picture = ImageForm(data=request.POST, files=request.FILES, instance=request.user.profile)
        if form.is_valid() and profile_picture.is_valid():
            user = form.save()
            profile_picture.save()
            form_updated = True
            django_login(request, user)
    popularTags = popularTags = getPopularTags()

    return render(request, 'settings.html', {'popularTags': popularTags,
    'form': form,
    'profile_picture': profile_picture})


@require_POST
@login_required
def votes(request):
    data = request.POST
    rating = 0
    print("HELLO!")
    print(data['type'])
    if data['type'] == 'question_react':
        print(data)
        form = LikeQuestionForm(user=request.user.profile, question=data['id'], is_like=(data['action'] == 'like'))
        rating = form.save()
    elif data['type'] == 'answer':
        form = LikeAnswerForm(user=request.user.profile, answer=data['id'], is_like=(data['action'] == 'like'))
        rating = form.save()

    return JsonResponse({'rating': rating})


@require_POST
@login_required
def is_correct(request):
    data = request.POST
    answer = Answer.objects.get(pk=data['id'])
    if Answer.objects.filter(question_id=answer.question_id, is_correct=True).count() < 3 or answer.is_correct:
        answer.change_flag_is_correct()
    return JsonResponse({'action': answer.is_correct})