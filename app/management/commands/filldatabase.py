from enum import unique
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Question, Answer, Tag, LikeQuestion, LikeAnswer
from random import choice, sample, randint, getrandbits
from faker import Faker
from tqdm import tqdm, trange

f = Faker()


class Command(BaseCommand):
    help = "Command to fill database"

    def add_arguments(self, parser):
        parser.add_argument('--full', nargs='+', type=int)
        parser.add_argument('--users', nargs='+', type=int)
        parser.add_argument('--questions', nargs='+', type=int)
        parser.add_argument('--answers', nargs='+', type=int)
        parser.add_argument('--tags', nargs='+', type=int)
        parser.add_argument('--likes', nargs='+', type=int)

        parser.add_argument('--dusers')
        parser.add_argument('--dlikes')

    def handle(self, *args, **options):
        if options['full']:
            self.fill_full_db(options['full'][0])

        if options['users']:
            self.fill_users(options['users'][0])

        if options['tags']:
            self.fill_tags(options['tags'][0])

        if options['questions']:
            self.fill_questions(options['questions'][0])

        if options['answers']:
            self.fill_answers(options['answers'][0])

        if options['likes']:
            self.fill_likes_questions(options['likes'][0])
            self.fill_likes_answers(2 * options['likes'][0])

        if options['dusers']:
            self.delete_users()

        if options['dlikes']:
            self.delete_likes()

    @staticmethod
    def fill_users(count):
        for i in tqdm(range(count), desc="Creating users"):
            name = f.user_name()
            while User.objects.filter(username=name).exists():
                name = f.user_name()
            user_id=User.objects.create(
                    username=name)
            Profile.objects.create(
                user=user_id,
            )

    @staticmethod
    def fill_tags(count):
        
        for i in tqdm(range(count), desc="Creating tags"):
            tag_name = f.word()
            while Tag.objects.filter(name=tag_name).exists():
                tag_name = f"{f.word()} {i}"
                #print(tag_name)
               
            Tag.objects.create(name=tag_name)

    @staticmethod
    def fill_questions(count):
        profiles = list(Profile.objects.values_list('id', flat=True))
        lastProfileID = Profile.objects.last().id
        firstProfileID = Profile.objects.first().id
        diff=count-(lastProfileID-firstProfileID)
        for i in tqdm(range(firstProfileID,lastProfileID+diff), desc="Creating questions"):
            tags = list(Tag.objects.values_list('id', flat=True))
            tags_for_question = sample(tags, k=randint(1, 5))
            current_question = Question.objects.create(
                author = Profile.objects.get(id=(i%lastProfileID)+1),
                title=f.sentence(),
                text=f.text(),
            )
            
            current_question.tags.set(tags_for_question)
            
    @staticmethod
    def fill_answers(count):
        profiles = list(Profile.objects.values_list('id', flat=True))
        questions = list(Question.objects.values_list('id', flat=True))
        for i in tqdm(range(count), desc="Creating answers"):
            Answer.objects.create(
                author=Profile.objects.get(pk=choice(profiles)),
                question=Question.objects.get(pk=choice(questions)),
                text=f.text(),
                is_correct=randint(0, 1),
            )

    @staticmethod
    def fill_likes_questions(count):
        lastQuestionId=Question.objects.last().id
        lastProfileId=Profile.objects.last().id
        
        firstQuestionId=Question.objects.first().id
        firstProfileId=Profile.objects.first().id
        
        for i in tqdm(range(count), desc="Creating likes for answers"):
            LikeQuestion.objects.create(
                    question=Question.objects.get(id=randint(firstQuestionId,lastQuestionId)),
                    user=Profile.objects.get(id=randint(firstProfileId,lastProfileId)),
                    opinion=bool(getrandbits(1))
            )
    @staticmethod
    def fill_likes_answers(count):
    
        lastAnswerId=Answer.objects.last().id
        lastProfileId=Profile.objects.last().id

        firstAnswerId=Answer.objects.first().id
        firstProfileId=Profile.objects.first().id
        
        for i in tqdm(range(count), desc="Creating likes for answers"):
            LikeAnswer.objects.create(
                    answer=Answer.objects.get(id=randint(firstAnswerId,lastAnswerId)),
                    user=Profile.objects.get(id=randint(firstProfileId,lastProfileId)),
                    opinion=bool(getrandbits(1))
            )
        

    @staticmethod
    def delete_users():
        Profile.objects.all().delete()
        User.objects.all().delete()

    @staticmethod
    def delete_likes():
        LikeQuestion.objects.all().delete()
        LikeAnswer.objects.all().delete()

    def fill_full_db(self, count):
        print('Creating users')
        #self.fill_users(count)
        print('Users are created')
        print('Creating tags')
        #self.fill_tags(count)
        print('Tags are created')
        print('Creating questions')
        self.fill_questions(count * 10)
        print('Questions are created')
        print('Creating answers')
        self.fill_answers(count * 100)
        print('Answers are created')
        self.fill_likes_questions(count * 500)
        print('Likes for questions are created')
        self.fill_likes_answers(count * 500)
        print('Likes for answers are created')