section 1



Flask==0.12.2
Flask-Babel==0.11.2
Flask-Bootstrap==3.3.7.1
Flask-Login==0.4.0
Flask-WTF==0.14.2
flipflop==1.0
html5lib==0.999999999
httplib2==0.7.4
Jinja2==2.9.6
requests==2.4.3
urllib3==1.9.1
Werkzeug==0.12.2
WTForms==2.1

section2

command: python3 run.py
url: http://127.0.0.1:5000
if it is the first time to run the server, you also need type these command:
python3 database_create.py #create the database file
python3 database_update_script.py #update the data in csv to the database


section 3

place the test.py which in test.zip in the same folder of run.py
then type command: python3 test.py
if the test program prints "True", then this test is passed.
tests name:
Test_enrol
Test_create_question
Test_create_optional_question
Test_Create_Survey
Test_Student_Course
