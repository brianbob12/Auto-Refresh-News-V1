import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
from tkinter import messagebox
import os

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
                groups[-1].append([i[:-1] for i in r])
    with open("base/emails.txt","r") as f:
        r=f.readlines()
        for i in r:
            emails.append(i[:-1])

def updateGroups():
    with open("base/management.txt","w") as f:
        toW=""
        for group in groups:
            toW+=group[0]+"\n"
        f.write(toW)
    for group in groups:
        toW=""
        for i in group[1]:
            toW+=i+"\n"
        with open("base/"+group[0]+"-sites.txt","w") as f:
            f.write(toW)
        toW=""
        for i in group[2]:
            toW+=i+"\n"
        with open("base/"+group[0]+"-keywords.txt","w") as f:
             f.write(toW)
            
def changeDropdown(*args):
    print( tkvar.get() )

def getIndex(x):
    for i,v in enumerate(groups):
        if v[0]==x:
            return i
    if x=="All":
        return -1
def addNew():
    print(elements["entry"].get())
    if xVal==-1:
        for group in groups:
            group[1].append(elements["entry"].get())
    else:
        groups[xVal][1].append(elements["entry"].get())
    updateGroups()
    loadState1(groups[xVal][0])
    elements["entry"].delete(first=0,last=len(elements["entry"].get()))

def addNewKey():
    tad=elements["keyEntry"].get().split(",")
    print(tad)
    if xVal==-1:
        for group in groups:
            [group[2].append(i) for i in tad]
    else:
        [groups[xVal][2].append(i) for i in tad]
    updateGroups()
    loadState1(groups[xVal][0])
    elements["keyEntry"].delete(first=0,last=len(elements["keyEntry"].get()))
    
def removeSite(index):
    values = [elements["listbox"].get(idx) for idx in elements["listbox"].curselection()]
    print(values)
    for value in values:
        for i,v in enumerate(groups[index][1]):
            if v ==value:
                del groups[index][1][i]
    updateGroups()
    loadState2(groups[index][0])
    
def removeKey(index):
    values = [elements["listbox"].get(idx) for idx in elements["listbox"].curselection()]
    print(values)
    for value in values:
        for i,v in enumerate(groups[index][2]):
            if v==value:
                del groups[index][2][i]
    updateGroups()
    loadState3(groups[index][0])
    
def removeGroupPractice(x):
    global danger
    danger=True
    loadState1(x)
    
def removeGroup(x):
    print("removing",x)
    for i,v in enumerate(groups):
        if v[0]==x:
            del groups[i]
            break
    updateGroups()
    loadChoices()
    loadState1(groups[0][0])
    
def removeEmails():
    values = [elements["listbox"].get(idx) for idx in elements["listbox"].curselection()]
    print(values)
    for value in values:
        for i,v in enumerate(emails):
            if v ==value:
                del emails[i]
    toW=""
    for email in emails:
        toW+=email+"\n"
    with open("base/emails.txt","w") as f:
        f.write(toW)
    loadState4()
    
def addEmail():
    emails.append(elements["entry"].get())
    toW=""
    for email in emails:
        toW+=email+"\n"
    with open("base/emails.txt","w") as f:
        f.write(toW)
    elements["entry"].delete(first=0,last=len(elements["entry"].get()))
    loadState4()
    
def addNewGroup():
    print("adding new group")
    groups.append([elements["newEntry"].get(),[],[]])
    updateGroups()
    elements["newEntry"].delete(first=0,last=len(elements["entry"].get()))
    loadChoices()
    loadState1(groups[:-1][0])
    
def clickHandler(x,a,b,c):
    return lambda: removeThing(x,a,b,c)

def clearElements():
    global elements,lsElements
    for elementKey in elements.keys():
        elements[elementKey].grid_forget()
    elements={}
    for elementKey in lsElements.keys():
        for element in lsElements[elementKey]:
            element.grid_forget()
    lsElements={}
    
def loadChoices():
    global choices,choicesMin,tkvar
    choices = [i[0] for i in groups]
    choicesMin=[i[0] for i in groups]
    choices.append("All")
    tkvar.set(choices[0])
    tkvar.trace('w', changeDropdown)


def loadState1(x):
    if not x in choices:
        x=groups[0][0]
    index=getIndex(x)
    tkvar.set(choices[index])
    global buttons,danger,xVal,elements
    if not first:
        global removeButton
        clearElements()
    elements["removeButton"]=tk.Button(myFrame,text="Remove this webpage",command=removeGroup)
    elements["entry"]=tk.Entry(myFrame)
    elements["entry"].configure(width=40)
    elements["entry"].grid(column=2,row=2,columnspan=2)
    elements["addNewButton"]=tk.Button(myFrame,text="Add new publication",command=addNew,bg="light green")
    elements["addNewButton"].grid(column=4,row=2,sticky="WE")
    elements["keyEntry"]=tk.Entry(myFrame)
    elements["keyEntry"].configure(width=40)
    elements["keyEntry"].grid(column=2,row=5,columnspan=2)
    elements["addKeyButton"]=tk.Button(myFrame,text="Add new keywords(seperated by commas)",command=addNewKey,bg="light green")
    elements["addKeyButton"].grid(column=4,row=5,sticky="WE")
    elements["popupMenu"] = tk.OptionMenu(myFrame, tkvar, *choices,command=loadState1)
    elements["popupMenu"].grid(row = 2, column =1)
    elements["countryLabel"]=tk.Label(myFrame,text="Group:")
    elements["countryLabel"].grid(row=1,column=1,sticky="WE")
    elements["newEntry"]=tk.Entry(myFrame)
    elements["newEntry"].configure(width=40)
    elements["newEntry"].grid(column=2,row=6,columnspan=2)
    elements["newButton"]=tk.Button(myFrame,text="Add new country/group",command=addNewGroup,bg="light green")
    elements["newButton"].grid(column=4,row=6,sticky="WE")
    
    xVal=index
    if index!=-1:    
        if danger:
            elements["removeButton"]=tk.Button(myFrame,text="Remove this country/group",command=lambda: removeGroup(x),bg="red")
            elements["removeButton"].grid(column=2,row=7)
            tk.messagebox.showwarning(title="Remove Group",message="This wil delete all website and keywords in the group "+x+".\nClick the button again to confirm.")
            danger=False
        else:
            elements["removeButton"]=tk.Button(myFrame,text="Remove this country/group",command=lambda: removeGroupPractice(x))
            elements["removeButton"].grid(column=2,row=7)
            
    elements["thisB"]=tk.Button(myFrame,text="New",command=goToNew,bg="gray")
    elements["thisB"].grid(column=0,row=0,sticky="EW")
    elements["pub"]=tk.Button(myFrame,text="Publications",command=goToPub)
    elements["pub"].grid(column=1,row=0,sticky="EW")
    elements["keys"]=tk.Button(myFrame,text="Keywords",command=goToKey)
    elements["keys"].grid(column=2,row=0,sticky="EW")
    elements["email"]=tk.Button(myFrame,text="Email",command=loadState4)
    elements["email"].grid(column=3,row=0,sticky="EW")
    elements["launch"]=tk.Button(myFrame,text="Launch",command=loadState5)
    elements["launch"].grid(column=4,row=0,sticky="EW")
    
def loadState2(x):
    clearElements()
    if not x in choices:
        x=groups[0][0]
    index=getIndex(x)
    tkvar.set(choices[index])
    xVal=index
    elements["new"]=tk.Button(myFrame,text="New",command=goToNew)
    elements["new"].grid(column=0,row=0,sticky="EW")
    elements["pub"]=tk.Button(myFrame,text="Publications",command=goToPub,bg="gray")
    elements["pub"].grid(column=1,row=0,sticky="EW")
    elements["keys"]=tk.Button(myFrame,text="Keywords",command=goToKey)
    elements["keys"].grid(column=2,row=0,sticky="EW")
    elements["email"]=tk.Button(myFrame,text="Email",command=loadState4)
    elements["email"].grid(column=3,row=0,sticky="EW")
    elements["launch"]=tk.Button(myFrame,text="Launch",command=loadState5)
    elements["launch"].grid(column=4,row=0,sticky="EW")
    elements["popupMenu"]=tk.OptionMenu(myFrame, tkvar, *choicesMin,command=loadState2)
    elements["popupMenu"].grid(row=2,column=1)
    elements["scrollbar"]=tk.Scrollbar(myFrame)
    elements["scrollbar"].grid(row=3,column=2,sticky="NS")
    elements["listbox"]=tk.Listbox(myFrame,selectmode="extended")
    elements["listbox"].config(yscrollcommand=elements["scrollbar"].set)
    elements["scrollbar"].config(command=elements["listbox"].yview)
    elements["listbox"].grid(row=3,column=1)
    elements["button"]=tk.Button(myFrame,command=lambda: removeSite(index),bg="red",text="Delete Selected")
    elements["button"].grid(row=4,column=1,sticky="EW")
    for i in groups[index][1]:
        elements["listbox"].insert("end",i)

def loadState3(x):
    clearElements()
    if not x in choices:
        x=groups[0][0]
    index=getIndex(x)
    tkvar.set(choices[index])
    xVal=index
    elements["new"]=tk.Button(myFrame,text="New",command=goToNew)
    elements["new"].grid(column=0,row=0,sticky="EW")
    elements["pub"]=tk.Button(myFrame,text="Publications",command=goToPub)
    elements["pub"].grid(column=1,row=0,sticky="EW")
    elements["keys"]=tk.Button(myFrame,text="Keywords",command=goToKey,bg="gray")
    elements["keys"].grid(column=2,row=0,sticky="EW")
    elements["email"]=tk.Button(myFrame,text="Email",command=loadState4)
    elements["email"].grid(column=3,row=0,sticky="EW")
    elements["launch"]=tk.Button(myFrame,text="Launch",command=loadState5)
    elements["launch"].grid(column=4,row=0,sticky="EW")
    elements["popupMenu"]=tk.OptionMenu(myFrame, tkvar, *choicesMin,command=loadState3)
    elements["popupMenu"].grid(row=2,column=1)
    elements["scrollbar"]=tk.Scrollbar(myFrame)
    elements["scrollbar"].grid(row=3,column=2,sticky="NS")
    elements["listbox"]=tk.Listbox(myFrame,selectmode="extended")
    elements["listbox"].config(yscrollcommand=elements["scrollbar"].set)
    elements["scrollbar"].config(command=elements["listbox"].yview)
    elements["listbox"].grid(row=3,column=1)
    elements["button"]=tk.Button(myFrame,command=lambda: removeKey(index),bg="red",text="Delete Selected")
    elements["button"].grid(row=4,column=1,sticky="EW")
    for i in groups[index][2]:
        elements["listbox"].insert("end",i)
def loadState4():
    clearElements()
    elements["new"]=tk.Button(myFrame,text="New",command=goToNew)
    elements["new"].grid(column=0,row=0,sticky="EW")
    elements["pub"]=tk.Button(myFrame,text="Publications",command=goToPub)
    elements["pub"].grid(column=1,row=0,sticky="EW")
    elements["keys"]=tk.Button(myFrame,text="Keywords",command=goToKey)
    elements["keys"].grid(column=2,row=0,sticky="EW")
    elements["email"]=tk.Button(myFrame,text="Email",command=loadState4,bg="gray")
    elements["email"].grid(column=3,row=0,sticky="EW")
    elements["launch"]=tk.Button(myFrame,text="Launch",command=loadState5)
    elements["launch"].grid(column=4,row=0,sticky="EW")
    elements["scrollbar"]=tk.Scrollbar(myFrame)
    elements["scrollbar"].grid(row=3,column=3,sticky="NS")
    elements["listbox"]=tk.Listbox(myFrame,selectmode="extended")
    elements["listbox"].config(yscrollcommand=elements["scrollbar"].set)
    elements["scrollbar"].config(command=elements["listbox"].yview)
    elements["listbox"].config(width=40)
    elements["listbox"].grid(row=3,column=1,columnspan=2)
    elements["button"]=tk.Button(myFrame,command=removeEmails,bg="red",text="Delete Selected")
    elements["button"].grid(row=4,column=1,sticky="EW")
    for i in emails:
        elements["listbox"].insert("end",i)
    elements["entry"]=tk.Entry(myFrame)
    elements["entry"].configure(width=40)
    elements["entry"].grid(column=1,row=5,columnspan=2)
    elements["submit"]=tk.Button(myFrame,text="Add new email",command=addEmail,bg="light green")
    elements["submit"].grid(column=3,row=5)
def loadState5():
    clearElements()
    elements["new"]=tk.Button(myFrame,text="New",command=goToNew)
    elements["new"].grid(column=0,row=0,sticky="EW")
    elements["pub"]=tk.Button(myFrame,text="Publications",command=goToPub)
    elements["pub"].grid(column=1,row=0,sticky="EW")
    elements["keys"]=tk.Button(myFrame,text="Keywords",command=goToKey)
    elements["keys"].grid(column=2,row=0,sticky="EW")
    elements["email"]=tk.Button(myFrame,text="Email",command=loadState4)
    elements["email"].grid(column=3,row=0,sticky="EW")
    elements["launch"]=tk.Button(myFrame,text="Launch",command=loadState5,bg="gray")
    elements["launch"].grid(column=4,row=0,sticky="EW")
    elements["button"]=tk.Button(myFrame,text="GO",command=go,bg="lime")
    elements["button"].grid(column=1,row=1,columnspan=3,sticky="NSEW")
    
def go():
    os.system("start scan.py")
def goToNew():
    print("go to new")
    loadState1(groups[0][0])
def goToPub():
    print("go to pub")
    loadState2(groups[0][0])
def goToKey():
    print("go to key")
    loadState3(groups[0][0])

loadStuff()
elements={}
lsElements={}
xVal=0
root=tk.Tk()
root.title("Auto Refresh News V1")
myFrame=tk.Frame(root)
myFrame.grid(column=0,row=0, sticky="NS" )
myFrame.columnconfigure(0, weight = 1)
myFrame.rowconfigure(0, weight = 1)
myFrame.pack(pady = 0, padx = 0)

tkvar = tk.StringVar(root)
choices=[]
choicesMin=[]
loadChoices()


first=True
loadState1(choices[0])
first=False

root.mainloop()


