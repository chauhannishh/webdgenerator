# from .models import *
from django.db.models import Avg
from .models import *
from GoogleNews import GoogleNews
from profanity_check import predict, predict_prob
import requests
import jinja2
import pdfkit

def getCollege(college_id):
    college = College.objects.get(college = college_id)

    data = {
        "college_id": college_id,
        "college_name": college.college_name,
        "university": college.university,
        "address": college.address,
        "contact_number": college.contact_number,
        "logo": college.logo.name,
        "domain": college.domain,
        "about_us": college.about_us,
        "image1": college.image1.name,
        "image2": college.image2.name,
        "image3": college.image3.name,
        "image4": college.image4.name,
        "image5": college.image5.name,
        "departments": [],
        "upcoming_events": [],
    }

    departments = Department.objects.filter(college = college_id)
    
    for department in departments:    
        subs = []
        subjects = Subject.objects.filter(college = college_id, department = department.department_id)

        for subject in subjects:
            completed = 0
            if (len(SyllabusStatus.objects.annotate(av=Avg('completed')).filter(college = college_id, department = department.department_id, subject = subject.subject_id)) != 0):
                completed = SyllabusStatus.objects.annotate(av=Avg('completed')).filter(college = college_id, department = department.department_id, subject = subject.subject_id)

            syllabus = Syllabus.objects.filter(college = college_id, department = department.department_id, subject = subject.subject_id)
            
            s = {
                "subject_id": subject.subject_id,
                "subject_name": subject.subject_name,
                "semester": subject.semester,
                # "taught_by": {
                #     "teacher_id": subject.taught_by.teacher_id,
                #     "teacher_name": subject.taught_by.teacher_name,
                # },
                "syllabus": {
                    "syllabus": [],
                    "completed": completed
                }
            }

            for syl in syllabus:
                s["syllabus"]["syllabus"].append({
                    "syllabus_id":syl.id,
                    "unit": syl.unit,
                    "unit_name": syl.unit_name,
                    "topics": syl.topics,
                    "recommended_books": getBooks(subject.subject_name + syl.unit_name, 1)
                })

            subs.append(s);

        data["departments"].append({
            "department_id": department.department_id,
            "department_name": department.department_name,
            "vision_mission": department.vision_mission,
            "hod": department.hod,
            "count": department.count,
            "subjects": subs,
        })

    upcomingEvents = UpcomingEvents.objects.filter(college = college_id)
    for event in upcomingEvents:
        data["upcoming_events"].append({
            "event_id": event.event_id,
            "event_name": event.event_name,
            "event_description": event.event_description,
            "event_image": event.event_image,
            "start_date": event.start_date,
            "end_date": event.end_date,
        })

    return data


def getNews(query):
    googleNews = GoogleNews()
    googleNews.search(query)
    news = []

    i = 0

    number = min([len(googleNews.result()), 7])

    for result in googleNews.result():
        if (i > number):
            break

        news.append({
            "title": result['title'],
            "description": result['desc'],
            "link": result['link'],
            "date": result['date'],
            "image": result['img']
        })

    googleNews.clear()

    return news


def getBooks(query, num_books=1):
    r = requests.get("http://openlibrary.org/search.json", {'q': query})
    data = r.json()
    docs = data['docs']

    num = min(data['num_found'], num_books)

    books = []

    i = 0
    for doc in docs:
        if (i >= num):
            break

        books.append({
            "title": doc['title'],
            "publisher": doc['publisher'],
            "authors": doc['author_name'],
        })
        i += 1

    return books

def predict_profanity(message):
    return predict([message])

def generateSyllabusPDF(subjectID):
    templateLoader = jinja2.FileSystemLoader(searchpath="../")
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "demo_template.html"
    template = templateEnv.get_template(TEMPLATE_FILE)

    syllabus = Syllabus.objects.filter(subject = subjectID)

    college = syllabus.college.college_name
    department = syllabus.department.department_name
    subject = syllabus.subject.subject_name
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