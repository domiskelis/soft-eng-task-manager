# Software Engineering: Task Manager
A python program to manage and edit employee user data and assigned tasks.

## Information on Task Prompt

The HyperionDev task prompt provided a skeleton version of this program as one continuous block of code; the log-in code, code to compile task and user lists and the code to add a new task were provided and unchanged beyond moving them into their own separate functions to be called as required.  
  
The task itself was to restructure the code and add missing utility; extra steps I took include:  
- Storing the entire software loop in a main function, as well as storing all code for intialisation and sorting into their own functions  
- Pausing the terminal after any task is executed, allowing the user to see the confirmation before returning to the menu;  
- When viewing own tasks, prompting the user on whether completed or due tasks were displayed, allowing to filter follow-up actions better (i.e. task editing, which is only valid for incomplete tasks);  
- Filtering admin-only actions so that they are only viewable in the menu and accessible if the user is admin;  
- On incorrect or invalid input, instead of restarting to main menu, the program prompts for new input or provides the option to abort current task and return to menu;  
- Repurposing and condensing several actions through the use of function inputs:  
- The action to display task statistics uses a truncated version of the generate report function;  
  - "View all" and "view mine" commands both use the same functions, using function parameters to determine output and what further user actions are allowed  
- Adding further actions when modifying an incomplete task, namely:  
  - Tasks can be reassigned to a different user  
  - Tasks can be renamed or have their description changed  
  - The due date can be pushed forwards (but never backwards)  
  
## Actions

When the code is run, a log-in determines and stores what user is accessing the program.  

All users can:  
- Register a new user  
  - This adds a new pair of username-password into the user file and list  
  - Repeat usernames are not allowed  
- Add a new task  
  - This adds a new task to the task file and list, prompting for relevant information  
  - The assigned user must be in the user file, and repeat task names are not allowed  
- View all tasks  
  - This prints out all the tasks stored in the task file, allowing filtering by either complete or incomplete tasks.  
- View own tasks  
  - This prints out only tasks whose assigned user matches the logged-in user, and are also filtered by complete or incomplete.
  - When viewing incomplete tasks, the user can select a task from the list to:  
    - Edit task name  
    - Edit task description  
    - Edit assigned user  
    - Push due date forward  
    - Mark task as complete  
  
The admin user can additionally:  
- Display statistics
  - This fetches simple counts on the number of users and tasks, as well as a few stats on overdue or complete tasks and users with no tasks or tasks which are overdue.
- Generate reports
  - This generates two new text-files in readable format:
    - A user report, which shows information on:
      - The total number of users
      - A breakdown for each user, showing the number of assigned/overdue/complete tasks for any valid users
    - A task report, which shows information on:
      - The total number of tasks generated
      - The total number of complete, incomplete and overdue tasks
      - The percentage of incomplete and overdue tasks