# PAL

PAL (Preserving Academic Life) - Read Me
Lillian Davis, Michaela Snyder, Eric Xing

The developers of this software project are all members of the CS 496 Spring 2023 Senior Project course at WKU. The goal of the PAL website is to assist the target audience, those in some way affiliated with the CS and Math departments at WKU, in organizing and maintaining their daily and semester schedules. The website is mainly divided into two applications, a Course Registration page and a Task Manager site. Both applications are designed to create a user-oriented scheduler website; focusing on goals such as ease of use, high levels of organization, and accurate and helpful course schedule advice.

This document will provide instructions for readers to recreate or access the PAL system. This file will also detail some of the main aspects of the site including how data is separated and accessed within the application. 

Clone PAL GitHub repository
Create virtual environment

Change directory to current project folder
	
Launch project



Users should then have access to the PAL site. 

If the user wants to continue as a regular user:
Navigate to the login screen → new user screen
Enter password and username
Return to PAL home page 

If the user wants to continue as an admin user:
Create a new superuser from the terminal
To ensure this was completed correctly, transition to the admin page (http://127.0.0.1:8000/admin/) 
Return to PAL home page

Users should now be able to access all areas of the website and test accordingly. Once gaining full access to the site, the user may navigate through the multiple site pages using the navigation bar located along the top of all site pages. The following list describes some features that are available to the user based on the corresponding site page:
Course Registration
Program automatically loads with a recommended schedule based on previous user credits
User may alter a schedule by adding or deleting courses
User may save or load a schedule
Task Manager
User may create a category
User may create a task
User may switch between task categories
User may view all tasks for a category, and all tasks in said category with a deadline within the current month
User Profile
User may enter previously taken courses
User may enter additional information such as user type (Student or Advisor) and chosen major
