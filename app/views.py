from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, redirect, reverse
from random import randint
from django.http import Http404
from app.models import Question, Answer, Profile, LikeAnswer, LikeQuestion, Tag
from django.db.models import Count
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from app.forms import *





def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, 5)
    page = request.GET.get('page')
    objects = paginator.get_page(page)

    return objects



    

def index(request):
    best_users = Profile.objects.best_members()
 
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
    print(best_users)
    

    return render(request, 'index.html', {
        'best_users': Profile.objects.best_members(), 
        'liked_questions': liked_questions,
        'disliked_questions': disliked_questions,
        'reacts_page': reacts_page,
        'questions': questions_page,
        'popularTags': Tag.objects.get_popular_tags()
    })


def hot_questions(request):
        best_users = Profile.objects.best_members()
    
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
            'best_users': Profile.objects.best_members(), 
            'liked_questions': liked_questions,
            'disliked_questions': disliked_questions,
            'reacts_page': reacts_page,
            'questions': questions_page,
            'popularTags': Tag.objects.get_popular_tags()
        })

@login_required
def logout(request):
    django_logout(request)
    previous_page = request.META.get('HTTP_REFERER')
    if previous_page is not None:
        return redirect(previous_page)
    return redirect("/")


def tag_questions(request, name):
    try:
        tag = Tag.objects.get(name=name)
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
        amount = f"{Question.objects.filter(tags__name=name).count()} questions with tag {name}"

        return render(request, 'tag.html', {
            'best_users': Profile.objects.best_members(), 
            'name': amount,
            'liked_questions': liked_questions,
            'disliked_questions': disliked_questions,
            'reacts_page': reacts_page,
            'questions': questions_page,
            'popularTags': Tag.objects.get_popular_tags()
        })
    except Tag.DoesNotExist:
        raise Http404

def answers_for_question(request, pk):
    try:
        current_question = Question.objects.get(id=pk)
        try: 
            userProfile = Profile.objects.get(user_id=request.user.id)
        except: 
            userProfile = Profile.objects.get(user_id=1)
        is_like = 'btn-secondary'
        is_dislike = 'btn-secondary'
        try:
        
            if(LikeQuestion.objects.get(question=current_question, user=userProfile.id).opinion):
                is_like = 'btn-success'
            else:
                is_dislike = 'btn-danger'
        except:
            print("not found")
        answers_page = paginate(Answer.objects.filter(question=pk).order_by('rating'), request, 5)
            

        if request.method == 'GET':
                form = AnswerForm()
        else:
                if not request.user.is_authenticated:
                    return redirect(f"login/?next={request.get_full_path()}")

                form = AnswerForm(profile_id=request.user.profile.id, question_id=pk, data=request.POST)
                if form.is_valid():
                    form.save()
                    answers_page = paginate(Answer.objects.filter(question=pk).order_by('rating'), request, 5)
                    return redirect(reverse('answers_for_questions', kwargs={'pk': pk}) + f"?page={answers_page.paginator.num_pages}")

    
        return render(request, 'question.html', {
            'dislike_color': is_dislike,
            'like_color': is_like,
            'best_users': Profile.objects.best_members(), 
            'form': form,
            'question': current_question,
            'answers': answers_page,
            'popularTags': Tag.objects.get_popular_tags()
        })
    except Question.DoesNotExist:
        raise Http404


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
 
    return render(request, 'login.html', {
        'best_users': Profile.objects.best_members(), 
        'popularTags': Tag.objects.get_popular_tags(),
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


    return render(request, 'signup.html', {'popularTags': Tag.objects.get_popular_tags(), 
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
    return render(request, 
            'ask.html', {
                'best_users': Profile.objects.best_members(), 
                'popularTags': Tag.objects.get_popular_tags(),
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
   

    return render(request, 'settings.html', {
        'best_users': Profile.objects.best_members(), 
        'popularTags': Tag.objects.get_popular_tags(),
        'form': form,
        'profile_picture': profile_picture
        })


@require_POST
@login_required
def votes(request):
    data = request.POST
    rating = 0
    if data['type'] == 'question_react':
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