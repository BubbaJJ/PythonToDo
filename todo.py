import sqlite3
import os
from datetime import date

con = sqlite3.connect('ToDo.db')

def createTable():
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS todo (id INTEGER PRIMARY KEY AUTOINCREMENT, taskName TEXT, createdDate TEXT, dueDate TEXT, finishedDate TEXT, done BOOLEAN)')
    con.commit()

def addTask():
    clearConsole()
    task_name = input('Enter task name: ')
    due_date = input('Enter task end date: [YYYYMMDD] ')
    due_date = due_date[0:4] + '-' + due_date[4:6] + '-' + due_date[6:8]
    today = date.today()
    query = 'INSERT INTO todo (taskName, createdDate, dueDate, done) VALUES ("{}","{}","{}",{})'.format(task_name, today, due_date, 0)
    cur = con.cursor()
    cur.execute(query)
    con.commit()
    print('\n{} has been added to the database. Due date is {}'.format(task_name, due_date))

def finishTask():
    clearConsole()
    print('Mark task finished\n')
    cur = con.cursor()
    count = cur.execute('SELECT COUNT(*) from todo where done = 0')
    if count == 0:
        print('\nNo unfinished task found.')
    else:
        availableIds = []
        for row in cur.execute('SELECT id, taskName from todo WHERE done = 0'):
            print("ID: {} Task Name: {}".format(row[0], row[1]))
            availableIds.append(row[0])
        idToFinsh = int(input('\nEnter ID for the task to mark as done: [0 to cancel] \nSelected ID: '))
    while True:
        if idToFinsh in availableIds:
            today = date.today()
            query = 'UPDATE todo SET done = {}, finishedDate = "{}" WHERE id = {}'.format(1, today, idToFinsh)
            cur.execute(query)
            con.commit()
            print('\n{} has been marked as done.'.format(row[1]))
            break
        else:
            if idToFinsh != 0:
                idToFinsh = int(input('\nEnter ID for the task to mark as done: [0 to cancel] \nSelected ID: '))
                continue
            clearConsole()
            mainMenu()
        
def showAllTasks():
    clearConsole()
    print('All tasks:\n')
    cur = con.cursor()
    for row in cur.execute('SELECT id, taskName, createdDate, dueDate, done from todo'):
        print("ID: {}\t Task Name: {}\t Created: {}\t Due Date: {}\t Done: {}".format(row[0], row[1], row[2],row[3],'Yes' if row[4] == 1 else "No"))

def showAllFinishedTasks():
    clearConsole()
    print('Finished tasks:\n')
    cur = con.cursor()
    count = cur.execute('SELECT COUNT(*) from todo where done = 1')
    if count == 0:
        print('No finished task found.')
    else:
        for row in cur.execute('SELECT id, taskName, createdDate, finishedDate from todo WHERE done = 1'):
            print("ID: {}\t Task Name: {}\t Created: {}\t Finished Date: {}".format(row[0], row[1], row[2],row[3]))

def showAllUnfinishedTasks():
    clearConsole()
    print('Unfinished tasks:\n')
    cur = con.cursor()
    count = cur.execute('SELECT COUNT(*) from todo where done = 0')
    if count == 0:
        print('No unfinished task found.')
    else:
        for row in cur.execute('SELECT id, taskName, createdDate, dueDate from todo WHERE done = 0'):
            print("ID: {}\t Task Name: {}\t Created: {}\t Due Date: {}".format(row[0], row[1], row[2],row[3]))

def resetDb():
    clearConsole()
    choice = int(input('''Are you sure you want to reset the database? 
1. Yes 
2. No

Choice: '''))
    if choice == 1:
        cur = con.cursor()
        cur.execute('DELETE FROM todo')
        con.commit()
        print('\nDatabase has been reset.')
    elif choice == 2:
        clearConsole()
        mainMenu()

def mainMenu():
    choice = int(input('''Main menu:
1. Add task
2. Mark task as finished
3. List all tasks
4. List all finished tasks
5. List all unfinished tasks

9. Reset database
0. Exit program
    
Choice: '''))

    if choice == 0:
        goodbye()
        exit()
    elif choice == 1:
        addTask()
        backToMainMenu()
    elif choice == 2:
        finishTask()
        backToMainMenu()
    elif choice == 3:
        showAllTasks()
        backToMainMenu()
    elif choice == 4:
        showAllFinishedTasks()
        backToMainMenu()
    elif choice == 5:
        showAllUnfinishedTasks()
        backToMainMenu()
    elif choice == 9:
        resetDb()
        backToMainMenu()
    else:
        clearConsole()
        mainMenu()

def greeting():
    print("Welcome to Bubba's ToDo! \n")

def goodbye():
    print("\nGoodbye...")

def clearConsole():
    os.system('cls' if os.name == 'nt' else 'clear')

def backToMainMenu():
    backToMain = input('\nPress any key to return to main menu...')
    clearConsole()

def main():
    greeting()
    createTable()
    while True:
        mainMenu()

if __name__ == '__main__':
    main()