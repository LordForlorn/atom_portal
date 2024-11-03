import sqlite3 as cn
from global_variables import *

myDB = cn.connect("atomdatabase.db")
myCursor = myDB.cursor()
currentGlobalID = 50

def exec(query):
    myCursor.execute(query)
    myDB.commit()


#  DELETING  =================
for i in ["Employees", "Groups", "Availability"]: exec(f"DROP TABLE IF EXISTS {i}")


def newID():
    global currentGlobalID
    currentGlobalID += 1
    return currentGlobalID

     
def insert(table, primary, valueStr):
    exec(f"""INSERT INTO {table} VALUES({primary}, {valueStr})""")

def selectOne(table, searchedField, knownField, knownValue):
    exec(f"""SELECT {searchedField} FROM {table} WHERE {knownField}={knownValue}""")
    return fetchConvert(myCursor.fetchall())

def fetchConvert(fetched):
    if fetched == []: return [None]
    else:
        returnList = []
        for i in range(len(fetched)):
            for j in fetched[i]: returnList.append(j)
        return returnList
    


# ================= Temporary =================

exec("""CREATE TABLE IF NOT EXISTS Employees (
                    employee_id INTEGER PRIMARY KEY,
                    name TEXT,
                    surname TEXT,
                    username TEXT,
                    password TEXT,
                    dob DATE,
                    position TEXT
)""")
exec("""CREATE TABLE IF NOT EXISTS Groups (
                    group_id INTEGER PRIMARY KEY,
                    name TEXT,
                    description TEXT
)""")
exec("""CREATE TABLE IF NOT EXISTS Availability (
                    id INTEGER PRIMARY KEY,
                    employee_id INTEGER,
                    group_id INTEGER,
                    date DATE,
                    start_time TIME,
                    end_time TIME,
                    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id),
                    FOREIGN KEY (group_id) REFERENCES Groups(group_id)
)""")
insert("Employees", newID(), "'Tim', 'Svetenko', 'timsvetenko', '0321635072a101d78b647568dc03b28f', '2001-01-01', 'Developer'")
insert("Employees", newID(), "'testname', 'testsurname', 'q', '099b3b060154898840f0ebdfb46ec78f', '2001-01-01', 'Developer'")
insert("Employees", newID(), "'Kostik', 'KSurname', 'kostik', 'ff162c2d897f52387244225eb2aa2738', '2001-01-01', 'Developer'")
insert("Employees", newID(), "'Adrian', 'ASurname', 'adrianadmin', '5e6e31aa29e388636d29b78ffc131da1', '2001-01-01', 'Developer'")





