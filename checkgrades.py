import requests
import smtplib
import os
with open("currentgradesVal.txt","r") as f:
    current=int(f.read())
with requests.Session() as c:
    loginurl='https://webkiosk.thapar.edu/CommonFiles/UserAction.jsp'
    gradesurl="https://webkiosk.thapar.edu/StudentFiles/Exam/StudentEventGradesView.jsp?x=&exam=1920ODDSEM&Subject=ALL"
    headers={
    "Connection": "keep-alive",
    "Origin": "https://webkiosk.thapar.edu",
    "Referer": "https://webkiosk.thapar.edu/",
    }
    logindata={
    "txtuType": "Member Type",
    "UserType": "S",
    "txtCode": "Enrollment No",
    "MemberCode": os.getenv("RollNumber"),
    "txtPin": "Password/Pin",
    "Password": os.getenv("WebkioskPassword"),
    }
    c.post(loginurl,logindata,headers)
    page=c.get(gradesurl)
    tr= int(page.text.count('tr')/2)
    print(tr)
    if tr>current:
        try:
            msg = """Subject: New Grades Uploaded \n\n Check https://webkiosk.thapar.edu"""
            fromaddr = os.getenv("emailID")
            password = os.getenv("emailIDPassword")
            with open("maillist.txt") as f:
            	toaddrs=f.read().strip().split("\n")
        
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(fromaddr, password)
        
            server.sendmail(fromaddr, toaddrs, msg)
            with open("currentgradesVal.txt","w") as f:
                f.write(str(tr))
            server.quit()
        except:
            server.sendmail(fromaddr,[fromaddr],"Error Occurred")
            server.quit()

