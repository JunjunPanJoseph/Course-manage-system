import sqlite3
#MODEL
class Config():
    
    
    _DATABASE = 'database.db'
    
    _PASSWORD = 'PASSWORD'
    _COURSE_LIST = 'COURSE_LIST'
    _STUDENT_COURSE = 'STUDENT_COURSE'
    _QUESTIONS_POOL = 'QUESTIONS_POOL'
    _OPTIONAL_QUESTIONS_POOL = 'OPTIONAL_QUESTIONS_POOL'
    _SURVEY = ' SURVEY'
    _PUBLISH_LIST = "PUBLIC_RESULT"
    
   
        
class db_operation(Config):
    def _db_select(self, query):
        with sqlite3.connect(self._DATABASE) as connection:
            try:
                cursorObj = connection.cursor()
                rows = cursorObj.execute(query)
                connection.commit()
                results = []
                for row in rows:
                    results.append(row)
                cursorObj.close()
                return results
            except:
                return False
        return False
        
    def _db_cursor(self,query):
        with sqlite3.connect(self._DATABASE) as connection:
            try:
                cursorObj = connection.cursor()
                cursorObj.execute(query)
                connection.commit()
                cursorObj.close()
                return True
            except:
                return False
        return False
        
    def _Select(self, table):
        query = "SELECT *  from " + table
        return self._db_select(query)
        
    def _Get(self, name, table):
        query = "SELECT *  from " + table + " WHERE NAME = '" + name + "'"
        n = self._db_select(query)
        if n == []:
        #can't find this name: return 1
            return 1
        else:
            return n
            
    def _Delete(self, name, table):
        query = "DELETE FROM " +  table + " WHERE NAME = '" + name + "'"
        return self._db_cursor(query)

class Questions_db(db_operation):
    def _select(self):
        return self._Select(self._QUESTIONS_POOL)
        
    def _get(self,name):
        return self._Get(name,self._QUESTIONS_POOL)
    
    def _delete(self, name):
        return self._Delete(name, self._QUESTIONS_POOL)
    
    def _create(self, name, com, description_text, type, q_text = ""):
        text ="'" + name + "', '" + com + "', '" + description_text + "', '" + type + "', '" + q_text + "'"
        query = "INSERT into " + self._QUESTIONS_POOL + " (NAME, COM,  DESCRIPTION_TEXT, TYPE, Q_TEXT) values (" + text + ")"
        return self._db_cursor(query)
        
    def _edit(self, name,new_name, com, description_text, type, q_text = ""):
        if self.Get(name) == False:
        
            return 1
        text ="NAME = '"+new_name+"', COM = '" + com+"', DESCRIPTION_TEXT = '"+ description_text +"',  TYPE = '"+ type +"', Q_TEXT = '" + q_text+"'"
        query = "UPDATE " + self._QUESTIONS_POOL + " SET " + text + " WHERE NAME = '" + name + "'"
        return self._db_cursor(query)
    
class Survey_db(db_operation):
    def _select(self):
        return self._Select(self._SURVEY)
        
    def _get(self,name):
        return self._Get(name,self._SURVEY)
    
    def _delete(self, name):
        return self._Delete(name, self._SURVEY)
        
    def _create(self, name, course_semester, com, description_text, q_list, oq_list, answer, state, t_start, t_end, attendence):
        text ="'" + name + "', '"+ course_semester + "', '" + com + "', '" + description_text + "', '" + q_list + "', '" + oq_list + "', '" + answer + "', '" + state + "', '" + t_start + "', '" + t_end + "', '" +  attendence + "'"
        query = "INSERT into " + self._SURVEY + " (NAME, COURSE_SEMESTER, COM,  DESCRIPTION_TEXT, Q_LIST, OQ_LIST, ANSWER, STATE, T_START, T_END, ATTENDENCE_RECORD) values (" + text + ")"
        
        return self._db_cursor(query)
        
    def _edit(self, name,new_name,  course_semester, com, description_text, q_list, oq_list, answer, state, t_start, t_end, attendence):
        if self.Get(name) == False:
            return 1
        text ="NAME = '"+new_name+"', COURSE_SEMESTER = '" +course_semester+"', COM = '" + com+"', DESCRIPTION_TEXT = '"+ description_text +"',  Q_LIST = '"+ q_list +"', OQ_LIST = '" + oq_list +"', ANSWER = '" + answer +"', STATE = '" + state +"', T_START = '" + t_start +"', T_END = '" + t_end +"', ATTENDENCE_RECORD = '" + attendence+"'"
        query = "UPDATE " + self._SURVEY  + " SET " + text + " WHERE NAME = '" + name + "'"
        return self._db_cursor(query)

class Course_db(db_operation):
    def _select(self):
        return self._Select(self._COURSE_LIST)
     
    def _create(self, course_semester):
        query =  "INSERT into " + self._COURSE_LIST +" (COURSE_SEMESTER) values ('"+ course_semester+"')"
        print("%s"%query)
        return self._db_cursor(query)
        
    def _delete(self, course_semester):
        query = "DELETE FROM " +  self._COURSE_LIST + " WHERE COURSE_SEMESTER = '" + course_semester + "'"
        return self._db_cursor(query)
        
    def _get(self,course_semester):
        query = "SELECT *  from " + self._COURSE_LIST + " WHERE COURSE_SEMESTER = '" + course_semester + "'"
        n = self._db_select(query)
        
        if n == []:
        #can't find this name: return 1
            return 1
        else:
            return n
        
class Password_db(db_operation):
    def _select(self):
        return self._Select(self._PASSWORD)
     
    def _create(self, id, password, authority):
        query =  "INSERT into " + self._PASSWORD +" (ID, PASSWORD, AUTHORITY) values ("+ id + ",'" + password + "','"+ authority +"')"
        print(query)
        return self._db_cursor(query)
        
    def Delete(self, id):
        query = "DELETE FROM " +  self._PASSWORD + " WHERE ID = " + str(id)
        return self._db_cursor(query)
        
    def Get(self,id):
        query = "SELECT *  from " + self._PASSWORD + " WHERE ID = " + str(id)
        n = self._db_select(query)
        if n == []:
        #can't find this name: return 1
            return 1
        else:
            return n
        
    def Edit(self, id, password, authority):
        if self.Get(id) == False:
            return 1
        text ="ID = '"+id+"', PASSWORD = '" + password+"', AUTHORITY = '"+ authority +"'"
        query = "UPDATE " + self._PASSWORD + " SET " + text + " WHERE ID = '" + id + "'"
        return self._db_cursor(query)
        
class Student_Course_db(db_operation):
    def _select(self):
        return self._Select(self._STUDENT_COURSE)
     
    def _create(self, id, course_semester):
        query =  "INSERT into " + self._STUDENT_COURSE +" (COURSE_SEMESTER, ID) values ('"+ course_semester + "','" + id + "')"
        return self._db_cursor(query)
        
    def _get(self,id, course_semester):
        query = "SELECT *  from " + self._STUDENT_COURSE + " WHERE ID = '" + id + "' AND COURSE_SEMESTER = '" + course_semester +"'"
        n = self._db_select(query)
        
        if n == []:
        #can't find this name: return 1
            return 1
        else:
            return n

class Publish_Survey(db_operation):
    def select(self):
        return self._Select(self._PUBLISH_LIST)
     
    def create(self,name):
        query =  "INSERT into " + self._PUBLISH_LIST +" (NAME) values ('"+ name + "')"
        print(query)
        return self._db_cursor(query)
        
    def Delete(self, name):
        query = "DELETE FROM " +  self._PUBLISH_LIST + " WHERE NAME = '" + name + "'"
        return self._db_cursor(query)
        
    def Get(self,name):
        query = "SELECT *  from " + self._PUBLISH_LIST + " WHERE NAME = '" + name + "'"
        n = self._db_select(query)
        if n == []:
        #can't find this name: return 1
            return 1
        else:
            return n










