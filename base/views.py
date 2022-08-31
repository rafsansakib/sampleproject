from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
from account.models import Profile
from chef.models import Blog, Course, Chef, Enroll


def index(request):
    blogs = Blog.objects.all()[:8]
    courses = Course.objects.all()[:8]
    chefs = Chef.objects.all()[:8]
    print(chefs)
    context = {
        'blogs': blogs,
        'courses': courses,
        'chefs': chefs
    }
    return render(request, 'base/index.html', context)


def courses(request):
    courses = Course.objects.all()
    return render(request, 'base/all_courses.html', {'courses': courses})


def chefs(request):
    chefs = Chef.objects.all()
    return render(request, 'base/all_chefs.html', {'chefs': chefs})


def all_chefs(request):
    chefs = Chef.objects.all()
    return render(request, 'base/chefs.html', {'chefs': chefs})


def students(request):
    students = User.objects.filter(profile__role='student')
    return render(request, 'base/all_students.html', {'students': students})


def course(request):
    course = Course.objects.get(id=request.GET.get('course_id'))
    return render(request, 'base/course.html', {'course': course})


def blogs(request):
    blogs = Blog.objects.all()
    return render(request, 'base/all_blogs.html', {'blogs': blogs})


def blog(request):
    blog = Blog.objects.get(id=request.GET.get('blog_id'))
    return render(request, 'base/blog.html', {'blog': blog})


def add_chef(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        restaurant = request.POST.get('restaurant')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        cover = request.FILES.get('cover')
        exist = User.objects.filter(username=username).first()
        if password != confirm_password:
            messages.error(request, 'Password unmatched')
            return redirect('all_chefs')
        if exist:
            messages.error(request, 'Username already exists')
            return redirect('all_chefs')
        exist = User.objects.filter(email=email).first()
        if exist:
            messages.error(request, 'Email already exists')
            return redirect('all_chefs')
        user = User.objects.create_user(username=username, password=password, email=email)
        Profile.objects.create(user=user, role="chef", cover=cover)
        print(cover)
        if restaurant:
            Chef.objects.create(user=user, restaurant=restaurant)
        messages.success(request, 'Chef added successfully')
        return redirect('all_chefs')
    return redirect('all_chefs')


def update_chef(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        restaurant = request.POST.get('restaurant')
        cover = request.FILES.get('cover')
        user = User.objects.filter(id=request.GET.get('chef_id')).first()
        user.username = username
        user.email = email
        user.save()
        chef = Chef.objects.filter(user_id=request.GET.get('chef_id')).first()
        chef.restaurant = restaurant
        chef.save()
        profile = Profile.objects.filter(user_id=request.GET.get('chef_id')).first()
        if cover:
            profile.cover = cover
            profile.save()
        messages.success(request, 'Chef updated successfully')
        return redirect('all_chefs')
    return redirect('all_chefs')


def delete_chef(request):
    chef = User.objects.filter(id=request.GET.get('chef_id')).first()
    chef.delete()
    messages.success(request, 'Chef deleted successfully')
    return redirect('all_chefs')


def add_student(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        exist = User.objects.filter(username=username).first()
        if password != confirm_password:
            messages.error(request, 'Password unmatched')
            return redirect('all_students')
        if exist:
            messages.error(request, 'Username already exists')
            return redirect('all_students')
        exist = User.objects.filter(email=email).first()
        if exist:
            messages.error(request, 'Email already exists')
            return redirect('all_students')
        user = User.objects.create_user(username=username, password=password, email=email)
        Profile.objects.create(user=user, role="student")
        messages.success(request, 'Student added successfully')
        return redirect('all_students')
    return redirect('all_students')


def update_student(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        student = User.objects.filter(id=request.GET.get('student_id')).first()
        student.username = username
        student.email = email
        student.save()
        messages.success(request, 'Student updated successfully')
        return redirect('all_students')
    return redirect('all_students')


def delete_student(request):
    student = User.objects.filter(id=request.GET.get('student_id')).first()
    student.delete()
    messages.success(request, 'Student deleted successfully')
    return redirect('all_students')


def enroll(request):
    if request.method == 'POST':
        course_id = request.GET.get('course_id')
        banking = request.POST.get('banking')
        txn_id = request.POST.get('txn_id')
        phone = request.POST.get('phone')
        print(course_id, banking, txn_id, phone)
        Enroll.objects.create(course_id=course_id, banking=banking, txn_id=txn_id, student_id=request.user.id,
                              phone=phone)
        messages.success(request, 'Successfully submitted enrollment form')
        return redirect('home')


def my_enrolls(request):
    enrolls = Enroll.objects.filter(student=request.user)
    return render(request, 'base/my_enrolls.html', {'enrolls': enrolls})


def chef_blogs(request):
    blogs = Blog.objects.filter(writer_id=request.GET.get('chef_id'))
    return render(request, 'base/all_blogs.html', {'blogs': blogs})


def chef_courses(request):
    print(request.GET.get('chef_id'))
    courses = Course.objects.filter(mentor_id=request.GET.get('chef_id'))
    return render(request, 'base/all_courses.html', {'courses': courses})
