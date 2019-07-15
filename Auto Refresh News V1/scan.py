import os,time,subprocess,smtplib,ssl,datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
groups=[]
emails=[]
danger=False
def loadStuff():
    with open("base/management.txt","r") as f:
        rl=[i[:-1] for i in f.readlines()]
        for i in rl:
            groups.append([i])
            with open("base/"+i+"-sites.txt","r") as f:
                r=f.readlines()
                groups[-1].append([i[:-1] for i in r])
            with open("base/"+i+"-keywords.txt","r") as f:
                r=f.readlines()
                groups[-1].append([i[:-1].lower() for i in r])
    with open("base/emails.txt","r") as f:
        r=f.readlines()
        for i in r:
            emails.append(i[:-1])
            
def getURL(site,word):
    out="http://www.google.com/search?q="
    site=site.lower()
    site=site.replace(" ","+")
    word=word.replace(" ","+")
    site=site.replace(",","%2C")
    word=word.replace(",","%2C")
    site=site.replace("=","%3D")
    word=word.replace("=","%3D")
    out+=site
    out+="%3A+"
    out+=word
    return out


def sendEmail(group,site,word):
    print("sending email...")
    
    port = 465  # For SSL
    password = "testingPass"
    senderEmail="autoemailmachine@gmail.com"
    subject="Refresh News Tool: "+site+" updated with "+word+" in group:"+group

    text=""
    htmlPart="<html>\n<body>\n<p>\n"
    text+="The publication:"+site+" was updated\n"
    htmlPart+="The publication:<b>"+site+"</b> was updated<br>\n"
    text+="The keyword:"+word+" was updated\n"
    htmlPart+="The keyword:<b>"+word+"</b> was updated<br>\n"
    text+="Group: "+group+"\n"
    htmlPart+="Group: <b>"+group+"</b><br>\n"
    text+=site+" was updated\n"
    htmlPart+='<a href="'+site+'">'+site+'</a><br>\n'
    text+="date and time: "+str(datetime.datetime.now())+" (US format)\n"
    htmlPart+="date and time: "+str(datetime.datetime.now())+" (US format)<br>\n"
    htmlPart+="</p>\n</body>\n</html>"


    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(senderEmail, password)
        for i in emails:
            message=MIMEMultipart("alternative")
            message["Subject"]=subject
            message["From"]=senderEmail
            message["To"]=i
            part1=MIMEText(text,"plain")
            part2=MIMEText(htmlPart,"html")
            message.attach(part1)
            message.attach(part2)
            
            server.sendmail(senderEmail,i,message.as_string())
            
    print("email sent")

def getHTML(url):
    out=""
    res=subprocess.check_output(["curl",url])
    out=res.lower()
    return out

loadStuff()
urlsByGroup=[]
KeyCountByGroup=[]
for group in groups:
    temp=[]
    temp2=[]
    for site in group[1]:
        temp.append([])
        temp2.append([])
        for keyword in group[2]:
            temp[-1].append(getURL(site,keyword))
            temp2[-1].append(getHTML(temp[-1]).count(keyword.encode()))
    urlsByGroup.append([i for i in temp])
    KeyCountByGroup.append([i for i in temp2])
print(urlsByGroup)

while True:
    try:
        for i,group in enumerate(urlsByGroup):
            for j,site in enumerate(group):
                for k,url in enumerate(site):
                    temp=getHTML(url).count(groups[i][2][k].encode())
                    if temp!=KeyCountByGroup[i][j][k]:
                        print(url,"changed")
                        sendEmail(groups[i][0],groups[i][1][j],groups[i][2][k])
    except Exception as e:
        print(e)
        print("ERROR, PGROGRAM STOPPED")
        input("press enter to close")
