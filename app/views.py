from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from random import randint
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
        'likesAmount': i + 42,
        'dislikesAmount': i + 24,
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
    popularTags = []
    for tag in tags:
        if tag.get('popularity') > 96:
            popularTags.append(tag)
    return popularTags

def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, 5)
    page = request.GET.get('page')
    objects = paginator.get_page(page)

    return objects


def index(request):
    all_new_questions = questions.copy()
    all_new_questions.reverse()
    popularTags = getPopularTags()
    new_questions = paginate(all_new_questions, request)

    return render(request, 'index.html', {'questions': new_questions,
                                          'popularTags': popularTags})


def hot_questions(request):
    all_sorted_questions = questions.copy()
    all_sorted_questions.sort(key=lambda x: x.get('likesAmount'), reverse=True)
    popularTags = getPopularTags()
    sorted_questions = paginate(all_sorted_questions, request)

    return render(request, 'hot_questions.html', {'questions': sorted_questions,
                                                  'popularTags': popularTags})


def tag_questions(request, name):
    current_tag = {}
    popularTags = getPopularTags()
    for tag in tags:
        if tag.get('name') == name:
            current_tag = tag
    current_tag_all_questions = []
    for question in questions:
        if current_tag.get('name') in question.get('tags'):
            current_tag_all_questions.append(question)
    current_tag_questions = paginate(current_tag_all_questions, request)

    return render(request, 'tag.html', {'tag': current_tag,
                                        'questions': current_tag_questions,
                                        'popularTags': popularTags})


def answers_for_question(request, pk):
    question = questions[pk]
    all_question_answers = []
    for answer in answers:
        if answer.get('question_id') == pk:
            all_question_answers.append(answer)
    popularTags = getPopularTags()
    question_answers = paginate(all_question_answers, request)

    return render(request, 'question.html', {'question': question,
                                             'answers': question_answers,
                                             'popularTags': popularTags})


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
