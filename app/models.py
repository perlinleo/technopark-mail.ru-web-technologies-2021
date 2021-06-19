from django.db import models
from django.contrib.auth.models import User

class ProfileManager(models.Manager):
    def best_members(self):
        a = self.annotate(questions_amount = models.Count('question')).order_by('questions_amount')[:10]
        
       
        return a



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name = 'User ID')
    avatar = models.ImageField(max_length=1024, verbose_name = 'Avatar', null = True)


    objects = ProfileManager()
    
    def __str__(self):
        return self.user.get_username()
    


    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'



class TagManager(models.Manager):
    def get_popular_tags(self):
        #return self.annotate(questions_amount = models.Count('question')).order_by('-questions_amount')[:10]
        return self.order_by('-popularity')[:10]

    def add_tags_to_question(self, added_tags):
        tags = self.filter(name__in=added_tags)
        for tag in tags:
            tag.popularity += 1
            tag.save()
        return tags

class Question(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name = 'Author ID')
    title = models.CharField(max_length = 258, verbose_name = 'Title')
    text = models.TextField(verbose_name = 'Text')
    tags = models.ManyToManyField('Tag', verbose_name = 'Tags', null = True, blank=True)
    likesAmount = models.IntegerField(default=0, verbose_name='Amount of likes', null=True)
    dislikesAmount = models.IntegerField(default=0, verbose_name='Amount of dislikes', null=True)
    rating = models.IntegerField(default = 0,verbose_name='Question rating', null = False)
    
    
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'



class Answer(models.Model):
    def change_flag_is_correct(self):
        self.is_correct = not self.is_correct
        self.save()
    author = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name = 'Author ID')
    question = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name = 'Question ID')
    text = models.TextField(verbose_name = 'Text')
    is_correct = models.BooleanField(verbose_name = 'Is correct?', null = True)
    likesAmount = models.IntegerField(default=0, verbose_name='Amount of likes', null=True)
    dislikesAmount = models.IntegerField(default=0, verbose_name='Amount of dislikes', null=True)
    rating = models.IntegerField(default = 0,verbose_name='Question rating', null = False)
 

    def __str__(self):
        return f"{self.author.user.get_username()} answers on {self.question.__str__()}"
        
    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'
        

class LikeQuestion(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name = 'User ID')
    question = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name = 'Question ID') 
    opinion = models.BooleanField(default=True, verbose_name = 'Like/Dislike', null=True)
    
    def __str__(self):
        return f"{self.user.user.get_username()} reacted on {self.question.title}"
    
    def change_opinion(self, *args, **kwargs):
        if(self.opinion):
            self.question.likesAmount -= 1
            self.question.dislikesAmount +=1
        else:
            self.question.dislikesAmount -=1
            self.question.likesAmount += 1

        print(f"i was {self.opinion}")
        self.opinion=not self.opinion
        self.save()
        print(f"i am {self.opinion}")
        self.question.rating = self.question.likesAmount - self.question.dislikesAmount
        self.question.save()
    def save(self, *args, **kwargs):
        if not self.pk:
            if self.opinion:
                self.question.likesAmount += 1
            else:
                self.question.dislikesAmount += 1
            self.question.rating = self.question.likesAmount - self.question.dislikesAmount
            self.question.save()
        super(LikeQuestion, self).save(*args, **kwargs)
        return self.question.rating

    
    def delete(self, *args, **kwargs):
        if self.opinion:
            self.question.likesAmount -= 1
        else:
            self.question.dislikesAmount -= 1
        self.question.rating = self.question.likesAmount - self.question.dislikesAmount
        self.question.save()
        super(LikeQuestion, self).delete(*args, **kwargs)
        return self.question.rating
        
    class Meta:
        verbose_name = 'Question reacts'
        verbose_name_plural = 'Question reacts'
        
class LikeAnswer(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name = 'User ID')
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE, verbose_name = 'Answer') 
    opinion = models.BooleanField(default=True, verbose_name = 'Like?', null=False) 
    
    def __str__(self): 
        return f"{self.user.user.get_username()} reacted on {self.answer.author.user.get_username()}'s answer"
   
    def save(self, *args, **kwargs):
        if not self.pk:
            if self.opinion:
                self.answer.likesAmount += 1
            
            else:
                self.answer.dislikesAmount += 1
                
            self.answer.rating = self.answer.likesAmount - self.answer.dislikesAmount
            self.answer.save()
            
        super(LikeAnswer, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.opinion:
                self.answer.likesAmount -= 1
                
        else:
                self.answer.dislikesAmount -= 1

        
        self.answer.rating = self.answer.likesAmount - self.answer.dislikesAmount
        self.answer.save()
        super(LikeAnswer, self).delete(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Answer feedback'
        verbose_name_plural = 'Answers feedback' 


class Tag(models.Model):
    name = models.CharField(max_length=64, verbose_name = 'Name')
    popularity = models.IntegerField(default=0, verbose_name='Popularity', null=False)

    objects = TagManager()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'    