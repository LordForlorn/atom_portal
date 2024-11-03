import tkinter as tk
from tkinter import ttk
import ctypes
from PIL import Image, ImageTk
import hashlib
from managedatabase import *
from global_variables import *

# ================== Main ==================

root = tk.Tk()
root.title("Phone App")
root.geometry("%dx%d" % screenSize)
root.resizable(False, False)
root.tk.call('tk', 'scaling', 2.0)
ctypes.windll.shcore.SetProcessDpiAwareness(True)
s = ttk.Style()

mainColor = "#fbf5ff"

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

loginFrame = tk.Frame(root)
# loginFrame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

loginFrame.grid_rowconfigure(0, weight=4)
loginFrame.grid_rowconfigure(1, weight=1)
loginFrame.grid_rowconfigure(2, weight=2)
# frame.grid_rowconfigure(3, weight=1)
loginFrame.grid_columnconfigure(0, weight=1)



def hash_md5(value): return hashlib.md5((value).encode()).hexdigest()
# s.configure("TFrame", background=mainColor)

defaultButtonImg = ImageTk.PhotoImage(Image.open("./materials/SquareWhite.png").resize((2000,2000)))
defaultColor = "#f0f0f0"
defaultProfileImg = ImageTk.PhotoImage(Image.open("./materials/default_profile_picture.png").resize((200,200)))
bankLogo = tk.PhotoImage(file="./materials/Atom-bank-logo.png").subsample(3)









# ================== CLASSES ==================

class BetterButton(tk.Button):
    def __init__(self, master, text, image=defaultButtonImg, size=(int(screenSize[0]-20), 50), sticky=tk.N):
        super().__init__(master, text=text, image=image, compound=tk.CENTER, width=size[0], height=size[1])
        self.config(width=size[0], height=size[1])

    def _grid(self, **kwargs): self.grid(kwargs)


Loaded_Group_ID = -1
class GroupButton(tk.Button):
    def __init__(self, master, title, globalGrid=(0,0), image=defaultButtonImg, size=(int(screenSize[0]-20), 50)):
        super().__init__(master, text=title, image=image, compound=tk.CENTER, width=size[0], height=size[1])

        self.groupID = -1
        self.config(width=size[0], height=size[1])

        self.grid(row=globalGrid[0], column=globalGrid[1], padx=5, pady=5, sticky=tk.N)

    def loadGroup(self):
        global Loaded_Group_ID
        groupDetailsName.delete(0, tk.END)
        groupDetailsName.insert(0, selectOne("Groups", "name", "group_id", f"{self.groupID}")[0])

        for page in allFramesList: page.grid_forget()
        groupDetailsFrame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        Loaded_Group_ID = self.groupID

        print(f"Group {self.groupID} loaded")
        print(f"Group {Loaded_Group_ID} loaded")
        root.update_idletasks()


class ExpandableFrame():
    def __init__(self, master, title, bg="grey", defaultHeight=50):
        self.frame = tk.Frame(master, background=bg, width=int(screenSize[0]-6), height=300)
        # self.frame.grid(row=0, column=0, padx=10, pady=30, sticky=tk.N)
        # self.frame.grid_columnconfigure(0, weight=1)

        self.button = BetterButton(self.frame, title, size=(int(screenSize[0]-20), defaultHeight))
        self.button.grid(row=0, column=0, padx=10, pady=(10,100), sticky=tk.N)

        self.defaultHeight = defaultHeight
        self.title = title

        self.button.config(command=self.expand)

        self.elements = []



    def addElement(self, element):
        self.expand()
        self.elements.append(element)
        element.grid(row=len(self.elements), column=0, padx=10, pady=10, sticky=tk.N)
    
    def removeElement(self, element):
        self.elements.remove(element)
        element.grid_forget()

    def expand(self):
        print(f"{self.title} expanded")
        for e in range(len(self.elements)): self.elements[e].grid(row=e+1, column=0, padx=10, pady=10, sticky=tk.N)
        self.button.grid_configure(pady=(10, 70))

        self.frame.update_idletasks()
        self.button.config(command=self.collapse)

    def collapse(self):
        print(f"{self.title} collapsed")
        for element in self.elements: element.grid_forget()
        self.button.grid_configure(pady=(10, 10))

        self.frame.update_idletasks()
        self.button.config(command=self.expand)

    def pack(self):
        self.frame.grid_forget()
        self.frame.pack_configure()
        self.frame.pack()

    def grid(self, **kwargs):
        self.frame.pack_forget()
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid(kwargs)












# ================== LOGIN PAGE ==================

# image
# image = Image.open("./materials/Atom-bank-logo.png")
# image = image.resize((image.width // 3, image.height // 3))


image_label = tk.Label(loginFrame, image=bankLogo)
image_label.image = bankLogo  # reference to avoid garbage collection
image_label.grid(row=0, column=0, pady=10)

# entries
entryFrame = tk.Frame(loginFrame)

# s.configure("entryFrame.TFrame", background=mainColor)

labelLogin = tk.Label(entryFrame, text="Login", font=("Helvetica", 10))
labelLogin.grid(row=0, column=0, pady=10, sticky=tk.E, padx=20)

labelPssw = tk.Label(entryFrame, text="Password", font=("Helvetica", 10))
labelPssw.grid(row=1, column=0, pady=10, sticky=tk.E, padx=20)

entryLogin = tk.Entry(entryFrame, font=("Helvetica", 10))
entryLogin.grid(row=0, column=1, pady=10, padx=20)

entryPssw = tk.Entry(entryFrame, font=("Helvetica", 10))
entryPssw.grid(row=1, column=1, pady=10, padx=20)

entryFrame.grid(row=1, column=0, pady=10)


# login button
loginButton = tk.Button(loginFrame, text="Login", width=30)
# style = tk.Style()
# style.configure("TButton", padding=10, relief="raised", borderwidth=8, font=("Helvetica", 12))
loginButton.grid(row=2, column=0, pady=10)














# ================== MAIN PAGE ==================


mainPageFrame = tk.Frame(root)
mainPageFrame.columnconfigure(0)
welcome_label = tk.Label(mainPageFrame, text="Have a good day!", font=("Helvetica", 24, "bold"))
welcome_label.grid(row=0, column=0, pady=40, padx=20, sticky=tk.W)


# s.configure("subFrame.TFrame", background="red")

class SubFrame(tk.Frame):
    def __init__(self, master, title, bg="grey", size=(int(screenSize[0]-20), 300)):
        super(tk.Frame).__init__()
        self.frame = tk.Frame(master, background=bg, width=size[0], height=size[1])
        self.title = title

    def place(self, **kwargs):
        # self.frame.grid(row=globalGrid[0], column=globalGrid[1], padx=10, pady=30, sticky=tk.N)
        # self.frame.grid_columnconfigure(0, weight=1)
        self.frame.place(kwargs)




annocFrame = SubFrame(mainPageFrame, "Announcements", bg="red")
annocFrame.place(relx=0.5, y=200, anchor="n")

annocName = tk.Label(annocFrame.frame, text=annocFrame.title, font=("Helvetica", 14), background="white")
annocName.place(x=10, y=30, anchor="nw")

# Create a canvas and a scrollbar
canvas = tk.Canvas(annocFrame.frame, bg="lightgrey", width=annocFrame.frame.cget("width"), height=200)
scrollbar = tk.Scrollbar(annocFrame.frame, orient=tk.HORIZONTAL, command=canvas.xview)
scrollable_frame = tk.Frame(canvas, bg="lightgrey")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(xscrollcommand=scrollbar.set)

canvas.grid(row=1, column=0, sticky="ew")
scrollbar.grid(row=2, column=0, sticky="ew")

# Add smaller frames inside the scrollable_frame
for i in range(10):  # Example: 10 smaller frames
    small_frame = tk.Frame(scrollable_frame, bg="white", width=300, height=int(canvas.cget("height"))-10)
    small_frame.grid(row=0, column=i, padx=5, pady=5)

    title_label = tk.Label(small_frame, text=f"Announcement {i+1}", font=("Helvetica", 12), bg="white")
    title_label.pack(pady=5)

    text_label = tk.Label(small_frame, text=f"announcement text {i+1}", font=("Helvetica", 10), bg="white")
    text_label.pack(pady=5)

    small_frame.grid_propagate(False)






groupFrame = ExpandableFrame(mainPageFrame, "Groups", bg="lightgrey")
groupFrame.frame.place(relx=0.5, y=550, anchor="n")

addNewGroupButton = tk.Button(groupFrame.frame, text="Add New Group", image=defaultButtonImg, compound=tk.CENTER, width=screenSize[0]-40, height=50)
addNewGroupButton.grid(row=0, column=0, padx=5, pady=(120,5), sticky=tk.N)
groupFrame.addElement(addNewGroupButton)














# ================== GROUP DETAILS PAGE ==================

groupDetailsFrame = tk.Frame(root)

groupDetailsName = tk.Entry(groupDetailsFrame, font=("Helvetica", 14), background=defaultColor, borderwidth=0, justify=tk.LEFT)
groupDetailsName.pack()
groupDetailsName.config(state = "disabled")

availabilityButton = tk.Button(groupDetailsFrame, text="Availability", width=20)
availabilityButton.pack()

groupMembersButton = tk.Button(groupDetailsFrame, text="Group Members", width=20)
groupMembersButton.pack()

editGroupNameButton = BetterButton(groupDetailsFrame, "Edit", size=(40,40))
editGroupNameButton.pack()

backToMainPageButton = tk.Button(groupDetailsFrame, text="Back to Main Page", width=20)
backToMainPageButton.pack()

groupMembersExpand = ExpandableFrame(groupDetailsFrame, "Test Frame")
addButton = BetterButton(groupMembersExpand.frame, "Add New Member")
# addButton.config(command=lambda: groupMembersExpand.addElement(BetterButton(groupMembersExpand.frame, "Test Member")))
groupMembersExpand.addElement(addButton)
groupMembersExpand.pack()









# ================== PROFILE FRAME ==================

profileFrame = tk.Frame(root)

# Profile Picture
profilePic = defaultProfileImg
profilePicLabel = tk.Label(profileFrame, image=profilePic)
profilePicLabel.image = profilePic  # reference to avoid garbage collection
profilePicLabel.pack(pady=10)

# Edit Profile Button
editProfileButton = tk.Button(profileFrame, text="Edit Profile", width=20)
editProfileButton.pack(pady=10)

# Person's Name Label
personNameLabel = tk.Label(profileFrame, text="Person's Name", font=("Helvetica", 14))
personNameLabel.pack(pady=10)

# Phone Number Entry
phoneNumberEntry = tk.Entry(profileFrame, font=("Helvetica", 10), state="disabled")
phoneNumberEntry.pack(pady=10)

# Email Address Entry
emailAddressEntry = tk.Entry(profileFrame, font=("Helvetica", 10), state="disabled")
emailAddressEntry.pack(pady=10)

# Back to Group Page Button
backToGroupPageButton = tk.Button(profileFrame, text="Back to Group Page", width=20)
backToGroupPageButton.pack(pady=10)

# Function to navigate back to the group page
def back_to_group_page():
    for page in allFramesList:
        page.grid_forget()
    groupDetailsFrame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

backToGroupPageButton.config(command=back_to_group_page)

# Placeholder Frame for Calendar
calendarFrame = tk.Frame(profileFrame, width=200, height=200, bg="grey")
calendarFrame.pack(pady=10)

# Function to enable editing




allFramesList = [loginFrame, mainPageFrame, groupDetailsFrame, profileFrame]
# listbox = tk.Listbox(frame)
# listbox.insert(1, "Item 1")
# listbox.insert(2, "Item 2")
# listbox.insert(3, "Item 3")
# listbox.grid(row=3, column=0, pady=10)

