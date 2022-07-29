import mysql.connector
import tkinter

con=mysql.connector.connect(user='root',host='localhost',password='Tan*357498',database='tan_db')
cur=con.cursor()

def create():
    c=Create.get()
    cur.execute(f"create table {c}(Student_ID int,Name varchar(15),Date_of_Birth Date,Age int,Gender varchar(10));")
    
def submit():
    s=Si.get()
    n=Name.get()
    d=Dob.get()
    a=Age.get()
    g=Gen.get()
    ch=Choose.get()
    con=mysql.connector.connect(user='root',password='Tan*357498',host='localhost',database='tan_db')
    cur=con.cursor()
    cur.execute(f"insert into {ch} values('{s}','{n}','{d}','{a}','{g}')")
    con.commit()
    Si.delete(0,tkinter.END)
    Name.delete(0,tkinter.END)
    Dob.delete(0,tkinter.END)
    Age.delete(0,tkinter.END)
    Gen.delete(0,tkinter.END)
    
    
def update():
    l=""
    s=Si.get()
    n=Name.get()
    d=Dob.get()
    a=Age.get()
    g=Gen.get()
    s2=Sit2.get()

    con=mysql.connector.connect(user='root',password='Tan*357498',host='localhost',database='tan_db')
    cur=con.cursor()

    if n!=l:
        cur.execute(f"update StudentDatabase3 set Name='{n}' where Student_ID={s2};")
        con.commit()
        
    elif d!=l:
        cur.execute(f"update StudentDatabase3 set Date_of_Birth='{d}'where Student_ID={s2};")
        con.commit()
        
    elif a!=l:
        cur.execute(f"update StudentDatabase3 set Age='{a}' where Student_ID={s2};")
        con.commit()
      
    elif g!=l:
        cur.execute(f"update StudentDatabase3 set Gender='{g}' where Student_ID={s2};")
        con.commit()

def delete():
    s2=Sit2.get()

    con=mysql.connector.connect(user='root',password='Tan*357498',host='localhost',database='tan_db')
    cur=con.cursor()
    cur.execute(f"delete from StudentDatabase3 where Student_ID='{s2}';")
    con.commit()
    
root=tkinter.Tk()
s=tkinter.StringVar()
n=tkinter.StringVar()
d=tkinter.StringVar()
a=tkinter.StringVar()
g=tkinter.StringVar()
s2=tkinter.StringVar()
c=tkinter.StringVar()
ch=tkinter.StringVar()

global Si
global Name
global Dob
global Age
global Gen
global Sit2
global Create
global Choose
Sit=tkinter.Label(root,text="Student ID")
Sit.grid(column=1,row=1)

Namet=tkinter.Label(root,text="Name")
Namet.grid(column=1,row=2)



Dobt=tkinter.Label(root,text="Date of Birth")

Dobt.grid(column=1,row=3)

Aget=tkinter.Label(root,text="Age")

Aget.grid(column=1,row=4)

Gent=tkinter.Label(root,text="Gender")

Gent.grid(column=1,row=5)

Sit2=tkinter.Label(root,text="Student ID")
Sit2.grid(row=7,column=1)
Create2=tkinter.Label(root,text="Table")
Create2.grid(row=10,column=1)
Choose2=tkinter.Label(root,text="Enter Table Name")
Choose2.grid(row=12,column=1)

Si=tkinter.Entry(root,width=30,textvariable=s)
s.set("Enter")
Si.grid(row=1,column=2)
Name=tkinter.Entry(root,width=30,textvariable=n)
n.set("Enter")
Name.grid(row=2,column=2)
Dob=tkinter.Entry(root,width=30,textvariable=d)
d.set("Enter")
Dob.grid(row=3,column=2)
Age=tkinter.Entry(root,width=30,textvariable=a)
a.set("Enter")
Age.grid(row=4,column=2)
Gen=tkinter.Entry(root,width=30,textvariable=g)
g.set("Enter")
Gen.grid(row=5,column=2)
upsi=tkinter.Entry(root,width=30)
upsi.grid(row=7,column=2)
Sit2=tkinter.Entry(root,width=30,textvariable=s2)
s2.set("Enter")
Sit2.grid(row=7,column=2)
Create=tkinter.Entry(root,width=30,textvariable=c)
c.set("Enter")
Create.grid(row=10,column=2)
Choose=tkinter.Entry(root,width=30,textvariable=ch)
ch.set("Enter")
Choose.grid(row=12,column=2)
       

B=tkinter.Button(root,text="Submit",command=submit)

B.grid(row=6,column=2)
u=tkinter.Button(root,text="Update Record",command=update)
u.grid(row=8,column=2)
d=tkinter.Button(root,text="Delete Record",command=delete)
d.grid(row=9,column=2)
c2=tkinter.Button(root,text="Create Table",command=create)
c2.grid(row=11,column=2)

root.mainloop()
