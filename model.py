import database
from wtforms import StringField, SubmitField, BooleanField, TextAreaField, DateTimeField, RadioField, SelectField, SelectMultipleField,PasswordField, HiddenField
from wtforms.validators import Required, AnyOf,Email,EqualTo,ValidationError,Optional
from flask_login import LoginManager,login_user, current_user, login_required, logout_user
from flask_wtf import Form
import datetime
from flask import flash
import Forms
import hashlib
import flask
from flask_login import UserMixin
from app import login_manager



class Counter():
    def __init__(self):
        self.i = 0
    def next(self):
        self.i=self.i+1
        return ""
    def reset(self):
        self.i = 0
        return ""
class Base():
    _Separate_1 = "|-#1-|"
    _Separate_2 = "|-#2-|"
    def _combine_list(self,l):
        if l == []:
            return ""
        r = ""
        for x in l:
            r = r + self._Separate_1 + x
        return r[6:]
    def _combine_questions(self,l):
        if l == []:
            return ""
        r = ""
        for x in l:
            r = r + self._Separate_1 + x.Name
        return r[6:]    
    def _decombine_list(self,s):
        t = s.split(self._Separate_1)
        if t == ['']:
            t = []
        return t
    def _combine_2d_list(self,l):
        if l == []:
            return ""
        r = ""
        for x in l:
            s = ""
            for y in x:
                s = s + self._Separate_2 + str(y)
            r = r + self._Separate_1 + s[6:]
        return r[6:]
    def _decombine_2d_list(self,s):
        l = s.split(self._Separate_1)
        r = []
        for x in l:
            t = []
            xt = x.split(self._Separate_2)
            for y in xt:
                try:
                    t.append(int(y))
                except:
                    t.append(y)
            r.append(t)
        return r
    def _combine_time(self,t):
        l = []
        l.append(str(t.year))
        l.append(str(t.month))
        l.append(str(t.day))
        l.append(str(t.hour))
        l.append(str(t.minute))
        l.append(str(t.second))
        return self._combine_list(l)
    def _decombine_time(self,s):
        t = self._decombine_list(s)
        et = datetime.datetime(int(t[0]),int(t[1]),int(t[2]),int(t[3]),int(t[4]),int(t[5]))
        return et
        
# Question class performing logic on the Questions_Pool and Question database
class Question(Base,database.Questions_db):

    # Returns list of surveys containing specified question
    def used_in_survey(self):
        sp = Surveys_Pool()
        sl = sp.Show()
        l = []
        for s in sl:
            for x in s.Question_list:
                if x.Name == self.Name:
                    l.append(s.Name)
                    break
            for x in s.Optional_Question_list:
                if x.Name == self.Name:
                    l.append(s.Name)
                    break
        return l
    def set_optional(self):
        self._QUESTIONS_POOL = self._OPTIONAL_QUESTIONS_POOL
    # Class init
    # Fields:
    #	- Name [unique identifier]		Format: Q_1, Q_2 etc.
    #	- Commit						Single line description of the content of the question. Used for quick-view when displaying a list of question.
    #	- Description text				More detail description of the content. Used in detailed view of individual question.
    #   - Type							Classification of question [Single choice, Multiple choice, Text based]
    #   - Q_options						List of options for answering the question (Only for single and multiple choice)
    def __init__(self,name = "", commit = "", description_text = "", type = "N_INIT", q_options = ""):
        self.Name = name
        self.Commit = commit
        self.Description_Text = description_text
        self.Type = type
        self.Q_options = q_options 
        
    # Output for printing summary of specified question
    def __str__(self):
        return "Name: " +self.Name + "\n" + "    Commit: "+self.Commit + "\n" + "    Description_Text: "+self.Description_Text + "\n" + "    Type: "+self.Type + "\n" + "    Q_options: %s"%(self.Q_options) + " len: %d"%(len(self.Q_options))
    def say_type(self):
        if self.Type == "C":
            return "Single choice"
        elif self.Type == "MTC":
            return "Multiple choice"
        else:
            return "Text based"
        
    # Logic for processing submission of create_question form.
    # creates initiation of question, performs validity checks.
    def form_init(self,form):
        r = True
        self.Name = form.name.data
        if self.exist():
            flash("Question name can not repeat with previous one!")
            print("Question name can not repeat with previous one!")
            r = False
        self.Commit = form.commit.data
        self.Description_Text = form.question_text.data
        self.Type = form.type.data
        if self.valid_type == False:
            flash("Invalid question type %"%(self.Type))
            print("Invalid question type %"%(self.Type))
            r = False
        if self.Type == "TEXT":
            self.Q_options = []
        else:
            self.Q_options = form.choices.data.split('\r\n')
            n = 0
            for x in self.Q_options:
                if x == "" or x ==" ":
                    self.Q_options.remove(x)
                else:
                    n = n + 1
                    #print("_________________-")
            if n < 2:
                self.Q_options = ["Strongly agree","agree","neutral","do not agree","strongly do not agree"]
        print(str(self))
        print("%d"%(len(self.Q_options)))
        return r
        
    # Creates instance of question form and returns
    def form_create(self):
        form = Forms.Question_Form()
        form.name.data = self.Name
        form.commit.data = self.Commit
        form.question_text.data = self.Description_Text
        form.type.data = self.Type
        t = ""
        for x in self.Q_options:
            t = t + x + "\r\n"
        form.choices.data = t[:-2]
        return form
        
    # Updates existing instance of form with new data
    def form_edit(self,form,old_name):
        r = True
        self.Name = form.name.data
        if self.exist() and (self.Name != old_name):
            flash("Question name can not repeat with previous one!")
            print("Question name can not repeat with previous one!")
            r = False
        self.Commit = form.commit.data
        self.Description_Text = form.question_text.data
        self.Type = form.type.data
        if self.valid_type == False:
            flash("Invalid question type %"%(self.Type))
            print("Invalid question type %"%(self.Type))
            r = False
        if self.Type == "TEXT":
            self.Q_options = []
        else:
            self.Q_options = form.choices.data.split('\r\n')
            for x in self.Q_options:
                if x == "" or x ==" ":
                    self.Q_options.remove(x)
            if self.Q_options == []:
                self.Q_options = ["Strongly agree","agree","neutral","do not agree","strongly do not agree"]
        print(str(self))
        return r
    def file_init(self,qt):
        self.Name = qt[0]
        self.Commit = qt[1]
        self.Description_Text = qt[2]
        self.Type = qt[3]
        if self.Type == 'TEXT':
            self.Q_options = ""
            return
        self.Q_options = self._decombine_list(qt[4])
    def exist(self):
        x = self._get(self.Name)
        if x == 1 or x == False or x == []:
            return False
        else:
            return True
    def valid_type(self):
        if self.Type == 'C' or self.Type == 'MTC' or self.Type == 'TEXT':
            return True
        return False
    def valid_option(self):
        if self.Type == 'TEXT':
            return True
        if type(self.Q_options) == list:
            if self.Q_options ==[]:
                return False
            else:
                return True
        else:
            return False
    def edit_choices(self):
        l = []
        for x in self.Q_options:
            t = (x,x)
            l.append(t)
        return l
    def get_n(self,option):
        i = 0
        n = False
        for x in self.Q_options:
            if x == option:
                n = i
                break
            i = i + 1
        return n

        
# Question Pool class for performing logic on the Question instances in the Questions database
class Questions_Pool(database.Questions_db,Base):
    def set_optional(self):
        self._QUESTIONS_POOL = self._OPTIONAL_QUESTIONS_POOL
    # Performs validity checks on supplied Question instance
    # If passed, Question is added to database
    def Create(self,question):
        c = True
        if question.exist() == True:
            try:
                flash("Repeated question name !")
            except:
                pass
            print("Repeated Question name!")
            c = False
        if question.valid_type() == False:
            try:
                flash("Invalid Question type !")
            except:
                pass
            print("Invalid Question type !")
            c = False
        if question.valid_option() == False:
            try:
                flash("Invalid Option type !")
            except:
                pass
            print("Invalid Option type !")
            c = False
            
        if c == False:
            return False
        
        return self._create(question.Name,question.Commit, question.Description_Text, question.Type, self._combine_list(question.Q_options))    
    
    # Performs validity checks on Question instance and supplied new data
    # If passed, edits existing Question and updates to database
    def Edit(self,question,new_name = False):
        temp_name = new_name
        if temp_name == False:
            temp_name = question.Name
        validity_indicator = True
        if question.exist() == False:
            flash("can't find Question !")
            print("Can't find Question !")
            validity_indicator = False
        if question.valid_type() == False:
            flash("Invalid Question type !")
            print("Invalid Question type !")
            validity_indicator = False
        if validity_indicator == True and question.Type == 'C' or 'MTC':
            if question.valid_option() == False:
                flash("Invalid Option type !")
                print("Invalid Option type !")
                validity_indicator = False
        if validity_indicator == False:
            return False
        l = question.used_in_survey()
        if l != []:
            flash("This question is used in these survey:%s, so can not edit."%l)
            print("This question is used in these survey:%s, so can not edit."%l)
            return False
        return self._edit(question.Name,temp_name,question.Commit, question.Description_Text, question.Type, self._combine_list(question.Q_options))
    
    # Removes question instance from database
    def Delete(self, name):
        question = self.Get(name)
        l = question.used_in_survey()
        if l != []:
            flash("This question is used in these survey:%s, so can not delete."%l)
            print("This question is used in these survey:%s, so can not delete."%l)
            return False
        return self._delete(name)
        
    # Returns private field of name in question instance
    def Get(self,name):
        
        n = self._get(name)
        if n == 1:
            return
        q = Question()
        q.file_init(n[0])
        return q
        
    # returns instance of self
    def Show(self):
        ql = self._select()
        result = []

        for x in ql:
            q = Question()
            q.file_init(x)
            result.append(q)
        return result
        
# Survey class performing logic on the Surveys_Pool and Survey database
class Survey(Base,database.Survey_db):

	# Class init
	# Fields:
    #	- Name					Reference for user-friendly viewing
	#	- Course_semester		*Unique identifier* Only one instance of each course for year/semester. 
	#								Format: MGMT110117S1   -   MGMT1101 for 2017 semester 1
    #	- Commit				Single line description of the content of the question. Used for quick-view when displaying a list of question.
    #	- Description text		More detail description of the content. Used in detailed view of individual question.
	#	- Q_list				List of compulsory questions added to the survey by the admin
	#	- Oq_list				List of optional questions added to the survey by the staff
	#	- State					Current state of the survey:
	#								N_INIT - initialisation by admin
	#								NOT_REVIEWED - approved by admin but not reviewed by staff
	#								A_OPEN - approved by staff and admin. Survey available to students
	#								A_CLOSED - Survey closed by admin
	#								Normal - default
	#	- T_start				Timestamp for survey open
	#	- T_end					Timestamp for survey close
	#	- Attend				Number of responses to survey
	
    def __init__(self,name = "",course_semester = "",commit = "",description_text = "",q_list = [],oq_list = [],state = "N_INIT",t_start = "", t_end = "",attend = []): 
        self.Name = name
        self.Course_Semester = course_semester
        self.Commit = commit
        self.Description_Text = description_text
        self.State = state
        self.Question_list = q_list
        self.Optional_Question_list = oq_list
        self.Answer = self.ans_list()
        self.Start_Time = t_start
        self.End_Time = t_end
        self.Attend_List = attend
    
    # Function for outputting user-friendly string containing data of survey instance
    def __str__(self):
        n_md = []
        n_od = []
        for x in self.Question_list:
            if x == None:
                continue
            n_md.append(x.Name)
        for x in self.Optional_Question_list:
            if x == None:
                continue
            n_od.append(x.Name)
        output_string = "Name: " +self.Name + '\n' + "    Course and semester: "+self.Course_Semester + '\n' + "    Commit: "+self.Commit + '\n' + "    Description_Text: "+self.Description_Text + '\n' + "    State: "+self.State + '\n' + "    Must Do Questions: %s"%(n_md) + '\n' + "    Optional Questions: %s"%(n_od) + '\n' + "    Time Period: "+str(self.Start_Time)+" - "+str(self.End_Time) + '\n' + "    Attend List: %s"%(self.Attend_List) + '\n' + "    Answer: %s"%(self.Answer) + '\n'
        return output_string
                
        
    def file_init(self,s):
        #print(s)
        q = Questions_Pool()
        self.Name = s[0]
        self.Course_Semester = s[1]
        self.Commit = s[2]
        self.Description_Text = s[3]
        
        n = self._decombine_list(s[4])
        self.Question_list = []
        for x in n:
            self.Question_list.append(q.Get(x))
            
        n = self._decombine_list(s[5])
        
        q.set_optional()
        self.Optional_Question_list = []
        for x in n:
            self.Optional_Question_list.append(q.Get(x))

        self.Answer = self._decombine_2d_list(s[6])
        
        self.State = s[7]
        self.Start_Time = self._decombine_time(s[8])
        self.End_Time = self._decombine_time(s[9])
        self.Attend_List = self._decombine_list(s[10])
    
    # Initial creation of survey by admin. Leaves validity checks to calling function.
    def admin_init(self,name, course_semester,commit,description_text,q_list,t_start,t_end):
        self.Name = name
        self.Course_Semester = course_semester
        self.Commit = commit
        self.Description_Text = description_text
        self.State = 'NOT_REVIEWED' 
        self.Question_list = q_list
        self.Optional_Question_list = []
        self.Answer = self.ans_list()
        self.Start_Time = t_start
        self.End_Time = t_end
        self.Attend_List = []
        return True
        
    # Secondary review by staff after initialisation by admin. Adds optional question to oq_list
    def staff_append(self,oq_list):
        if self.State == 'NOT_REVIEWED' :
            
            for x in oq_list:
                if x not in self.Optional_Question_list:
                    self.Optional_Question_list.append(x)
            self.Answer = self.ans_list()
            return True
        else:
            return False
            
    # Function to append data to specified instance of survey. [Only accessible by admin]
    # Default variables are set to default unless a field is required to be updated.
    def edit(self,name = False,course_semester = False,commit = False,description_text = False,q_list = False,oq_list = False,state = False,t_start = False, t_end = False,attend = False): 
        if name is not False:
            self.Name = name
        if course_semester is not False:
            self.Course_Semester = course_semester
        if commit is not False:
            self.Commit = commit
        if description_text is not False:        
            self.Description_Text = description_text
        if state is not False:        
            self.State = state
        if q_list is not False:        
            self.Question_list = q_list
            self.Answer = self.ans_list()
        if oq_list is not False:             
            self.Optional_Question_list = oq_list   
            self.Answer = self.ans_list()
        if t_start is not False:        
            self.Start_Time = t_start
        if t_end is not False:        
            self.End_Time = t_end
        if attend is not False:        
            self.Attend_List = attend
        return True
        
    def return_len(self):
        return len(self.Attend_List)
        
    def _name_list(self):
        l = []
        for x in self.Question_list:
            l.append(x.Name[:])
        for x in self.Optional_Question_list:
            l.append(x.Name[:])
        return l
        
    def say_state(self):
        if self.State == "NOT_REVIEWED":
            return "'Not reviewed survey'"
        elif self.State == "'A_OPENED":
            return 'Admin Opened'
        elif self.State == 'A_CLOSED':
            return "Admin Closed"
        else:
            return "Normal"
            
    def ans_list(self):
        a = []
        for x in self.Question_list:
            if x.Type == 'TEXT':
                a.append([])
            else:
                ans = []
                for y in x.Q_options:
                    ans.append(0)
                a.append(ans)
                
        for x in self.Optional_Question_list:
            if x.Type == 'TEXT':
                a.append([])
            else:
                ans = []
                for y in x.Q_options:
                    ans.append(0)
                a.append(ans)
        return a    
    
    def Change_State(self, state):
        if state == 'NOT_REVIEWED' or state == 'A_OPENED' or state == 'A_CLOSED' or state == 'NORMAL':
            self.State = state
            return True
        else:
            return False
            
    def publish(self):
        if self.State == 'A_OPENED' or self.State == 'A_CLOSED':
            return False
        return self.Change_State("NORMAL")
    def update_answer_attend(self,answer,name):
        print("-------------attend name: %s -------------"%name)
        if self.Attend_List.append(name) == False:
            return False
        i = 0
        for x in self.Question_list:
            if x.Type == "TEXT":
                self.Answer[i].append(answer[i])
            else:
                j = 0
                while j < len(answer[i]):
                    self.Answer[i][j] = self.Answer[i][j] + answer[i][j]
                    j = j + 1
            i = i + 1
        for x in self.Optional_Question_list:
            if x.Type == "TEXT":
                self.Answer[i].append(answer[i])
            else:
                j = 0
                while j < len(answer[i]):
                    self.Answer[i][j] = self.Answer[i][j] + answer[i][j]
                    j = j + 1
            i = i + 1
        print(self.Answer)
        
        return True
    def form_admin_init(self,form):
        qp = Questions_Pool()
        c = True
        self.Name = form.name.data
        if self.exist() == True:
            flash("Repeated Survey name!!!!")
            print("Repeated Survey name!!!!")
            c = False
        self.Course_Semester = form.course.data + "_" + form.semester.data
        if self.valid_Course_semester() == False:
            flash("Invalid Course/semester, please check your input")
            print("Invalid Course/semester, please check your input")
            c = False
        self.Commit = form.commit.data
        self.Description_Text = form.description.data
        self.State = 'NOT_REVIEWED'

        self.Question_list = []
        #print(form.q_list.data)
        for x in form.q_list.data:
            t_q = qp.Get(x)
            if type(t_q) != Question:
                c = False
                flash("Invalid Question name :%s"%x)
                print("Invalid Question name :%s"%x)
            else:
                re = False
                for y in  self.Question_list:
                    if y.Name == t_q.Name:
                        re = True
                        break
                if re == True:
                    continue
                self.Question_list.append(t_q)
                   
        self.Optional_Question_list = []
        qp.set_optional()
        for x in form.oq_list.data:
            t_q = qp.Get(x)
            if type(t_q) != Question:
                c = False
                flash("Invalid Question name :%s"%x)
                print("Invalid Question name :%s"%x)
            else:
                re = False
                for y in  self.Optional_Question_list:
                    if y.Name == t_q.Name:
                        re = True
                        break
                if re == True:
                    continue
                self.Optional_Question_list.append(t_q)
        self.Answer = self.ans_list()
        self.Start_Time = form.time_start.data
        self.End_Time = form.time_end.data
        if self.valid_time() == False:
            flash("Invalid time")
            print("Invalid time")
            c = False
        self.Attend_List = []
        #print(self)
        if self.valid_new_survey() == False:
            
            c = False
        return c
    def form_edit(self,form,old_name):
        c = True
        ql_list = self._name_list()
        self.Name = form.name.data
        if self.exist() and (self.Name != old_name):
            flash("Survey name can not repeat with previous one!")
            print("Survey name can not repeat with previous one!")
            c = False
        qp = Questions_Pool()
        self.Course_Semester = form.course.data + "_" + form.semester.data
        if self.valid_Course_semester(False) == False:
            flash("Course, semester do not exist")
            print("Course, semester do not exist")
            c = False
        self.Commit = form.commit.data
        self.Description_Text = form.description.data
        self.State = form.state.data
        
        self.Question_list = []
        l = form.q_list.data
        for x in l:
            if x == "" or x ==" ":
                l.remove(x)
                continue
            t_q = qp.Get(x)
            if type(t_q) != Question:
                c = False
                flash("Invalid Question name :%s"%x)
                print("Invalid Question name :%s"%x)
            else:
                re = False
                for y in  self.Question_list:
                    if y.Name == t_q.Name:
                        re = True
                        break
                for y in  self.Optional_Question_list:
                    if y.Name == t_q.Name:
                        re = True
                        break
                if re == True:
                    continue
                self.Question_list.append(t_q)
            
        qp.set_optional()
        self.Optional_Question_list = []
        l = form.oq_list.data
        for x in l:
            if x == "" or x ==" ":
                l.remove(x)
                continue
            t_q = qp.Get(x)
            try:
                t_q.set_optional()
            except:
                pass
            if type(t_q) != Question:
                c = False
                flash("Invalid Question name :%s"%x)
                print("Invalid Question name :%s"%x)
            else:
                re = False
                for y in  self.Optional_Question_list:
                    if y.Name == t_q.Name:
                        re = True
                        break
                for y in  self.Question_list:
                    if y.Name == t_q.Name:
                        re = True
                        break
                if re == True:
                    continue
                self.Optional_Question_list.append(t_q)
        if ql_list != self._name_list():
            '''
            print("Answer CHANGED!!!!!")
            print(ql_list)
            print(self._name_list())
            '''
            self.Answer = self.ans_list()
        self.Start_Time = form.time_start.data
        self.End_Time = form.time_end.data
        if self.valid_time() == False:
            flash("Invalid time")
            print("Invalid time")
            c = False
        self.Attend_List = []
        if self.valid_exist_survey() == False:
            c = False
        return c
    def form_create(self):
        form = Forms.c_Survey_Form()
        form.name.data = self.Name
        form.course.data = self.Course_Semester[0:8]
        form.semester.data = self.Course_Semester[9:]
        form.commit.data = self.Commit
        form.description.data = self.Description_Text
        form.state.data = self.State
        form.time_start.data = self.Start_Time
        form.time_end.data = self.End_Time
        

        form.questionlist_init()
        form.q_list.data = [q.Name for q in self.Question_list]

        form.oq_list.data = [q.Name for q in self.Optional_Question_list]
        return form
    def form_update_answer_attend(self,form,name = "Attendee"):
        for attender in self.Attend_List:
            if name == attender:
                flash("can not repeat attend same survey!")
                return False
        st = True
        i = 0
        qp = Questions_Pool()
        ans_list = []
        for x in form:
            if x.type == "HiddenField":
                
                qp.set_optional();
                continue
            if x.type != 'TextAreaField' and x.type != 'SelectField' and x.type != 'SelectMultipleField':
                continue
            q = qp.Get(x.name[1:])
            print(x)
            l = q.Q_options
            t = []
            print(x.name)
            print(x.type)
            print(x.data)
            if x.type == 'TextAreaField':
                ans_list.append(x.data)
            elif x.type == 'SelectField':
                for _ in l:
                    if _ == x.data:
                        t.append(1)
                    else:
                        t.append(0)
                ans_list.append(t)
                #self.Answer[i][?] = self.Answer[i][?] + 1
            elif x.type == 'SelectMultipleField':
                for _ in l:
                    
                    if _ in x.data:
                        t.append(1)
                    else:
                        t.append(0)
                ans_list.append(t)

        print(ans_list)
        if self.update_answer_attend(ans_list,name) == False:
            print("Repeated attend")
            flash("Repeated attend!")
            st = False
        print(self.Attend_List)
        return st
    def form_staff_append(self,form):
        qp = Questions_Pool()
        qp.set_optional()
        c = True
        l = form.oq_list.data
        for x in l:
            if x == "" or x ==" ":
                l.remove(x)
                continue
            t_q = qp.Get(x)
            t_q.set_optional()
            if type(t_q) != Question:
                c = False
                flash("Invalid Question name :%s"%x)
                print("Invalid Question name :%s"%x)
            else:
                re = False
                for y in  self.Question_list:
                    if y.Name == t_q.Name:
                        re = True
                        break
                if re == True:
                    continue
                for y in  self.Optional_Question_list:
                    if y.Name == t_q.Name:
                        re = True
                        break
                if re == True:
                    continue
                self.Optional_Question_list.append(t_q)

        self.Answer = self.ans_list()

        if self.valid_exist_survey() == False:
            c = False
        return c
    def exist(self):
        if self._get(self.Name) == 1:
            #flash("survey do not exist!!!!!")
            #print("survey do not exist!!!!!")
            return False
        else:
            return True
    def valid_State(self):
        if self.State == 'NOT_REVIEWED' or self.State == 'A_OPENED' or self.State == 'A_CLOSED' or self.State == 'NORMAL':
            return True
        #flash("Invalid survey state!")
        print("Invalid survey state!")
        return False    
    def valid_question(self):
        #print(self)
        if type(self.Question_list) == list and type(self.Optional_Question_list) == list:
            if self.Question_list == []:
                #flash("at least one question needed!")
                print("at least one question needed!")
                return False
            else:
                for x in self.Question_list:
                    if type(x) != Question:
                        return False
                    if x.exist() == False:
                        return False
                for x in self.Optional_Question_list:
                    try:
                        x.set_optional()
                    except:
                        pass
                    if type(x) != Question:
                        return False
                    if x.exist() == False:
                        return False
                return True
        else:
            return False  
    def valid_time(self):
        if type(self.Start_Time) == datetime.datetime and type(self.End_Time) == datetime.datetime:
            if self.Start_Time < self.End_Time:
                return True
            else:
                #flash("end time should larger then start time!")
                print("end time should larger then start time!")
                return False
        else:
            return False
    def valid_Course_semester(self,state = True):
        cl = Course_list()
        x = cl.Get(self.Course_Semester)
        if x == 1 or x == False:
            return False
        else:
            if state:
                sp = Surveys_Pool()
                sl = sp.Show()
                for s in sl:
                    if s.Course_Semester==self.Course_Semester:
                        return False
            return True
    def valid_exist_survey(self):
        if self.exist() and self.valid_State() and self.valid_question() and self.valid_time() and self.valid_Course_semester(False):
            return True
        else:
            #flash("invalid survey!")
            #print("invalid survey!")
            return False
    def valid_new_survey(self):
        #print(self)
        if self.exist() == True:
            return False
        if self.valid_State() and self.valid_question() and self.valid_time() and self.valid_Course_semester():
            return True
        else:
            #flash("invalid survey!")
            #print("invalid survey!")
            return False
    def survey_open(self,ID = False):
        if ID != False:
            if ID in self.Attend_List:
                return False
        if self.valid_exist_survey():
            if self.State == 'NOT_REVIEWED'  or self.State == 'A_CLOSED':
                return False
            if self.State == 'A_OPENED' :
                return True
            now = datetime.datetime.now()
            if now < self.End_Time and self.Start_Time < now:
                return True
            else:
                return False
        else:
            #flash("invalid survey!")
            #print("invalid survey!")
            return False
    def create_survey_form(self):
        if self.survey_open():
            class DynamicForm(Form):
                pass
            '''
            setattr(DynamicForm,'name', self.Name)
            setattr(DynamicForm,'course', self.Course_Semester[0:8])
            setattr(DynamicForm,'semester',self.Course_Semester[8:])
            setattr(DynamicForm,'description_text',self.Description_Text)
            '''
            for q in self.Question_list:
                if q.Type == 'C':
                    setattr(DynamicForm, "C"+q.Name, SelectField(q.Description_Text, choices = q.edit_choices(),validators=[Required()]))
                elif q.Type == 'MTC':
                    setattr(DynamicForm, "C"+q.Name, SelectMultipleField(q.Description_Text, choices = q.edit_choices(),validators=[Required()]))
                elif q.Type == 'TEXT':
                    setattr(DynamicForm, "C"+q.Name, TextAreaField(q.Description_Text, validators=[Required()]))
                else:
                    #flash("Invalid question type in %, type = %"%(q.Name,q.Type))
                    print("Invalid question type in %, type = %"%(q.Name,q.Type))
            setattr(DynamicForm, "HIDEN_*%$@$@$#", HiddenField())
            for q in self.Optional_Question_list:
                if q.Type == 'C':
                    l = q.edit_choices()
                    l.insert(0, ("OPTIONAL","OPTIONAL"))
                    setattr(DynamicForm, "O"+q.Name, SelectField("Optional: " + q.Description_Text, choices = l,validators=[Optional()]))
                elif q.Type == 'MTC':
                    l = q.edit_choices()
                    #l.insert(0, ("OPTIONAL","OPTIONAL"))
                    setattr(DynamicForm, "O"+q.Name, SelectMultipleField("Optional: " + q.Description_Text, choices = l,validators=[Optional()]))
                elif q.Type == 'TEXT':
                    setattr(DynamicForm, "O"+q.Name, TextAreaField("Optional: " + q.Description_Text,validators=[Optional()]))
                else:
                    #flash("Invalid question type in %, type = %"%(q.Name,q.Type))
                    print("Invalid question type in %, type = %"%(q.Name,q.Type))
            setattr(DynamicForm,'submit', SubmitField('Submit'))
            return DynamicForm()
        else:
            #flash("survey is not opened! ")
            print("survey is not opened! ")
            return False
    def publish_to_public(self):
        if self.valid_exist_survey() == False:
            return False
        pub_survey = database.Publish_Survey()
        pub_survey.create(self.Name)
        self.State = 'NORMAL'
        sp=Surveys_Pool()
        sl = sp.Show()
        #forced close all other opened survey.
        for s in sl:
            if s.survey_open()==True and s.Course_Semester == self.Course_Semester:
                s.State = "A_CLOSED"
                sp.Update(s)
        return True
    def close_to_public(self):
        pub_survey = database.Publish_Survey()
        pub_survey.Delete(self.Name)
        self.State =  'A_CLOSED'
        return True
    def to_public(self):
        pub_survey = database.Publish_Survey()
        if pub_survey.Get(self.Name) == 1:
            return False
        else:
            return True
 
class Surveys_Pool(database.Survey_db,Base):
    def Create(self, survey):
        if survey.valid_new_survey:
            self._create(survey.Name, survey.Course_Semester, survey.Commit, survey.Description_Text, self._combine_questions(survey.Question_list),self._combine_questions(survey.Optional_Question_list), self._combine_2d_list(survey.ans_list()),survey.State, self._combine_time(survey.Start_Time), self._combine_time(survey.End_Time),self._combine_list([]))
        else:
            return False
    def Update(self, survey,n_name = False):
        if n_name == False:
            n_name = survey.Name
        if survey.valid_exist_survey:
            return self._edit(survey.Name,n_name, survey.Course_Semester, survey.Commit, survey.Description_Text, self._combine_questions(survey.Question_list),self._combine_questions(survey.Optional_Question_list), self._combine_2d_list(survey.Answer),survey.State, self._combine_time(survey.Start_Time), self._combine_time(survey.End_Time),self._combine_list(survey.Attend_List))
        else:
            return False
    def Get(self,name):
        st = self._get(name)
        s = Survey()
        s.file_init(st[0])
        return s
    def Show(self):
        sl = self._select()
        result = []

        for x in sl:
            s = Survey()
            s.file_init(x)
            result.append(s)
        return result
    def Delete(self, name):
        return self._delete(name)
class Course_list(database.Course_db,Base):
    def Create(self,course,semester):
        return self._create(course + '_' + semester)
    def Delete(self,course,semester):
        return self._delete(course + '_' + semester)
    def Get(self,course,semester = False):
        if semester == False:
            return self._get(course)
        return self._get(course + '_' + semester)
    def Show(self):
        l = self._select()
        l2 = []
        for x in l:
            t = []
            t.append(x[0][0:8])
            t.append(x[0][9:])
            l2.append(t)
        return l2
        
class Password(database.Password_db,Base):
    def check_password(self, user_id, password):
        l = self.Get(user_id)
        if l == 1:
            return False
        if l[0][1] == password:
            user = User(user_id)
            login_user(user)
            return True
        else:
            return False
    def get_user(self,user_id):
        l = self.Get(user_id)
        if l == 1:
            return None
        return User(user_id)
    
    def Create(self,id,password,authority):
        return self._create(id,password,authority)
    def Show(self):
        l = self._select()
        return l
        
class Student_Course(database.Student_Course_db,Base):
    def Create(self,id,course_semester):
        return self._create(id,course_semester)
    def Get(self,id,course_semester):
        return self._get(id,course_semester)
    def Show(self):
        l = self._select()
        return l

class User(UserMixin,Password):
    def __init__(self,id):
        self.id = id
        self.authority = self._get_authority()
    def _get_authority(self):
        l = self.Get(self.id)
        return l[0][2]

class Guest(database.Guest_db,Base):
    def __init__(self,form = None):
        if form == None:
            return
        self.id = form.ID.data
        self.password = form.password.data
        self.course_semester = form.course_semester.data.splitlines(False)
        self.Email = form.Email.data
    def __str__(self):
        return "name: "+str(self.id)+"  password: "+self.password+"Email: " + self.Email+"  course_semester: %s"%(self.course_semester)
    def valid(self):
        if self.id.isdecimal() == False:
            flash("ID should only contain decimal! ")
            return False
        pw = Password()
        user = pw.get_user(self.id)
        if user != None:
            flash("repeated id!")
            return False
        #print(self.Get(self.id))
        if self.Get(self.id) != False:
            flash("This id is in the Guest application list!")
            return False
        wrong_qlist = []
        cl = Course_list()
        cs = cl.Show()
        cl_new = []
        for c in cs:
            cl_new.append(c[0]+"_"+c[1])
        valid = True
        for q in self.course_semester:
            if q in cl_new:
                continue
            else:
                wrong_qlist.append(q)
                valid = False
        if valid == False:
            flash("These course_semester do not exist! %s"%wrong_qlist)
            return False
        return True
    def save_file(self):
        if self.valid():
            self.Create(self.id,self.password,self.Email,self._combine_list(self.course_semester))
            return True
        else:
            return False
    def init_file(self,id):
        g = self.Get(id)
        if g == False:
            return g
        self.id = g[0][0]
        self.password = g[0][1]
        self.Email = g[0][2]
        self.course_semester = self._decombine_list(g[0][3])
        return True
         
    def Show(self):
        gl = self._show()
        ngl = []
        for g in gl:
            ng = Guest()
            ng.init_file(g[0])
            ngl.append(ng)
        return ngl
    
    def save_all(self):
        if self.valid:
            pw = Password()
            sc = Student_Course()
            pw.Create(str(self.id),str(self.password),"GUEST")
            for c in self.course_semester:
                sc.Create(str(self.id),c)
            return True
        else:
            return False
    
    