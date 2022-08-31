from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
from chef.models import Course, Blog, Enroll


def index(request):
    return render(request, 'chef/index.html')


def my_courses(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        cover = request.FILES.get('cover')
        price = request.POST.get('price')
        duration = request.POST.get('duration')
        total_class = request.POST.get('total_class')
        description = request.POST.get('description')
        course = Course.objects.create(
            title=title,
            cover=cover,
            price=price,
            duration=duration,
            total_class=total_class,
            mentor_id=request.user.id,
            description=description
        )
        if course:
            messages.success(request, 'Course created successfully')
            return redirect(my_courses)
    courses = Course.objects.filter(mentor=request.user)
    return render(request, 'chef/my_courses.html', {'courses': courses})


def update_course(request):
    if request.method == 'POST':
        cover = request.FILES.get('cover')
        course = Course.objects.get(id=request.GET.get('course_id'))
        course.title = request.POST.get('title')
        course.price = request.POST.get('price')
        course.duration = request.POST.get('duration')
        course.total_class = request.POST.get('total_class')
        course.mentor = request.user
        course.description = request.POST.get('description')

        if cover is not None:
            course.cover = cover
        messages.success(request, 'Course updated successfully')
        course.save()
        return redirect(my_courses)


def delete_course(request):
    course = Course.objects.get(id=request.GET.get('course_id'))
    course.delete()
    messages.success(request, 'Course deleted successfully')
    return redirect(my_courses)


def my_blogs(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        cover = request.FILES.get('cover')
        content = request.POST.get('content')
        blog = Blog.objects.create(
            title=title,
            cover=cover,
            content=content,
            writer=request.user
        )
        if blog:
            messages.success(request, 'Blog added successfully')
            return redirect(my_blogs)
    blogs = Blog.objects.filter(writer=request.user)
    return render(request, 'chef/my_blogs.html', {'blogs': blogs})


def update_blog(request):
    if request.method == 'POST':
        cover = request.FILES.get('cover')
        blog = Blog.objects.get(id=request.GET.get('blog_id'))
        blog.title = request.POST.get('title')
        blog.content = request.POST.get('content')
        blog.writer = request.user

        if cover is not None:
            blog.cover = cover
        messages.success(request, 'Blog updated successfully')
        blog.save()
        return redirect(my_blogs)


def delete_blog(request):
    blog = Blog.objects.get(id=request.GET.get('blog_id'))
    blog.delete()
    messages.success(request, 'Blog deleted successfully')
    return redirect(my_blogs)


def my_students(request):
    enrolls = Enroll.objects.filter(course__mentor_id=request.user.id)
    print(enrolls.first())
    return render(request, 'chef/my_students.html', {'enrolls': enrolls})


def update_enroll(request):
    if request.method == 'POST':
        enroll_id = request.GET.get('enroll_id')
        status = request.POST.get('status')
        enroll = Enroll.objects.filter(id=enroll_id).first()
        print(status)
        if status == 'on':
            enroll.status = 1
        else:
            enroll.status = 0
        enroll.save()
        messages.success(request, 'Enrollment status saved successfully')
        return redirect('my_students')
