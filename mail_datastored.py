from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
#database connected in mysql
def databaseconnect():
    myconn = mysql.connector.connect(host="192.168.1.5", user="root", passwd="root", database="demo1")
    return myconn

con=databaseconnect()

# Define the Gmail API scopes required
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    """Authenticate and create a Gmail API service instance"""
    # Set up OAuth 2.0 credentials flow
    flow = InstalledAppFlow.from_client_secrets_file(
        '/home/mano/Downloads/garan31.json', SCOPES)
    credentials = flow.run_local_server(port=0)
   
    # Create a Gmail API service instance
    service = build('gmail', 'v1', credentials=credentials)
    return service

# Authenticate and create a Gmail API service instance and connect device with bluetooth
service = get_gmail_service()

def list_emails(service):
    """Retrieve a list of emails from the Gmail inbox"""
    # Call the Gmail API to retrieve the list of emails
    results = service.users().messages().list(userId='me', maxResults=100).execute()
    emails = results.get('messages', [])

    if not emails:
        print('No emails found.')
    else:
        #print('Emails:')
        for email in emails:
            #print(f'- {email["id"]}')
	    mailmsgdata=service.users().messages().get(userId='me', id=email['id']).execute()
	    subjectget=[dd["name"] for dd in  mailmsgdata if dd["name"]=="subject"][0]
	    getfrommail=[dd["name"] for dd in  mailmsgdata if dd["name"]=="From"][0]
	    maildatastored(email['id'],subjectget,getfrommail)

# Retrieve the list of emails from the Gmail inbox and stored in database
list_emails(service)

def maildatastored(email_id,subjectget,getfrommail):
        try:
	    mycursor = conn.cursor()
	    # Insert the email ID into the database
            mycursor.execute("INSERT INTO emaildata (id,email_id,mail_subject,mail_from) VALUES (NULL,'"+email_id+"','"+subjectget+"','"+getfrommail+"')")
            conn.commit()
	







