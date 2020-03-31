import jinja2
import pdfkit

templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "demo_template.html"
template = templateEnv.get_template(TEMPLATE_FILE)

syllabus = [
    {
        "unit": "Unit1",
        "unit_name": "Unit Name 1",
        "topics": "ABC, BCD, CDE, DEF",
        "recommended_books": [
            {
                "title": "Book Title1",
                "publisher": ["Publishers1"],
                "authors": ["Authors1"]
            },
            {
                "title": "Book Title2",
                "publisher": ["Publishers2"],
                "authors": ["Authors2"]
            }
        ]
    },
    {
        "unit": "Unit2",
        "unit_name": "Unit Name 2",
        "topics": "DEF, EFG, ABC, BCD, CDE, DEF",
        "recommended_books": [
            {
                "title": "Book Title1",
                "publisher": ["Publishers1"],
                "authors": ["Authors1"]
            },
            {
                "title": "Book Title2",
                "publisher": ["Publishers2"],
                "authors": ["Authors2"]
            }
        ]
    },
    {
        "unit": "Unit3",
        "unit_name": "Unit Name 3",
        "topics": "ABC, BCD, CDE, DEF",
        "recommended_books": [
            {
                "title": "Book Title1",
                "publisher": ["Publishers1"],
                "authors": ["Authors1"]
            },
            {
                "title": "Book Title2",
                "publisher": ["Publishers2"],
                "authors": ["Authors2"]
            }
        ]
    }
]

print(type(syllabus))

outputText = template.render(CollegeName="SGSITS", DepartmentName="IT", SubjectName="Distributed", syllabus=syllabus)
html_file = open('sgsits.html', 'w')
html_file.write(outputText)
html_file.close()

    
pdfkit.from_file('sgsits.html', 'sgsits.pdf')