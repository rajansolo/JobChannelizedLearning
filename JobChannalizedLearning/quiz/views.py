from django.shortcuts import render, redirect, HttpResponse
from .models import Quiz
from django.views import View
from django.http import HttpResponseNotAllowed, JsonResponse
from questions.models import Question, Answer
from results.models import Result
from .forms import QuizForm, QuestionForm, AnswerFormSet, QuizUploadForm
from django.shortcuts import get_object_or_404
from django.forms import inlineformset_factory
from django.db.models import OuterRef, Subquery
from django.contrib.auth.decorators import login_required
import json

@login_required
def question_list(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.question_set.all()
    form = QuizUploadForm()
    if request.POST:
        form = QuizUploadForm(request.POST, request.FILES)
        if form.is_valid():
            json_file = form.cleaned_data['json_file']
            json_data = json.load(json_file)
            for question in json_data:
                question_instance = Question(
                    text=question['text'],
                    quiz=quiz,
                )
                question_instance.save()
                for answer in question['answers']:
                    answer_instance = Answer(
                        text=answer['text'],
                        correct=answer['correct'],
                        question=question_instance,
                    )
                    answer_instance.save()
        return redirect('quiz:question_list', quiz_id=quiz.id)
    return render(request, 'quiz/question_list.html', {'quiz': quiz, 'questions': questions, 'form': form})

@login_required
def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        print(request.POST)
        question_form = QuestionForm(request.POST)
        answer_formset = AnswerFormSet(request.POST)
        if question_form.is_valid() and answer_formset.is_valid():
            question = question_form.save(commit=False)
            question.quiz = quiz
            question.save()
            answer_formset.instance = question
            answer_formset.save()
            return redirect('quiz:question_list', quiz_id=quiz.id)
    else:
        question_form = QuestionForm()
        answer_formset = AnswerFormSet()
    return render(request, 'quiz/add_question.html', {'quiz': quiz, 'question_form': question_form, 'answer_formset': answer_formset})

@login_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        question.delete()
        return redirect('quiz:question_list', quiz_id=question.quiz.id)
    else:
        return HttpResponseNotAllowed(['POST'])


@login_required
def update_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    AnswerFormSet = inlineformset_factory(Question, Answer, fields=('text', 'correct'), extra=0)

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = AnswerFormSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('quiz:question_list', quiz_id=question.quiz.id)
    else:
        form = QuestionForm(instance=question)
        formset = AnswerFormSet(instance=question)
    return render(request, 'quiz/update_question.html', {'form': form, 'formset': formset})

@login_required
def delete_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    if request.method == 'POST':
        answer.delete()
        return redirect('quiz:update_question', question_id=answer.question.id)
    else:
        return HttpResponseNotAllowed(['POST'])

@login_required
def quizzes(request, slug):
    quizzes = Quiz.objects.filter(topic=slug)
    return render(request, 'quiz/quizzes.html', {'quizzes': quizzes, 'slug': slug})

@login_required
def add_quiz(request, slug):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.topic = slug
            form.save()
            return redirect('quiz:quizzes', slug=slug)
    else:
        form = QuizForm()
    return render(request, 'quiz/add_quiz.html', {'form': form})

@login_required
def update_quiz(request, quiz_id, slug):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('quiz:quizzes', slug=slug)
    else:
        form = QuizForm(instance=quiz)
    return render(request, 'quiz/update_quiz.html', {'form': form, 'quiz': quiz, 'slug': slug})

@login_required
def delete_quiz(request, quiz_id, slug):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        quiz.delete()
        return redirect('quiz:quizzes', slug=slug)
    else:
        return HttpResponseNotAllowed(['POST'])

class Quiz_list_view(View):
    def get(self,request,slug):
        if not request.user.is_authenticated:
            return redirect('user_account:login_first')
        context={}
        score_subquery = Result.objects.filter(quiz=OuterRef('pk')).values('quiz').order_by('-score').values('score')[
                         :1]
        context['object_list'] = Quiz.objects.filter(topic=slug).annotate(score=Subquery(score_subquery))
        return render(request,'quiz/main.html',context)


@login_required
def quiz_view(request, slug, pk):
    quiz = Quiz.objects.get(pk=pk)
    return render(request, 'quiz/quiz.html', {'obj': quiz, 'slug':slug})

@login_required
def quiz_data_view(request,slug,pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions,
        'time': quiz.time,
    })

@login_required
def save_quiz_view(request,slug, pk):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            print('key: ', k)
            question = Question.objects.get(text=k)
            questions.append(question)
        print(questions)

        user = request.user
        quiz = Quiz.objects.get(pk=pk)

        score = 0
        multiplier = 100 / quiz.number_of_questions
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.text)

            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text

                results.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                results.append({str(q): 'not answered'})
            
        score_ = score * multiplier
        Result.objects.create(quiz=quiz, user=user, score=score_)

        if score_ >= quiz.required_score_to_pass:
            return JsonResponse({'passed': True, 'score': score_, 'results': results})
        else:
            return JsonResponse({'passed': False, 'score': score_, 'results': results})