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
        for i in range((options['users_amount'])[0]):
            name = f"user#{i+3668}"
            mail = f"{name}@askpierre.com"
            password = "123AasDds#1"
            newUser = User.objects.create_user(name, mail, password)
            newUser.save()