import smtplib
from email.message import EmailMessage

# whenever a person signs in send them a message
sender = "Enter your gmail acocunt"
password = "EnterAppKey"
host = ""

def signUpMsg(email,name):

    em = EmailMessage()
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    try:
        # Authentication
        s.login(sender, password)
    except:
        print('Incorrect Username or Password:\n')
        return 
    em["To"] = email
    message = f"""
    Dear {name},
        We welcome you whole heartedily to Ilm Ghar where we teach thousands the way they want to be taught.Explore our wide variety of offered courses from top instructors in your regional languages. Lets learn and grow together
        Regards Ilm Ghar

    """
    em["From"] = sender
    em["Subject"] = "Welcome To Ilm Ghar!"
    em.set_content(message)
    s.send_message(em)
    s.quit()

def signUpMsgInstructor(email,name):

    em = EmailMessage()
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    try:
        # Authentication
        s.login(sender, password)
    except:
        print('Incorrect Username or Password:\n')
        return 
    em["To"] = email
    message = f"""
    Dear {name},
        write your welcome message here

    """
    em["From"] = sender
    em["Subject"] = "Welcome to the Ilm Ghar Team!"
    em.set_content(message)
    s.send_message(em)
    s.quit()


def enrolledInCourse(email,name,course):

    em = EmailMessage()
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    try:
        # Authentication
        s.login(sender, password)
    except:
        print('Incorrect Username or Password:\n')
        return 
    em["To"] = email
    message = f"""
    Dear {name},
        You have successfully enrolled in course {course}. We hope you continue learning and moving towards your target with our hands in yours.
        Regards Ilm Ghar

    """
    em["From"] = sender
    em["Subject"] = "Successful Enrollment"
    em.set_content(message)
    s.send_message(em)
    s.quit()


def enrolledInCourseIns(email,name,course):

    em = EmailMessage()
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    try:
        # Authentication
        s.login(sender, password)
    except:
        print('Incorrect Username or Password:\n')
        return 
    em["To"] = email
    message = f"""
    Dear {name},
       A new student has enrolled in your course {course}.
       Regards Ilm ghar
    """
    em["From"] = sender
    em["Subject"] = "Enrolled in course"
    em.set_content(message)
    s.send_message(em)
    s.quit()

def applicationRecieved(email,name):

    em = EmailMessage()
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    try:
        # Authentication
        s.login(sender, password)
    except:
        print('Incorrect Username or Password:\n')
        return 
    em["To"] = email
    message = f"""
    Dear {name},
        THIS IS AN AUTOMATED RESPONSE
        Your application regarding a career at Ilm ghar has been recieved someone from our hiring team will contact you shortly
        Regards Ilm Ghar
    """
    em["From"] = sender
    em["Subject"] = "Application Recieved"
    em.set_content(message)
    s.send_message(em)
    s.quit()

def applicationRecievedAdmin(email,name):

    em = EmailMessage()
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    try:
        # Authentication
        s.login(sender, password)
    except:
        print('Incorrect Username or Password:\n')
        return 
    em["To"] = 'admin@admin.com'
    message = f"""
    Dear Admin,
        An application for a new instructor has been recieved the application was submitted by {name}, email address {email}

    """
    em["From"] = sender
    em["Subject"] = "New Application"
    em.set_content(message)
    s.send_message(em)
    s.quit()



