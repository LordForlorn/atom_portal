from B_Layout import *
from managedatabase import *




def UpdateMainPage():
    welcome_label.config(text="Welcome,\n" + selectOne("Employees", "name", "username", f"'{entryLogin.get()}'")[0] + "!")


def ValidateLogin():
    username = entryLogin.get()
    password = entryPssw.get()
    hashed = hash_md5(username+password)
    if  username == "" or password == "":
        print("Login unsuccessful")
        return
    if hashed not in selectOne("Employees", "password", "username", f"'{username}'"):
        print("Login unsuccessful")
        return
    print("Login successful")

    loginFrame.grid_forget()
    ShowPage(mainPageFrame)
    UpdateMainPage()


# places page to the right of the hotbar
def ShowPage(page):
    for i in allFramesList: print(i); i.grid_forget()
    page.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    root.update_idletasks()


numberOfGroups = 0
def AddNewGroup():
    global numberOfGroups

    widget = GroupButton(groupFrame.frame, "Test Group", globalGrid=(numberOfGroups+2,0), size=(screenSize[0]-40, 50))
    widget.config(command=widget.loadGroup)
    groupFrame.addElement(widget)   

    numberOfGroups += 1
    newGroupID = newID()
    widget.groupID = newGroupID
    insert("Groups", newGroupID, "'Test Group', 'Test Description'")
    print(widget.groupID)


def backToMainPage():
    ShowPage(mainPageFrame)
    UpdateMainPage()
    editGroupName(False)



def editGroupName(doCheck=True):
    # madas.exec(f"UPDATE Groups SET name='{groupDetailsName.get()}' WHERE group_id={groupButton.groupID}")
    # print(f"Group {groupButton.groupID} name updated to {groupDetailsName.get()}")
    global Loaded_Group_ID
    print("Globaltest >>>>> ", Loaded_Group_ID)

    def startEdit(): 
        editGroupNameButton.config(text="Save")
        groupDetailsName.config(state="normal")
    def stopEdit(): 
        editGroupNameButton.config(text="Edit")
        groupDetailsName.config(state="disabled")
        exec(f"UPDATE Groups SET name='{groupDetailsName.get()}' WHERE group_id={Loaded_Group_ID}")
        print(f"Group {Loaded_Group_ID} name updated to {groupDetailsName.get()}")

    if doCheck:
        if editGroupNameButton.cget("text") == "Edit":  startEdit()
        else:                                           stopEdit()
    else: stopEdit()




def editProfile(doCheck=True):
    global Loaded_Group_ID

    def startEdit(): 
        editProfileButton.config(text="Save")
        phoneNumberEntry.config(state="normal")
        emailAddressEntry.config(state="normal")
    def stopEdit(): 
        editProfileButton.config(text="Edit Profile")
        phoneNumberEntry.config(state="disabled")
        emailAddressEntry.config(state="disabled")
        # exec(f"UPDATE Employees SET name='{groupDetailsName.get()}' WHERE group_id={Loaded_Group_ID}")
        # print(f"Group {Loaded_Group_ID} name updated to {groupDetailsName.get()}")

    if doCheck:
        if editProfileButton.cget("text") == "Edit Profile":  startEdit()
        else:                                                 stopEdit()
    else: stopEdit()


editProfileButton.config(command=editProfile)




def AddNewMember():
    new_member_button = BetterButton(groupMembersExpand.frame, "Test Member")
    new_member_button.config(command=lambda: ShowPage(profileFrame))
    groupMembersExpand.addElement(new_member_button)
    exec(f"INSERT INTO Employees VALUES({newID()}, 'Test Name', 'Test Surname', 'TestUsername', 'a05752a8e9587922dedeec41e3f57a7b', '2000-01-01', 'Test Position')")
    print("New member added")

addButton.config(command=AddNewMember)



addNewGroupButton.config(command=AddNewGroup)

loginFrame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))  
loginButton.config(command=ValidateLogin)
backToMainPageButton.config(command=backToMainPage)
editGroupNameButton.config(command=editGroupName)

root.mainloop()