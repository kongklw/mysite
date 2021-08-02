from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.urls import reverse


# Create your views here.


# 方式1 使用template模板，然后在 httpResponse 里面render
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:3]
#     context = {'latest_question_list': latest_question_list}
#     template = loader.get_template('polls/index.html')
#     # output = ', '.join([q.question_text for q in latest_question_list])
#     # return HttpResponse(output)
#     return HttpResponse(template.render(context, request))

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    # try:
    #     question = Question.objects.get(id=question_id)
    #     print(question)
    # except Question.DoesNotExist:
    #     raise Http404('question does not exit')

    question = get_object_or_404(Question, id=question_id)
    return render(request, 'polls/detail.html', {'question': question})
    # return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    # response = "You're looking at the results of question %s."
    # return HttpResponse(response % question_id)

    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    print(question_id)
    print(request.POST)

    # 此时的choice 是choice 的数据库id

    question = get_object_or_404(Question, pk=question_id)

    # try:
    #     selected_choice = question.choice_set.get(pk=request.POST['choice'])
    #
    # except (KeyError, Choice.DoesNotExist):
    #     return render(request, 'polls/detail.html', {
    #         'question': question,
    #         'error_message': "You didn't select a choice.",
    #     })
    #
    # else:
    #     selected_choice.votes += 1
    #     selected_choice.save()

    # 方式2 直接使用choice模型类
    try:
        choice_id = request.POST['choice']
        selected_choice = Choice.objects.get(pk=choice_id)

    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })

    else:
        selected_choice.votes += 1
        selected_choice.save()

    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
