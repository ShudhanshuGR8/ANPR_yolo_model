#importing required modules
from email.message import EmailMessage
import ssl
import smtplib
import gspread
from oauth2client.service_account import ServiceAccountCredentials 

#function which is to be called in the other file after reading the plate number and generating the slot number. 
# Its parameters are the licence plate number and the parking slot number. 
# It'll fetch the email id according to the licence plate number and send the email acoordingly. 
def send(plate_number,slot):
    try:
        #estabilishing the connectivity between the google sheet
        scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("sending/gs_credentials.json",scope)
        client = gspread.authorize(creds)

        #The sheet holding the faculty information
        sheet2=  client.open("Parking slots").worksheet("Sheet2") #has details of the owner of vehicle
    except Exception as e:
        print("The connection was not estabilished.")
        return 
    #fetching the required email address
    RecieverDetails = sheet2.row_values(sheet2.find(str(plate_number)).row)

    #preparing the mail contents
    sender = "automatedparkingopen@gmail.com" #email id of sender
    password = "fgccvkxetqnqomps" #password for the sender's account
    reciever = str(RecieverDetails[-1]) #email id of the receiver
    subject = "This is your parking slot" #subject of the email
    body = f"You have to park your vehical at slot number {str(slot)}" #body of the email

    #collecting all the elments of the email message
    e = EmailMessage() #making the message
    e['From'] = sender #setting the from as the sender's email id
    e['To'] = reciever #setting the to as the reciever's email id
    e['Subject'] = subject #setting the subject in the email
    e.set_content(body) #combining the contents

    #creating the context
    con = ssl.create_default_context()

    #sending the email using the smtplib module
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=con) as smtp:
        smtp.login(sender,password) #the account from which it is to be send
        smtp.sendmail(sender,reciever,e.as_string()) #the from,to and content of the email to be sent '''


