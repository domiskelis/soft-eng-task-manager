# ===== Importing libraries ===========
import os
from datetime import datetime, date

# ==== Utility exception ====
class UserQuit(Exception):
    '''
    Indicates user chose to exit task before reaching the end of a function.
    Used to exit back to the main loop of the program, either from one of the sub-menus
    or after a user chooses to abandon input and exit after a specific prompt.
    '''
    pass

# ===== Functions for main body =======
# ==== Data Processing ====
# These two sets of code were provided by HyperionDev and were moved into their own functions, but otherwise mostly unedited.

def compile_tasklist(task_filename):
    # - Create tasks.txt if it doesn't exist
    if not os.path.exists(task_filename):
        with open(task_filename, "w") as default_file:
            pass

    with open(task_filename, 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    task_list = []
    for t_str in task_data:
        curr_t = {}

        # Split by semicolon and manually add each component
        task_components = t_str.split(";")
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
        curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        curr_t['completed'] = True if task_components[5] == "Yes" else False

        task_list.append(curr_t)

    return task_list

def compile_userlist(user_filename):
    # If no user.txt file, write one with a default account
    if not os.path.exists(user_filename):
        with open(user_filename, "w") as default_file:
            default_file.write("admin;password")

    # Read in user_data
    with open(user_filename, 'r') as user_file:
        user_data = user_file.read().split("\n")

    # Convert to a dictionary
    user_list = {}
    for user in user_data:
        username, password = user.split(';')
        user_list[username] = password

    return user_list

# ==== Menu Options ====
def reg_user():
    '''Adds a new user to the user.txt file'''
    
    # Sub-function for username input and duplicate checks:
    def username_setter():
        # - Request new username and password
        new_username = input("New Username: ")

        # - Check if this user exists; allow retry if duplicate is detected
        if new_username in username_password:
            print(f"A user with username {new_username} already exists; would you like to try with a different username?")
            retry = input("(y/n): ").lower()
            while retry != "y" and retry != "n":
                retry = input("Enter y to retry or n to go back to menu: ").lower()
        
            # - Retry if y, otherwise ends task:
            if retry == "y":
                return username_setter()
            else:
                raise UserQuit
        
        # - Return the new username if it's entered successfully
        return str(new_username)
    
    # Sub-function for password input and password confirmation:
    def password_setter():
        # - Request password
        new_password = input("New Password: ")

        # - Request to confirm new password
        confirm_password = input("Confirm Password: ")

        # - Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
            return str(new_password)

        # - Otherwise, print alert and allow retry
        else:
            print("Passwords do no match; try again? (y/n)")
            retry = input(": ").lower()
            while retry != "y" and retry != "n":
                retry = input("Enter y to retry or n to go back to menu: ").lower()

            # - Allow to retry from the start, otherwise ends task
            if retry == "y":
                return password_setter()
            else:
                raise UserQuit
    
    try:
        # - Run username and password setters, quitting if False is returned
        print()
        new_username = username_setter()
        new_password = password_setter()

        # - If they are the same, add them to the user.txt file,
        username_password[new_username] = new_password

        with open(user_filename, "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))

        # - Confirm process succeeded.
        print(f"User {new_username} succesfully registered.")

    # - If user chooses to not retry username/password assignment, confirm nothing has changed.
    except UserQuit:
        print("No new users added.")

    # - Always pause before return to menu
    finally:
        print()
        os.system('pause')

# The add_task function was left mostly unchanged from the version provided by HyperionDev, except a tweak to check whether
# the assigned task name would be unique.
def add_task():
    '''
    Allow a user to add a new task to task.txt file;
    Prompt a user for the following: 
        - A username of the person whom the task is assigned to,
        - A title of a task,
        - A description of the task and 
        - the due date of the task.
    '''
    # Request inputs
    while True:
        # Username for task must exist
        task_username = input("Username of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            continue
        # Task title must not be duplicate
        task_title = input("Title of Task: ")
        for task in task_list:
            task_title_list = task['title']
            while task_title in task_title_list:
                print(f"Task with title '{task_title}' already exists, please assign a unique title.")
                task_title = input("Title of Task:")

        task_description = input("Description of Task: ")
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break

            except ValueError:
                print("Invalid datetime format. Please use the format specified.")

        # - Close input loop once input has been assigned correctly
        break

    # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    with open(task_filename, "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.\n")

    # - Always pause before return to menu
    os.system('pause')

def view_tasks(mode):
    '''
    Reads all tasks and:
        - if view all was selected, allows to view by complete or incomplete tasks
        - if view mine was selected, displays only relevant matches and allows modifying of incomplete tasks
    '''
    # ==== Joint Functions ====
    # - Sub-function to parse and print task information, used for all tasks
    def print_task(t, task_no = False):
        # Formats a given task object into user-friendly format;
        # If task_no is provided, amend first line to include it.
        if task_no == False:
            disp_str = f" \t| Task: \t {t['title']}\n"
        else:
            disp_str = f"{task_no} \t| Task: \t {t['title']}\n"

        disp_str += f" \t| Assigned to: \t\t {t['username']}\n"
        disp_str += f" \t| Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f" \t| Due Date: \t\t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f" \t| Task Description: \n"
        disp_str += f" \t| \t{t['description']}\n"
        disp_str += line_separator
        print(disp_str)
    
    # - Sub-function to read and print complete tasks
    def find_complete():
        # - Header
        print("\n=========================== COMPLETED TASKS ===========================")

        for t in task_list:
            # Tasks for the current user will always be printed
            if t['username'] == curr_user and t['completed'] == True:
                print_task(t)
            # Other tasks only printed for relevant view_all mode
            elif t['completed'] and mode == 'view_all':
                print_task(t)

        # Now, allow user to either view incomplete tasks or return to menu:
        while True:
            print()
            user_prompt = input("Enter 'vi' to view incomplete tasks, or 'm' to return to menu: ").lower()
            if user_prompt == 'vi':
                return find_todos()
            elif user_prompt == 'm':
                raise UserQuit
            else:
                print("Invalid option.")

    # - Sub-function to read and print incomplete tasks
    def find_todos():
        # - Header
        print("\n=========================== INCOMPLETE TASKS ===========================")
        
        # - Branch depending on if modifying will be available (view_mine) or not (view_all)
        if mode == 'view_mine':
            menu_text = "Enter a task number to modify it, 'vc' to view complete tasks, or 'm' to return to menu: "
            # If viewing own tasks, save incomplete task indices in case user wants to modify them:
            task_dict = {}
            task_no = 0

            for t in task_list:
                if t['username'] == curr_user and t['completed'] == False:
                    # Register the task in task_dict, then print
                    task_no += 1
                    task_dict[task_no] = t['title']
                    print_task(t, task_no)
        
        else:
            menu_text = "Enter 'vc' to view complete tasks, or 'm' to return to menu: "
            for t in task_list:
                if t['completed'] == False:
                    print_task(t)
        
        # - Now, check for user action; only allow modification if in view_mine mode.
        while True:
            print()
            # Allow user to modify a task or return to menu
            task_menu = input(menu_text).lower()

            if task_menu == 'vc':
                return find_complete()    
            elif task_menu == 'm':
                raise UserQuit
            
            # If anything else is entered, check if user is in view_mine and then whether
            # it matches a task; pass to modifier if it does:
            try:
                if mode == 'view_all':
                    print("Invalid option.")
                elif int(task_menu) not in task_dict:
                    raise ValueError
                else:
                    task_no = int(task_menu)
                    return modify_task(task_no, task_dict[task_no])
            except ValueError:
                print("Please select a valid task.")

    # ==== view_mine functions ====
    # - Sub-function to modify the state or description of a task, only called for incomplete tasks
    def modify_task(task_no, task_title):
        # Check what's being done to the file
        print(f"Selected task {task_no}: \"{task_title}\".")
        while True:
            mod_type = input('''Select one of the following options:
1 - mark task as complete
2 - edit assigned user
3 - edit title
4 - edit description
5 - edit due date
m - return to menu: ''').lower()

            # Quit if user changes their mind
            if mod_type == "m":
                raise UserQuit
            # Otherwise, check that input is valid
            elif mod_type not in ["1","2","3","4","5"]:
                print("Invalid option.")
            
            # If input is valid, continue to determine changes. When passing to modify the txt file and task list,
            # completion and due date have different bare text for file and non-string values for use in the task list;
            # Hence, all new info is passed with write-to-file and update-to-list fields separately.
            if mod_type == "1": # Mark complete
                new_data = {'position': 'completed', 'new_file_text': 'Yes\n', 'new_list_val': True}

            elif mod_type == "2": # User
                new_user = input("Enter the user you would like to reassign the task to: ").lower()
                while new_user not in username_password:
                    user_input = input("That user does not exist; try again? (y/n): ").lower()
                    if user_input == "y":
                        new_user = input("Enter the user you would like to reassign the task to: ").lower()
                    elif user_input == "n":
                        raise UserQuit
                    else:
                        print("Invalid option.")
                new_data = {'position': 'username', 'new_file_text': new_user, 'new_list_val': new_user}

            elif mod_type == "3": # Title
                new_title = input("Enter a new title: ")
                new_data = {'position': 'title', 'new_file_text': new_title, 'new_list_val': new_title}

            elif mod_type == "4": # Description
                new_desc = input("Enter a new description: ")
                new_data = {'position': 'description', 'new_file_text': new_desc, 'new_list_val': new_desc}

            elif mod_type == "5": # Due date
                # First, get the old date for comparison
                for t in task_list:
                    if t['username'] == curr_user and t['title'] == task_title:
                        old_date = t['due_date'] 
                while True:
                    try:
                        new_due_date = input("Enter a new due date (YYYY-MM-DD): ")
                        due_date_time = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                        if due_date_time <= old_date:
                            print("New due date must come after old due date.")
                        else:
                            break
                    except ValueError:
                        print("Invalid datetime format. Please use the format specified.")
                
                new_data = {'position': 'due_date', 'new_file_text': new_due_date, 'new_list_val': due_date_time}
            
            # Finally, update the file and task list with new info
            write_task(task_title, new_data)
            # Return to task screen
            return find_todos()

    # - Sub-function called for all succesful task modifications to update task info in the txt file
    def write_task(task_title,new_info_object):
        # - Parse the input info;
        modified_prop = new_info_object['position']
        new_text = new_info_object['new_file_text']
        new_val = new_info_object['new_list_val']

        # - Pinpoint what part of a textline is being modified:
        task_props = list(task_list[0].keys())
        prop_index = task_props.index(modified_prop)

        # - Separate all lines in the task file:
        with open(task_filename, 'r') as task_file:
            all_lines = task_file.readlines()
        
        # - Then, find and replace the line of interest
        for i, line in enumerate(all_lines):
            task_props = line.split(";")
            if task_props[0] == curr_user and task_props[1] == task_title:
                # Replace old info with new info
                task_props[prop_index] = new_text
                new_line = ";".join(task_props)
                all_lines[i] = new_line
        
        # - Finally, recompile the file and refresh task list
        with open(task_filename, 'w') as task_file:
            task_file.writelines(all_lines)

        # - Finally, update the task list variable:
        for t in task_list:
            if t['username'] == curr_user and t['title'] == task_title:
                t[modified_prop] = new_val

        print("Task succesfully edited.")
        os.system('pause')

    # - Quick-access line separator for formatting
    line_separator = f"========================================================================"

    # - Allow user to select which tasks they would like to access:
    while True:
        print()
        menu_select = input('''Select which tasks you would like to view:
1 - completed tasks
2 - incomplete tasks
: ''')

        try:
            if menu_select == "1":
                find_complete()
            elif menu_select == "2":
                find_todos()
            else:
                print("Invalid choice.")
        # - Return to menu once user is done
        except UserQuit:
            break

def display_stats():
    '''
    If the user is an admin they can display statistics about number of users
    and tasks.
    '''
    # - Use a truncated report generate function to get basic stats
    task_stats, user_stats = generate_report(truncated = True)

    # - Print to display
    print_str = f"\n============TASK STATISTICS============\n"
    print_str += f"Total tasks: {task_stats['total']}\n"
    print_str += f"\t Of which complete: {task_stats['complete']:.2f}%\n"
    print_str += f"\t Of which overdue: {task_stats['overdue']:.2f}%\n"
    print_str += f"============USER STATISTICS============\n"
    print_str += f"Total users: {user_stats['total']}\n"
    print_str += f"\t Users with no tasks: {user_stats['no_tasks']}\n"
    print_str += f"\t Users with overdue tasks: {user_stats['overdue']}\n"
    print_str += f"=======================================\n"

    print(print_str)

    # - Always pause before return to menu
    os.system('pause')

def generate_report(truncated = False):
    '''
    If user is admin, generates a task report and user report;
    if the optional argument truncate is True, outputs basic statistics instead of generating a full report.
    '''
    def generate_task_report(truncated = False):
        # Generates information from task file
        total_tasks = 0
        total_completed = 0
        total_overdue = 0

        with open(task_filename,'r') as reader:
            task_list = reader.readlines()
            for line in task_list:
                # Process each task, storing each line in a list for the other function
                task = line.split(";")
                all_tasks.append(task)

                task_due_date = datetime.strptime(task[3], DATETIME_STRING_FORMAT)
                task_completed = True if task[5] == "Yes\n" else False
                
                # Update counters
                total_tasks += 1
                if task_completed:
                    total_completed += 1
                elif task_due_date > curr_date:
                    total_overdue += 1
        
        # Generate implicit information
        total_incomplete = total_tasks - total_completed
        percent_incomplete = (total_incomplete/total_tasks)*100
        percent_overdue = (total_overdue/total_tasks)*100

        # If only generating stats, now output stats:
        if truncated:
            task_stats = {
                'total': total_tasks,
                'complete': 100-percent_incomplete,
                'overdue': percent_overdue
            }
            return task_stats
        # Otherwise, the full code runs to generate a report.

        # Format output
        print_str = f"Total generated tasks: \t\t\t\t\t{total_tasks}\n"
        print_str += f"\t ==========================================\n"
        print_str += f"\t Total tasks completed: \t\t\t{total_completed}\n"
        print_str += f"\t Total tasks still incomplete: \t\t{total_incomplete}\n"
        print_str += f"\t\t Of which overdue: \t\t\t\t{total_overdue}\n"
        print_str += f"\t ==========================================\n"
        print_str += f"\t Percentage of incomplete tasks: \t{percent_incomplete:.2f}%\n"
        print_str += f"\t Percent of tasks overdue: \t\t\t{percent_overdue:.2f}%"

        # Finally, generate report file and return the list of tasks
        with open(task_report_filename, 'w') as writer:
            writer.write(print_str)

    def generate_user_report(truncated = False):
        # Generates information from user file and previously generated task data

        # Firstly, extract all user names:
        all_users = []
        with open(user_filename, 'r') as reader:
            user_list = reader.readlines()
            for user in user_list:
                user_name = user.split(";")[0]
                all_users.append(user_name)

        # If truncated, only sort through basic information:
        if truncated:
            user_stats = {
                'total': len(all_users),
                'no_tasks': 0,
                'overdue': 0
            }

            # Quick check for whether any users don't have tasks or have overdue tasks
            for user in all_users:
                has_tasks = False
                has_overdue = False
                for task in all_tasks:
                    if task[0] == user:
                        has_tasks = True
                        task_due_date = datetime.strptime(task[3], DATETIME_STRING_FORMAT)
                        if task_due_date > curr_date:
                            has_overdue = True
                if not has_tasks:
                    user_stats['no_tasks'] += 1
                elif has_overdue:
                    user_stats['overdue'] += 1
            
            return user_stats
        # Otherwise, run the whole report loop

        # Define task and user count
        total_tasks = len(all_tasks)
        total_users = len(all_users)
        total_str = f"Total registered users: {total_users}\n"
        total_str += f"Total generated tasks: {total_tasks}\n"
        total_str += f"\nIndividual reports:\n"
        total_str += f"\t ==========================================\n"

        # Now, begin writing; user reports will be generated within a loop
        with open(user_report_filename, 'w') as writer:
            writer.write(total_str)

            # Individual data
            for user in all_users:
                user_task_count = 0
                user_completed = 0
                user_overdue = 0

                # Run through relevant tasks
                for task in all_tasks:
                    if task[0] == user:
                        # Process relevant info
                        task_due_date = datetime.strptime(task[3], DATETIME_STRING_FORMAT)
                        task_completed = True if task[5] == "Yes\n" else False
                        
                        # Adjust counts
                        user_task_count += 1
                        if task_completed:
                            user_completed += 1
                        elif task_due_date > curr_date:
                            user_overdue += 1
                
                # For each user, generate implicit data IF they have tasks
                user_task_percent = (user_task_count/total_tasks)*100
                if user_task_count != 0:
                    user_completed_percent = (user_completed/user_task_count)*100
                    user_incomplete_percent = 100-user_completed_percent
                    user_overdue_percent = (user_overdue/user_task_count)*100

                # Format all of user's relevant data
                user_str = f"\t User: {user}\n"
                user_str += f"\t\t Total tasks assigned: \t{user_task_count}\n"
                if user_task_count != 0:
                    user_str += f"\t\t Percent of all tasks: \t{user_task_percent:.2f}%\n"
                    user_str += f"\t\t\t Percent completed: \t\t{user_completed_percent:.2f}%\n"
                    user_str += f"\t\t\t Percent still incomplete: \t{user_incomplete_percent:.2f}%\n"
                    user_str += f"\t\t\t Percent overdue: \t\t\t{user_overdue_percent:.2f}%\n"
                user_str += f"\t ==========================================\n"

                # Finally, write and move on to next user
                writer.write(user_str)
    
    # - Report filenames
    task_report_filename = "task_overview.txt"
    user_report_filename = "user_overview.txt"

    # - Get current date
    curr_date = datetime.today()

    # - List of task data to be populated by task report
    all_tasks = []

    # - If we're only generating stats, run truncated functions
    if truncated:
        return generate_task_report(truncated = True), generate_user_report(truncated = True)
    # - Otherwise, run full loops:

    # - Run sub-functions
    print("\nGenerating task report...")
    generate_task_report()
    print("Generating user report...")
    generate_user_report()

    # - On completion, notify user and pause
    print(f"\nReports generated with filenames {task_report_filename} and {user_report_filename}.\n")
    os.system('pause')

# ==== Log-in upon startup ====
def user_login():
    '''This code reads usernames and password from the user.txt file to 
        allow a user to login.
    '''
    while True:
        print("LOGIN")
        curr_user = input("Username: ")
        curr_pass = input("Password: ")
        if curr_user not in username_password.keys():
            print("User does not exist.")
            continue
        elif username_password[curr_user] != curr_pass:
            print("Wrong password")
            continue
        else:
            print("Login Successful!")
            return curr_user

# ==== Main loop of program ====
def main():
    "Main menu and user interface of the program."

    # - On succesful login, display menu until user exits program.
    while True:
        print()
        # If user is admin, show all options
        if curr_user == 'admin':
            print(f"{menu_options_all}{menu_options_admin}{menu_options_exit}")
        # Otherwise, only show non-admin options
        else:
            print(f"{menu_options_all}{menu_options_exit}")
        
        # Take user input, parsing as lower-case
        menu = input(": ").lower()

        if menu == 'r':
            reg_user()

        elif menu == 'a':
            add_task()

        elif menu == 'va':
            view_tasks('view_all')
                
        elif menu == 'vm':
            view_tasks('view_mine')
                    
        elif menu == 'ds' and curr_user == 'admin': 
            display_stats()
        
        elif menu == 'gr' and curr_user == 'admin':
            generate_report()

        elif menu == 'e':
            print('Thank you for using the Task Manager!')
            exit()

        else:
            print("Invalid choice.")

# ====Global variable set up=====
# Date formatting
DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Task list
task_filename = "tasks.txt"
task_list = compile_tasklist(task_filename)
# User database
user_filename = "user.txt"
username_password = compile_userlist(user_filename)

# Menu options
menu_options_all = ("Select one of the options below:\n"
                    "\tr  - Register a new user\n"
                    "\ta  - Add a new task\n"
                    "\tva - View all tasks\n"
                    "\tvm - View my tasks\n")
menu_options_admin = ("\tds - Display statistics\n"
                    "\tgr - Generate report\n")
menu_options_exit = ("\te  - Exit")

# ====Main Program====
# - Prompt login and determine current user
curr_user = user_login()

# - Display menu and options
main()