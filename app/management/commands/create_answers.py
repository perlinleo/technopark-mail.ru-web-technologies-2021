from django.core.management.base import BaseCommand, CommandError
from app.models import Question, Answer, Profile, LikeAnswer, LikeQuestion, Tag
from django.contrib.auth.models import User
import random_name_generator as rng
import random

class Command(BaseCommand):
    help = 'creates users'

    def add_arguments(self, parser):
        parser.add_argument('users_amount', nargs='+', type=int)

    def handle(self, *args, **options):
        Authors = Profile.objects.all()
        Questions = Question.objects.all()
        for i in range((options['users_amount'])[0]):
            new = Answer.objects.create(author=Authors[random.randint(0,9000)],question=Questions[random.randint(55000,60040)],text="test",likesAmount=0,dislikesAmount=0,is_correct=False)
            
            new.save()