from django.db import models
import datetime
from django.utils import timezone
# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now-datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class CourseList(models.Model):
    department_text = models.CharField(max_length=100)
    course_text = models.CharField(max_length=100)
    igetc_text = models.CharField(max_length=100)
    session_id = models.IntegerField(default=0)
    schedule_text = models.CharField(max_length=100)
    location_text = models.CharField(max_length=100)
    instructor_text = models.CharField(max_length=100)
    grade_A_num = models.IntegerField(default=0)
    grade_B_num = models.IntegerField(default=0)
    grade_C_num =models.IntegerField(default=0)
    grade_P_num =models.IntegerField(default=0)
    grade_total_num =models.IntegerField(default=0)
    grade_A_rate = models.IntegerField(default=0)
    grade_gt_B_rate =models.IntegerField(default=0)
    grade_gt_C_rate =models.IntegerField(default=0)
    grade_gt_P_rate =models.IntegerField(default=0)
    rating_num_text = models.CharField(max_length=100)
    url_text =models.CharField(max_length=200)
    instructor_department_text=models.CharField(max_length=100)
    lname_text =models.CharField(max_length=100)
    fname_text =models.CharField(max_length=100)
    tid_id = models.IntegerField(default=0)
    votes_num = models.IntegerField(default=0)

    def __str__(self):
        return self.course_text + ','+self.instructor_text

