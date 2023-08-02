from django.shortcuts import render, redirect, get_object_or_404
from course.models import Catogaries, Course, CourseView
from quiz.models import Quiz
from results.models import Result
from course.forms import CategoryForm, CourseForm  # ZipUploadForm
import re
from django.conf import settings
from django.contrib.auth.decorators import login_required


# Create your views here.

def home_view(request):
    catogery = Catogaries.objects.all()
    course = Course.objects.filter(status='PUBLISH').order_by('-id')
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = CategoryForm()
    context = {
        'catogery': catogery,
        'course': course,
        'form': form
    }
    if not request.user.is_authenticated:
        return redirect('user_account:login_first')
    return render(request, 'website_content/home_page.html', context)


@login_required
def course_detail(request, name):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course_form = form.save(commit=False)
            course_form.author = request.user.username
            course_form.category = Catogaries.objects.get(name=name)
            slug = re.sub(r'[^\w\s]', '', form.cleaned_data['title']).lower()
            course_form.slug = re.sub(r'\s+', '_', slug)
            form.save()
    else:
        form = CourseForm()
    filtered_courses = Course.objects.filter(
        category=Catogaries.objects.get(name=name))
    context = {
        'filtered_courses': filtered_courses,
        'form': form
    }
    if request.user.user_role == 'STUDENT':
        return render(request, 'courses/filtered_course.html', context)
    else:
        filtered_courses = filtered_courses.filter(
            author=request.user.username)
        context['filtered_courses'] = filtered_courses
        return render(request, 'courses/M_filtered.html', context)

@login_required
def pay(request, price):
    return render(request, 'website_content/payment.html', {'price': price})

@login_required
def filtered_content(request, name, slug):
    courses = Course.objects.filter(slug=slug)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES,
                          instance=courses.first())
        if form.is_valid():
            form.save()
    else:
        form = CourseForm(instance=courses.first())

    context = {
        'courses': courses,
        'form': form,
        'slug': slug,
    }

    if request.user.user_role == 'STUDENT':
        course = get_object_or_404(Course, slug=slug)
        course_view, created = CourseView.objects.get_or_create(
            user=request.user, course=course)
        if not created:
            course_view.view += 1
            course_view.save()
        return render(request, 'courses/course_content.html', context)
    else:
        return render(request, 'courses/M_course.html', context)


# membership pages
@login_required
def plan_details(request):
    return render(request, 'website_content/plans.html')


@login_required
def handle_transaction(request, price):
    print("inside handle")
    if price == '0':
        plan = 'Basic'
    elif price == '10':
        plan = 'Super'
    else:
        plan = 'Pro'
    user = request.user
    user.plan = plan
    user.save()
    return redirect('website_content:plan_details')

# Student grades


@login_required
def access_grades(request):
    courses = Course.objects.filter(author=request.user)
    course_slugs = courses.values_list('slug', flat=True)
    quizzes = Quiz.objects.filter(topic__in=course_slugs)
    results = Result.objects.filter(quiz__topic__in=course_slugs)

    context = {
        'courses': courses,
        'quizzes': quizzes,
        'results': results
    }
    return render(request, 'website_content/grades.html', context)


# views.py
@login_required
def course_view(request, slug):
    course = get_object_or_404(Course, slug=slug)
    course_views = CourseView.objects.filter(course=course).count()
    detail = CourseView.objects.filter(course=course)
    return render(request, 'website_content/course_view.html', {'course': course, 'course_views': course_views, 'detail': detail})
