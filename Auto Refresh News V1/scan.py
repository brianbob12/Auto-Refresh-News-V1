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
    site=site.lower()
    site=site.replace(" ","+")
    word=word.replace(" ","+")
    site=site.replace(",","%2C")
    word=word.replace(",","%2C")
    site=site.replace("=","%3D")
    word=word.replace("=","%3D")
    if site in specialCases.keys():
        out=specialCases[site]
    else:
        out="https://www.ecosia.org/search?q="
        out+='"'+site+'"'
        out+="+"
    out+=word
    return out


def sendEmail(group,site,word,url):
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
    htmlPart+="<a href='"+url+"'>'+url+'</a><br>\n"
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
    #time.sleep(1) << handycap for not getting blocked
    out=res.lower()
    return out
specialCases={
    "ft.com":"https://www.ft.com/search?q=",
    "bloomberg.com":"https://www.bloomberg.com/search?query=",
    "thetimes.co.uk":"https://www.thetimes.co.uk/search?source=search-page&q=",
    "reuters.com":"https://uk.reuters.com/search/news?sortBy=&dateRange=&blob=",
    "spiegel.de":"https://www.spiegel.de/suche/?suchbegriff=",
    "faz.net":"https://www.faz.net/suche/?query="
    }
loadStuff()
urlsByGroup=[]
KeyCountByGroup=[]
threshold=7
loopLimiter=7
triggerHistory=[]
for group in groups:
    temp=[]
    temp2=[]
    triggerHistory.append([])
    for site in group[1]:
        temp.append([])
        temp2.append([])
        triggerHistory[-1].append([])
        for keyword in group[2]:
            temp[-1].append(getURL(site,keyword))
            temp2[-1].append(getHTML(temp[-1][-1]).count(keyword.encode()))
            triggerHistory[-1][-1].append(0)
            print(temp2)
    urlsByGroup.append([i for i in temp])
    KeyCountByGroup.append([i for i in temp2])
print(urlsByGroup)
lastt=time.time()
counter=0
while True:
    try:
        for i,group in enumerate(urlsByGroup):
            for j,site in enumerate(group):
                for k,url in enumerate(site):
                    temp=getHTML(url)
                    print(len(temp),i,j,k)
                    temp=temp.count(groups[i][2][k].encode())
                    if temp!=KeyCountByGroup[i][j][k]:
                        print(url,"changed")
                        print(KeyCountByGroup[i][j][k],(temp))
                        if counter-triggerHistory[i][j][k]<=loopLimiter:
                            print("this is tirggering too often, ignoring")
                            triggerHistory[i][j][k]=counter
                            continue
                        triggerHistory[i][j][k]=counter
                        if abs(temp-KeyCountByGroup[i][j][k])>threshold or groups[i][0][j] in specialCases.keys():
                            KeyCountByGroup[i][j][k]=temp
                            sendEmail(groups[i][0],groups[i][1][j],groups[i][2][k],url)
                            print("taking a break")
                            print ("taking a break",end="")
                            for i in range(4):
                                time.sleep(30)
                                print(".",end="")
                            print()
                        else:
                            print("below threshold")
        print("-"*20)
        print("CYCLE COMPLETE")
        print("time:",time.time()-lastt)
        print("-"*20)
        counter+=1
        lastt=time.time()
    except Exception as e:
        print(e)
        print("ERROR, PGROGRAM STOPPED")
        input("press enter to close")
        exit()
