from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from random import randint
from app.models import Question, Answer, Profile, LikeAnswer, LikeQuestion, Tag
# Create your views here.

questions = [
    {
        'id': i,
        'title': f'Title #{i}',
        'text': f'Question\'s text #{i}',
        'likesAmount': randint(0, 1000),
        'dislikesAmount': randint(0, 500),
        'answersAmount': 2,
        'tags': {f'Tag{randint(0, 100)}', f'Tag{randint(0, 100)}'},
        'username': f'user{i}'
    } for i in range(1000)
]

answers = [
    {
        'id': i,
        'question_id': i // 2,
        'text': f'Answer\'s text #{i}',
        'likesAmount': i + 3,
        'dislikesAmount': i + 3,
        'username': f'user{i}'
    } for i in range(1000)
]

tags = [
    {
        'id': i,
        'questions_id': {randint(0, 30), randint(0, 30)},
        'name': f'Tag{i}',
        'popularity': randint(0, 100)
    } for i in range(100)
]


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
    questions_page = paginate(Question.objects.all(), request)
    popularTags = getPopularTags()
    return render(request, 'index.html', {
        'questions': questions_page,
        'popularTags': popularTags
    })


def hot_questions(request):
    popularTags = getPopularTags()
    questions_page = paginate(Question.objects.all(), request)
    return render(request, 'hot.html', {
        'questions': questions_page,
        'popularTags': popularTags
    })



def tag_questions(request, name):
    popularTags = getPopularTags()
    tagQuestionPage = paginate(Question.objects.filter(tags__name=name), request)
    return render(request, 'tag.html', {'questions': tagQuestionPage, 'name': name, 
        'popularTags': popularTags})


def answers_for_question(request, pk):
    popularTags = getPopularTags()
    current_question = Question.objects.get(id=pk)
    answers_page = paginate(Answer.objects.filter(question=pk), request, 5)

    return render(request, 'question.html', {
        'question': current_question,
        'answers': answers_page,
        'popularTags': popularTags
    })


def login(request):
    popularTags = getPopularTags()
    return render(request, 'login.html', {'popularTags': popularTags})


def signup(request):
    popularTags = getPopularTags()

    return render(request, 'signup.html', {'popularTags': popularTags})


def ask(request):
    popularTags = popularTags = getPopularTags()

    return render(request, 'ask.html', {'popularTags': popularTags})


def settings(request):
    popularTags = popularTags = getPopularTags()

    return render(request, 'settings.html', {'popularTags': popularTags})
