import model
import database
import csv
cl = model.Course_list()
pw = model.Password()
sc = model.Student_Course()
#admin:12450 password:ADMIN
pw.Create("12450","ADMIN","ADMIN")
#course list

with open('courses.csv','rt') as r:
    reader = csv.reader(r)
    for line in reader:
        try:
            cl.Create(line[0],line[1])
        except:
            pass
    r.close()
print("update course finsih")

#password
with open('passwords.csv','rt') as r:
    reader = csv.reader(r)
    for line in reader:
        try:
            #print("%s"%line)
            x = line[2].upper()
            #print(x)
            pw.Create(line[0],line[1],x)
            #print(line[0])
        except:
            pass
    r.close()
print("update password finish")

#relationship
with open('enrolments.csv','rt') as r:
    reader = csv.reader(r)
    for line in reader:
        try:
            x = line[1]+"_"+line[2]
            sc.Create(line[0],x)
            
        except:
            pass
    r.close()
print("enrolments finish")

#show
