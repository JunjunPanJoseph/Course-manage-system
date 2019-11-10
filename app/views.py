from flask import Flask, render_template,session, redirect, url_for, flash,request
from flask_bootstrap import Bootstrap
from flask_login import LoginManager,login_user, current_user, login_required, logout_user
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SubmitField, BooleanField, TextAreaField, DateTimeField, RadioField, SelectField, SelectMultipleField,PasswordField
from wtforms.validators import Required, AnyOf,Email,EqualTo,ValidationError,Optional
import os
import datetime
from app import app, login_manager

from Forms import Question_Form,Survey_Form,Delete_Form,c_Survey_Form,Optional_Q,Register_Form
import model

def AUTHORITY_TEST(authority):
    if current_user.authority != authority and current_user.authority != "ADMIN":
        print("INVALID_AUTHORITY!")
        return False
    return True
@login_manager.user_loader
def load_user(user_id):
    pw = model.Password()
    user = pw.get_user(user_id)
    return user

@app.route("/login",methods = ["Get","POST"])
def login():
    if request.method == "POST":
        pw = model.Password()
        user_id = int(request.form["id"])
        password = request.form["password"]
    
        if pw.check_password(user_id,password):
            return redirect(request.args.get('next') or url_for('index'))
        else:
            flash("Wrong user ID or Password!!!!")
    return render_template("basic_login.html")
@app.route("/Register",methods = ["Get","POST"])
def register():

    form = Register_Form()
   
    if form.validate_on_submit():
        guest = model.Guest(form)
        if guest.valid() == True:
            guest.save_file()
            flash("Your request has been sent.")
            return redirect(url_for("index"))
    form.Email.data = ""
    return render_template("register.html",form = form)
    
@app.route('/',methods=['GET','POST'])
@login_required
def index():
    print(current_user.authority)
    print(current_user.id)
    sc = model.Student_Course()
    if current_user.authority == "STAFF" or current_user.authority == "STUDENT" or current_user.authority == "GUEST":
        sp = model.Surveys_Pool()
        sl = sp.Show()
        cl = []
        for s in sl:
            rv = sc.Get(current_user.id,s.Course_Semester)
            if rv == 1 and current_user.authority != "ADMIN":
                continue
            if s.Course_Semester not in cl:
                cl.append(s.Course_Semester)

        cl.sort()
        scl=sc.Show() 
        cl2=[]
        for x in scl:
            if x[1] == int(current_user.id):
                cl2.append(x[0])
        cl2.sort()
        for x in cl2:
            if x not in cl:
                cl.append(x)
        

        
        if current_user.authority == "STUDENT" or current_user.authority == "GUEST":
            return render_template("student_index.html",ID = current_user.id,surveys = sl,cl=cl)
        else:
            return render_template("staff_index.html",ID = current_user.id,surveys = sl,cl=cl)
    g = model.Guest()
    gl = g.Show()
    return render_template('index.html',guest_list = gl)

@app.route("/guest/<ID>/ADD",methods = ['GET',"POST"])
@login_required
def guest_add(ID):    
    if AUTHORITY_TEST("ADMIN") == False:
        return render_template("INVALID_AUTHORITY.html",a1 = current_user.authority,a2 = "ADMIN")
    g = model.Guest()
    if g.init_file(ID):
        if g.save_all():
            g.Delete(ID)
            flash("Success! id = %s"%ID)
        else:
            flash("fail in save data!")
    else:
        flash("fail in init the guest!")
    return redirect(url_for("index"))
        
@app.route("/guest/<ID>/DELETE",methods = ['GET',"POST"])
@login_required
def guest_delete(ID):    
    if AUTHORITY_TEST("ADMIN") == False:
        return render_template("INVALID_AUTHORITY.html",a1 = current_user.authority,a2 = "ADMIN")
    g = model.Guest()
    g.Delete(ID)
    return redirect(url_for("index"))
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
   
@app.route('/Public')
@login_required
# page for published survey and their result
# should include entries for survey and statistic.
def Public():
    if AUTHORITY_TEST("STAFF") == False:
        return render_template("INVALID_AUTHORITY.html",a1 = current_user.authority,a2 = "STAFF")
    sp = model.Surveys_Pool()
    l = sp.Show()
    return render_template('Public.html' ,surveys = l)
 
@app.route('/Public/result/<Survey_name>')
@login_required
def Survey_result(Survey_name):
    ct = model.Counter()
    ct2 = model.Counter()
    sp = model.Surveys_Pool()
    s = model.Survey()
    s.Name = Survey_name
    if s.exist() == False:
        return render_template('Survey_result.html')
    s = sp.Get(Survey_name)
    '''
    if AUTHORITY_TEST("STAFF") == False:
        if s.to_public():
            pass
        else:
            return render_template("INVALID_AUTHORITY.html",a1 = current_user.authority,a2 = "STAFF")
    '''
    sc = model.Student_Course()
    rv = sc.Get(current_user.id,s.Course_Semester)
    if current_user.authority == "ADMIN":
        return render_template('Survey_result.html', survey = s,c=ct,c2=ct2,a1 = current_user.authority)
    if rv == 1:
        return render_template('display_Survey.html',text = "You Are Not Enrolled in This Course!!!")
    if s.survey_open() == False and s.State != "NOT_REVIEWED":
        return render_template('Survey_result.html', survey = s,c=ct,c2=ct2,a1 = current_user.authority)
    else:
        return render_template('display_Survey.html',text = "Survey result closed")

    
@app.route('/Survey/publish_to_public/<Survey_name>')
@login_required
def Publish_to_public(Survey_name):
    if AUTHORITY_TEST("STAFF") == False:
        return render_template("INVALID_AUTHORITY.html",a1 = current_user.authority,a2 = "STAFF")
    sp = model.Surveys_Pool()
    s = model.Survey()
    s.Name = Survey_name
    if s.exist() == False:
        flash("can't find survey name")
        return redirect(url_for('Survey_Pool'))
    s = sp.Get(Survey_name)
    sc = model.Student_Course()
    rv = sc.Get(current_user.id,s.Course_Semester)
    if rv == 1 and current_user.authority != "ADMIN":
        flash("You Are Not Enrolled in This Course!!!")
        if current_user.authority == "STAFF":
            return redirect(url_for('index'))
        return redirect(url_for('Survey_Pool'))
    s.publish_to_public()
    sp.Update(s)
    if current_user.authority == "STAFF":
        return redirect(url_for('index'))
    
    return redirect(url_for('Survey_Pool'))
    
@app.route('/Survey/close_to_public/<Survey_name>')
@login_required
def Close_to_public(Survey_name):
    if AUTHORITY_TEST("STAFF") == False:
        return render_template("INVALID_AUTHORITY.html",a1 = current_user.authority,a2 = "STAFF")
    sp = model.Surveys_Pool()
    s = model.Survey()
    s.Name = Survey_name
    if s.exist() == False:
        flash("can't find survey name")
        return redirect("/Survey_Pool")
    s = sp.Get(Survey_name)
    sc = model.Student_Course()
    rv = sc.Get(current_user.id,s.Course_Semester)
    if rv == 1 and current_user.authority != "ADMIN":
        flash("You Are Not Enrolled in This Course!!!")
        return redirect("/Survey_Pool")
    s.close_to_public()
    sp.Update(s)
    return redirect("/Survey_Pool")
    
@app.route('/Course_Info')
@login_required
# search for all course information and can display its survey.
def Courese_Info():
    if AUTHORITY_TEST("STAFF") == False:
        return render_template("INVALID_AUTHORITY.html",a1 = current_user.authority,a2 = "STAFF")
    cl = model.Course_list()
    
    return render_template('Course_Info.html',course_list = cl.Show())


@app.route('/Question_Pool', methods=['GET','POST'])
@login_required
# Create, edit Questions
def Question_Pool():
    if AUTHORITY_TEST("STAFF") == False:
        return render_template("INVALID_AUTHORITY.html",a1 = current_user.authority,a2 = "STAFF")
    qp = model.Questions_Pool()
    questions = qp.Show()
    qp.set_optional()
    o_questions = qp.Show()
    if questions == [] and o_questions == []:
        return render_template('Question_Pool.html',a1 = current_user.authority)
    if o_questions == []:
        return render_template('Question_Pool.html', questions = questions,a1 = current_user.authority)
    if questions == []:
        return render_template('Question_Pool.html', o_questions = o_questions,a1 = current_user.authority)
        
    return render_template('Question_Pool.html',questions = questions, o_questions = o_questions,a1 = current_user.authority)

@app.route('/Question/Create/<type>', methods=['GET', 'POST'])
@login_required
def Create_Question(type):
    if (AUTHORITY_TEST("ADMIN") == False) and (AUTHORITY_TEST("STAFF") == False):
        return render_template("INVALID_AUTHORITY.html",a1 = current_user.authority,a2 = "ADMIN or STAFF")
    if type !="NORMAL" and type != "OPTIONAL":
        return render_template("INVALID_AUTHORITY.html",a1 = current_user.authority,a2 = "ADMIN or STAFF")
        
    form = Question_Form()
    
    if form.validate_on_submit():
        q = model.Question()
        qp = model.Questions_Pool()
        
        if type == "OPTIONAL":
            q.set_optional()
            qp.set_optional()
            
            
        if q.form_init(form) == False:
            return render_template('Create_Question.html',form = form)
        else:
            if qp.Create(q) == False:
                flash("Can not create question in question pool!")
                return render_template('Create_Question.html',form = form)
            else:
                return redirect(url_for('Question_Pool'))
    form.type.data="C"
    return render_template('Create_Question.html',form = form)
    
    
@app.route('/Question/Edit/<Question_name>/<type>', methods=['GET', 'POST'])
@login_required
def Edit_Question(Question_name,type):
    if AUTHORITY_TEST("ADMIN") == False:
        return render_template("INVALID_AUTHORITY.html",a1 = current_user.authority,a2 = "ADMIN")
    if type !="NORMAL" and type != "OPTIONAL":
        return render_template("INVALID_AUTHORITY.html",a1 = current_user.authority,a2 = "ADMIN or STAFF")
    qp = model.Questions_Pool()
    q = model.Question()
    if type == "OPTIONAL":
        q.set_optional()
        qp.set_optional()

        
    q.Name = Question_name
    if q.exist() == False:
        return render_template('Edit_Question.html')
    q = qp.Get(Question_name)
    form = Question_Form()
    
    if form.validate_on_submit():
        if type == "OPTIONAL":
            q.set_optional()
            qp.set_optional()
        if q.form_edit(form,Question_name) == False:
            return render_template('Edit_Question.html',form = form)
        else:
            new_name = form.name.data
            q.Name = Question_name
            if qp.Edit(q,new_name) == False:
                flash("Can not edit question in question pool!")
                return render_template('Edit_Question.html',form = form)
            else:
                return redirect(url_for('Question_Pool'))
    form = q.form_create()
    return render_template('Edit_Question.html',form = form)
    
@app.route('/Question/Delete/<Question_name>/<type>', methods=['GET', 'POST'])
@login_required
def Delete_Question(Question_name,type):
    if AUTHORITY_TEST("ADMIN") == False:
        return render_template("INVALID_AUTHORITY.html",a1 = current_user.authority,a2 = "ADMIN")
    if type !="NORMAL" and type != "OPTIONAL":
        return render_template("INVALID_AUTHORITY.html",a1 = current_user.authority,a2 = "ADMIN or STAFF")
    qp = model.Questions_Pool()
    q = model.Question()
    
    if type == "OPTIONAL":
        q.set_optional()
        qp.set_optional()
        
    q.Name = Question_name
    if q.exist() == False:
        return render_template('Delete_Question.html')
    form = Delete_Form()
    
    if form.validate_on_submit():
        if qp.Delete(Question_name) == False:
            flash("Can not delete question in question pool!")
            return render_template('Delete_Question.html',form = form,name = Question_name)
        else:
            return redirect(url_for('Question_Pool'))
    return render_template('Delete_Question.html',form = form,name = Question_name)
    
@app.route('/Survey_Pool')
@login_required
# Create, edit Surveys and publish them
def Survey_Pool():
    if AUTHORITY_TEST("STAFF") == False:
        return render_template("INVALID_AUTHORITY.html",a1 = current_user.authority,a2 = "STAFF")
    if current_user.authority == "STAFF":
        return redirect(url_for('index'))
    sp = model.Surveys_Pool()
    sl = sp.Show()
    cl = []
    for s in sl:
        print(s)
        if s.Course_Semester not in cl:
            cl.append(s.Course_Semester)
    cl.sort()
    return render_template('Survey_Pool.html',surveys = sl,cl=cl)

@app.route('/Survey/Create', methods=['GET', 'POST'])
@login_required
#Create new survey.
def Create_Survey():
    if AUTHORITY_TEST("ADMIN") == False:
        return render_template("INVALID_AUTHORITY.html",a1 = current_user.authority,a2 = "ADMIN")
#create not reviewed survey (by admin)
    s = model.Survey()
    sp = model.Surveys_Pool()
    form = Survey_Form()
    form.questionlist_init()
    if form.validate_on_submit():

        if s.form_admin_init(form) == False:
            #print("***************")
            return render_template('Create_Survey.html',form = form)
        else:
            #print(s)
            if sp.Create(s) == False:
                flash("Can't create survey!")
                print("Can't create survey!")
                return render_template('Create_Survey.html',form = form)
            return redirect(url_for('Survey_Pool'))
    return render_template('Create_Survey.html',form = form)
    
@app.route('/Survey/Delete/<Survey_name>', methods=['GET', 'POST'])
@login_required
def Delete_Survey(Survey_name):
    if AUTHORITY_TEST("ADMIN") == False:
        return render_template("INVALID_AUTHORITY.html",a1 = current_user.authority,a2 = "ADMIN")
    sp = model.Surveys_Pool()
    s = model.Survey()
    s.Name = Survey_name
    if s.exist() == False:
        return render_template('Delete_Survey.html')
    form = Delete_Form()
    
    if form.validate_on_submit():
        if sp.Delete(Survey_name) == False:
            flash("Can not delete survey in survey pool!")
            return render_template('Delete_Survey.html',form = form,name = Survey_name)
        else:
            return redirect(url_for('Survey_Pool'))
    return render_template('Delete_Survey.html',form = form,name = Survey_name)
@app.route('/Survey/Edit/<Survey_name>', methods=['GET', 'POST'])
@login_required
def Edit_Survey(Survey_name):
    if AUTHORITY_TEST("ADMIN") == False:
        return render_template("INVALID_AUTHORITY.html",a1 = current_user.authority,a2 = "ADMIN")
    sp = model.Surveys_Pool()
    s = model.Survey()
    s.Name = Survey_name
    if s.exist() == False:
        return render_template('Edit_Survey.html')
    s = sp.Get(Survey_name)
    form = c_Survey_Form()
    form.questionlist_init()
    if form.validate_on_submit():
        if s.form_edit(form,Survey_name) == False:
            return render_template('Edit_Survey.html',form = form)
        else:
            new_name = form.name.data
            s.Name = Survey_name
            if sp.Update(s,new_name) == False:
                flash("Can not edit Survey in Survey pool!")
                return render_template('Edit_Survey.html',form = form)
            else:
                return redirect(url_for('Survey_Pool'))
    form = s.form_create()
    return render_template('Edit_Survey.html',form = form)

@app.route('/Survey/Publish/<Survey_name>', methods=['GET', 'POST'])
@login_required
#Publish survey for course and publish the link.
def Publish_Survey(Survey_name):
    if AUTHORITY_TEST("STAFF") == False:
        return render_template("INVALID_AUTHORITY.html",a1 = current_user.authority,a2 = "STAFF")
    sp = model.Surveys_Pool()
    s = model.Survey()
    s.Name = Survey_name
    if s.exist() == False:
        if current_user.authority == "STAFF":
            return redirect(url_for('index'))
        return redirect(url_for('Survey_Pool'))
    s = sp.Get(Survey_name)
    s.publish()
    if sp.Update(s) == False:
        flash("Can not Publish Survey!")
    if current_user.authority == "STAFF":
        return redirect(url_for('index'))
    return redirect(url_for('Survey_Pool'))

 
@app.route('/Survey/Review/<Survey_name>', methods=['GET', 'POST'])
@login_required
def Review_Survey(Survey_name):
    if AUTHORITY_TEST("STAFF") == False:
        return render_template("INVALID_AUTHORITY.html",a1 = current_user.authority,a2 = "STAFF")
    sp = model.Surveys_Pool()
    s = model.Survey()
    s.Name = Survey_name
    if s.exist() == False:
        return render_template('Review_Survey.html')
    s = sp.Get(Survey_name)
    sc = model.Student_Course()
    rv = sc.Get(current_user.id,s.Course_Semester)
    if rv == 1 and current_user.authority != "ADMIN":
        flash("You are not enroll in this course!!!!!")
        if current_user.authority == "STAFF":
            return redirect(url_for('index'))
        return render_template('Review_Survey.html',)
    
    form = Optional_Q()
    form.questionlist_init()
    if form.validate_on_submit():
        if s.form_staff_append(form) == False:
            flash("Can not append optional question!")
            return render_template('Review_Survey.html',form = form,survey = s)
        else:
            if s.publish_to_public() == False:
                flash("Can not publish")
                return render_template('Edit_Survey.html',form = form)

            if sp.Update(s) == False:
                flash("Can not edit Survey in Survey pool!")
                return render_template('Edit_Survey.html',form = form)

            return redirect(url_for('Survey_Pool'))
    form.oq_list.data = [oq.Name for oq in s.Optional_Question_list]
    
    return render_template('Review_Survey.html',form = form,survey = s)



 
@app.route('/Survey/display/<Survey_name>', methods=['GET', 'POST'])
@login_required
def survey_display(Survey_name):

    if AUTHORITY_TEST("STUDENT") == False and current_user.authority != "GUEST":
        return render_template("INVALID_AUTHORITY.html",a1 = current_user.authority,a2 = "STUDENT")

    
    sp = model.Surveys_Pool()
    s = model.Survey()
    s.Name = Survey_name
    if s.exist() == False:
        return render_template('display_Survey.html',text = "Survey not exist")
    s = sp.Get(Survey_name)
    
    sc = model.Student_Course()
    rv = sc.Get(current_user.id,s.Course_Semester)
    if rv == 1 and current_user.authority != "ADMIN":
        return render_template('display_Survey.html',text = "You Are Not Enrolled in This Course!!!")
        
    if s.survey_open() == False:
        return render_template('display_Survey.html',text = "Survey is not opened")
    
    form = s.create_survey_form()
    
    if form == False:
        return render_template('display_Survey.html',text = "Can not create form!")
        
    if form.validate_on_submit():
        print(s)
        if s.form_update_answer_attend(form,current_user.id) == False:
            return render_template('display_Survey.html',form = form, survey = s,text = "")
        else:
            if sp.Update(s) == False:
                flash("Can not edit Survey in Survey pool!")
                return render_template('display_Survey.html',form = form, survey = s,text = "")
            else:
                return render_template('Thankyou.html',message = "Thank you for complete survey! ")
            
    return render_template('display_Survey.html',form = form, survey = s,text = "")
    




@app.route('/Admin_Page')
@login_required
#account operation, authority change.
def Admin_Page():
    if AUTHORITY_TEST("ADMIN") == False:
        return render_template("INVALID_AUTHORITY.html",a1 = current_user.authority,a2 = "ADMIN")
    return render_template('Admin_Page.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500
