from django.shortcuts import render
from django.http import HttpResponse
from .models import Question, Choice
from django.shortcuts import render
from django.shortcuts import get_list_or_404
from django.http import HttpResponseRedirect
# from django.urls import reverse
from django.views import generic
from django.utils import timezone
# Create your views here.

#
# class IndexView(generic.ListView):
#     template_name = 'poos/index.html'
#     context_object_name = 'latest_question_list'
#
#     def get_queryset(self):
#         # return Question.objects.order_by("pub_date")[:5]
#         return Question.objects.filter(
#             pub_date__lte=timezone.now()
#         ).order_by('pub_date')[:5]


# class IndexView(generic.ListView):
#     template_name = 'poos/index.html'
#     context_object_name = 'course_list'
#
#     def get_queryset(self):
#         return CourseList.objects.all()



class IndexView(generic.ListView):
    template_name = 'poos/index.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        return Question.objects.all()

class DetailView(generic.DetailView):
    model = Question
    template_name = 'poos/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'poos/results.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())









# def vote(request, question_id):
#     question = get_list_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question[0].choice_set.get(pk=request.POST['choice'])
#         print(question[0],question[0].choice_set.get(pk=request.POST['choice']))
#     except(KeyError, Choice.DoesNotExist):
#         return render(request, "poos/detail.html", {"question": question, 'error_message': 'you didn\'t select a choice'})
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         return HttpResponseRedirect(reverse('poos:results', args=(question_id,)))

def sample(request):
    return render(request, 'poos/sample.html,')
# class CourseView(generic.ListView):
#     template_name = 'poos/course.html'
#     context_object_name = 'course_list'
#
#     def get_queryset(self):
#
#         return CourseList.objects.all()