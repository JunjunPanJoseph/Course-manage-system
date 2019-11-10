from wtforms import StringField, SubmitField, BooleanField, TextAreaField, DateTimeField, RadioField, SelectField, SelectMultipleField,PasswordField
from wtforms.validators import Required, AnyOf,Email,EqualTo,ValidationError
from flask_wtf import Form
import datetime
import model

#class Question
class Question_Form(Form):
    name = StringField('Name of question, can not repeat', validators=[Required()])
    commit = TextAreaField('Comment of this question', validators=[Required()])
    question_text = TextAreaField('Question:', validators=[Required()])
    choices = TextAreaField("Separate each choice with a new line.")
    type = RadioField('Type of question', choices = [("C",'Single Choice Question'),('MTC','Multiple choices question'),("TEXT",'Text based question')], validators=[Required()])
    submit = SubmitField('Submit')




#class survey
class Survey_Form(Form):
    name = StringField('name of this survey', validators=[Required()])
    course = StringField('course of this survey', validators=[Required()])
    semester = StringField('semester of this survey', validators=[Required()])
    commit = TextAreaField('Commit of this Survey', validators=[Required()])
    description = TextAreaField('The description of this survey',validators=[Required()])
    time_start = DateTimeField('survey start time %Y-%m-%d %H:%M:%S',validators=[Required()])
    time_end = DateTimeField('survey end time %Y-%m-%d %H:%M:%S' ,validators=[Required()])
    q_list = SelectMultipleField("Question List")
    oq_list = SelectMultipleField("Optional Question List")
    submit = SubmitField('Submit')
    def questionlist_init(self):
        qp = model.Questions_Pool()
        ql = qp.Show()
        self.q_list.choices = [(q.Name, q.Name) for q in ql]
        qp.set_optional()
        oql = qp.Show()
        self.oq_list.choices = [(q.Name, q.Name) for q in oql]
        
class Optional_Q(Form):
    oq_list = SelectMultipleField("Optional Question List")
    def questionlist_init(self):
        qp = model.Questions_Pool()
        qp.set_optional()
        oql = qp.Show()
        self.oq_list.choices = [(q.Name, q.Name) for q in oql]
    submit = SubmitField('Submit')
class c_Survey_Form(Form):
    name = StringField('name of this survey', validators=[Required()])
    course = StringField('course of this survey', validators=[Required()])
    semester = StringField('semester of this survey', validators=[Required()])
    commit = TextAreaField('Commit of this Survey', validators=[Required()])
    description = TextAreaField('The description of this survey',validators=[Required()])
    state = RadioField('Type of Survey', choices = [('NOT_REVIEWED','Not reviewed survey' ),('A_OPENED','Admin Opened'),('A_CLOSED',"Admin Closed"),('NORMAL','Normal')], validators=[Required()])
    time_start = DateTimeField('survey start time %Y-%m-%d %H:%M:%S',validators=[Required()])
    time_end = DateTimeField('survey end time %Y-%m-%d %H:%M:%S' ,validators=[Required()])
    q_list = SelectMultipleField("Question List")
    oq_list = SelectMultipleField("Optional Question List")
    def questionlist_init(self):
        qp = model.Questions_Pool()
        ql = qp.Show()
        self.q_list.choices = [(q.Name, q.Name) for q in ql]
        qp.set_optional()
        oql = qp.Show()
        self.oq_list.choices = [(q.Name, q.Name) for q in oql]
    
    submit = SubmitField('Submit')
class Delete_Form(Form):
    submit = SubmitField('Delete it')
class Register_Form(Form):
    ID = StringField('Your ID', validators=[Required()])
    password = PasswordField("Your Password", validators=[Required(),EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    Email = StringField('Your Email, if provided, admin may send your an email if application is successed')
    course_semester = TextAreaField("enter Course_Semester, each separate with a new line")
    submit = SubmitField('Submit')