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
        Answers = Answer.objects.all()
        for i in range((options['users_amount'])[0]):
            decision = random.randint(0,1)
            if decision==0:
                new = LikeQuestion.objects.create(user=Authors[random.randint(0,9000)],question=Questions[random.randint(0,60041)],opinion=False)
            else: 
                new = LikeQuestion.objects.create(user=Authors[random.randint(0,9000)],question=Questions[random.randint(0,60041)],opinion=True)
            new.save()