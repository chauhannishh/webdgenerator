from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from .models import *
import json
from django.urls import reverse
from myapp.forms import *
from django.utils import timezone
from .utils import getCollege, getNews, getBooks
import jinja2
import pdfkit
from django.conf import settings

def index(request):
    if request.user.is_authenticated:
        clg = str(College.objects.filter(applicant_id=request.session['uid'])[0].college)
        return HttpResponseRedirect('http://localhost:8000/college/'+clg)
    return HttpResponse("Login karna!")

def courses(request):
    return render(request,'courses.html',{})

def website_render(request):
    go_true = False
    syllabusObj = None
    if request.method == "POST":
        if request.POST.get("submit") == "clg":
            if request.POST.get("update") == "1":
                college_name = request.POST.get("college_name")
                university = request.POST.get("university")
                address = request.POST.get("address")
                contact_number = request.POST.get("contact_number")
                domain = request.POST.get("domain")
                about_us = request.POST.get("about_us")
                coll = College.objects.filter(college=request.POST.get('college_id'))
                coll.update(college_name=college_name,
                    university=university,address=address,contact_number=contact_number,domain=domain,
                    about_us=about_us)
                coll = coll[0]
                if "logo" in request.FILES:
                    coll.logo = request.FILES['logo']
                    coll.save()
                if "image1" in request.FILES:
                    coll.image1 = request.FILES['image1']
                    coll.save()
                if "image2" in request.FILES:
                    coll.image2 = request.FILES['image2']
                    coll.save()
                if "image3" in request.FILES:
                    coll.image3 = request.FILES['image3']
                    coll.save()
                if "image4" in request.FILES:
                    coll.image4 = request.FILES['image4']
                    coll.save()
                if "image5" in request.FILES:
                    coll.image5 = request.FILES['image5']
                    coll.save()
                return HttpResponse('http:127.0.0.1:8000/college/'+str(request.POST.get('college_id')))
            else:
                mutable_post = request.POST.copy()
                mutable_post["applicant_id"] = request.session['uid']
                clgForm = CollegeForm(mutable_post, request.FILES)
                if clgForm.is_valid():
                    clgForm.save()
                clg_id = College.objects.filter(applicant_id=request.session['uid'])[0].college
                return HttpResponse('http:127.0.0.1:8000/college/'+str(clg_id))   
        elif request.POST.get("submit") == "upcomming":
            clg = College.objects.filter(applicant_id=request.session['uid'])
            mutable_post = request.POST.copy()
            mutable_post["college"] = clg[0].college
            upForm = UpcommingForm(mutable_post, request.FILES)
            if upForm.is_valid():
                upForm.save()    
            return redirect('website_render')
        elif request.POST.get("submit") == "dept":

            if request.POST.get("update") == "1":
                deptID = request.POST.get('department_id')
                clgID = request.POST.get('college_id')
                name = request.POST.get('department_name')
                vision = request.POST.get('vision_mission')
                hod = request.POST.get('hod')
                count = request.POST.get('count')
                Department.objects.filter(department_id=deptID).update(department_name=name,hod = hod,count = count,vision_mission = vision)
                
            else:    
                clg = College.objects.filter(applicant_id=request.session['uid'])
                mutable_post = request.POST.copy()
                mutable_post["college"] = clg[0].college
                print(mutable_post)
                deptForm = DepartmentForm(mutable_post)
                if deptForm.is_valid():
                    dep = deptForm.save()

                    students = []
                    for i in range(99):
                        students.append(Student(
                            college = clg[0],
                            department = dep,
                            roll_number = str(clg[0].college_name[:3]) + "_" + str(request.POST['department_name'][:3]) + str(i).zfill(3),
                            semester = 1
                            ))
                    
                # Student.objects.bulk_create(students)
            return redirect('website_render')

        elif request.POST.get("submit") == "subject":
            if request.POST.get("update") == "1":
                print(request.POST.get('subject_id'))
                Subject.objects.filter(subject_id=request.POST.get('subject_id')).update(subject_name=request.POST.get('subject_name'),semester=request.POST.get('semester'))
            else:
                subForm = SubjectForm(request.POST)
                if subForm.is_valid():
                    subForm.save()
            return redirect('website_render')

        
        elif request.POST.get('submit') == 'get_syllabus':
            go_true = True
            college_id = request.POST.get('college')
            dept_id = request.POST.get('dept_name_syllabus')
            subject_id = request.POST.get('subject_name_syllabus')
            syllabusObj = [dept_id,subject_id,Syllabus.objects.filter(college__college=college_id,department__department_id=dept_id,subject__subject_id=subject_id)]


        elif request.POST.get('submit') == 'syllabus':
            if request.POST.get('update') == "1":
                syllabus_id = request.POST.get('syllabus_id')
                print(syllabus_id)
                
                syl = Syllabus.objects.filter(id=syllabus_id)
                print(syl)
                syl.update(unit=request.POST.get('unit'),unit_name=request.POST.get('unit_name'),topics=request.POST.get('topics'))
            else:
                sylForm = SyllabusForm(request.POST)
                if sylForm.is_valid():
                    sylForm.save()
            
            go_true = False
            # dept_id = request.POST.get('dept_name_syllabus')
            # subject_id = request.POST.get('subject_name_syllabus')
            # syllabusObj = [dept_id,subject_id,Syllabus.objects.filter(department__department_id=dept_id,subject__subject_id=subject_id)]
                            
    clg = College.objects.filter(applicant_id=request.session['uid'])
    CollegeObj = None
    hasCollege = False
    departments = None
    if len(clg):
        cc = getCollege(clg[0].college)
        hasCollege = True
        CollegeObj = cc
        departments = cc['departments']
        #Edit Dashboard
    clgForm = CollegeForm()
    deptForm = DepartmentForm()
    upForm = UpcommingForm()
    college = None
    flag = True
    dept_list = []
    try:
        flag = True
        if len(clg):
            college = clg[0].college
            dept_list = Department.objects.filter(college=College.objects.get(applicant_id= request.session['uid']))
        else:
            dept_list = []
    except:
        flag = False
        dept_list = []
    subForm = SubjectForm()
    syllabusForm = SyllabusForm()
    return render(request,'website_render.html',{"hasCollege":hasCollege,"CollegeObj":CollegeObj,"go_true":go_true,"syllabusObj":syllabusObj,"upForm":upForm,"user_id": request.session['uid'],"college_id":college,"clgForm":clgForm,"deptForm":deptForm,"flag":flag,"subForm":subForm,"syllabusForm":syllabusForm,"dept_list":dept_list,"departments":departments})

def user_login(request,college_id):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                # request.session['member_cat'] = val
                # return HttpResponseRedirect(reverse('index'))
                return render(request,'forum.html')

        else:
            return render(request,'login.html')
              
    return render(request,'login.html')

@login_required(login_url='index')
def user_logout(request,college_id):
    logout(request)
    return redirect("http://127.0.0.1:8000/college/"+college_id)

##########################

def admin_user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                # print()
                request.session['uid'] = User.objects.get(username=username).id 
                # return HttpResponseRedirect(reverse('index'))
                return redirect('website_render')
        else:
            return render(request,'admin/admin_index.html',{"invalidDetails":True})
              
    return render(request,'admin/admin_index.html',{})

@login_required(login_url='index')
def admin_user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("admin_user_login"))

def admin_login_page(request):
    return render(request,'admin/admin_index.html')

##########################

def login_page(request,college_id):
    return render(request,'login.html')

def college(request, college_id):
    data = getCollege(college_id)
    clg_news_img = getNews(data['college_name'])[1]
    clg_news = getNews(data['college_name'])[1:5]
    event_list = data['upcoming_events'][0:3]
    print(event_list)
    return render(request, 'index.html', {"data":data,"clg_news_img":clg_news_img,"clg_news":clg_news,"event_list":event_list})
    # return HttpResponse(json.dumps(data, indent=4), content_type="application/json")

def forums(request, college_id, forum_id):
    if request.method == "POST":
        ForumMessage(
            college = College.objects.get(college_id = college_id),
            forum = Forum.objects.get(forum_id),
            message = request.POST['message'],
            sent_by = request.session['uid'],
            sent_at = timezone.now(),
            isAnonymous = request.POST['isAnonymous']
            ).save()
        return HttpResponse("Hello")
    
    messages = []
    msgs = ForumMessage.objects.filter(college = college_id, forum = forum_id)

    for m in msgs:
        message = {}
        print(m.isAnonymous)
        message["message"] = m.message
        message["sent_at"] = m.sent_at
        if (m.isAnonymous == True):
            message["sent_by"] = "anonymous"
        else:
            message["sent_by"] = m.sent_by
        
        messages.append(message)

    return render(request,'forum.html',{"messages":messages})

def getDepartment(request,college_id):
    data = getCollege(college_id)
    return render(request, 'department.html', {"data":data})

def getSubjects(request,college_id,dept_name):
    data = getCollege(college_id)
    subj = []
    for i in data['departments']:
        if i['department_name'] == dept_name:
            subj = i['subjects']
            break
    return render(request, 'subjects.html', {"data":data,"subj":subj})

def generateSyllabusPDF(request):
    if request.method == "POST":
        subjectID = request.POST.get('Syllabus')
        print(subjectID)
        templateLoader = jinja2.FileSystemLoader(searchpath=".")
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = "demo_template.html"
        template = templateEnv.get_template(TEMPLATE_FILE)

        syllabus = Syllabus.objects.filter(subject = subjectID)
        print(syllabus)
        if len(syllabus):
            college = syllabus[0].college.college_name
            department = syllabus[0].department.department_name
            subject = syllabus[0].subject.subject_name
            syll = []

            for units in syllabus:
                syll.append({
                    "unit": units.unit,
                    "unit_name": units.unit_name,
                    "topics": units.topics,
                    "recommended_books": getBooks(subject + " " + units.unit_name)
                })

            outputText = template.render(CollegeName=college, DepartmentName=department, SubjectName=subject, syllabus=syll)
            html_file = open(college + '.html', 'w')
            html_file.write(outputText)
            html_file.close()

            pdfkit.from_file(college + '.html', college + '.pdf')
        else:
            return HttpResponse("No Syllabus Found")