  
# Project 4: Network  
  
### HarvardX CS50W  
### Submission by William Shearer, June, 2023  
  
## Overview  
  
This project aims to simulate a **social media** platform containing some common features of said online applications. The liberty was taken to call the application itself a name other than simply "Network". In this case, it was named **PhiQuips**, to give the application a theme for the posting of random, philosophical comments.  
  
The requirements for the inclusion of these features are determined in the project specifications, which are as follow:  
  
1. **New Post:** Users who are signed in should be able to write a new text-based post by filling in text into a text area and then clicking a button to submit the post.  

    - The screenshot at the top of this specification shows the “New Post” box at the top of the “All Posts” page. You may choose to do this as well, or you may make the “New Post” feature a separate page.  
  
2. **All Posts:** The “All Posts” link in the navigation bar should take the user to a page where they can see all posts from all users, with the most recent posts first.  
  
    - Each post should include the username of the poster, the post content itself, the date and time at which the post was made, and the number of “likes” the post has (this will be 0 for all posts until you implement the ability to “like” a post later).  
  
3. **Profile Page:** Clicking on a username should load that user’s profile page. This page should:  
  
    - Display the number of followers the user has, as well as the number of people that the user follows.  
    - Display all of the posts for that user, in reverse chronological order.  
    - For any other user who is signed in, this page should also display a “Follow” or “Unfollow” button that will let the current user toggle whether or not they are following this user’s posts. Note that this only applies to any “other” user: a user should not be able to follow themselves.  
  
4. **Following:** The “Following” link in the navigation bar should take the user to a page where they see all posts made by users that the current user follows.  

    - This page should behave just as the “All Posts” page does, just with a more limited set of posts.  
    - This page should only be available to users who are signed in.  
  
5. **Pagination:** On any page that displays posts, posts should only be displayed 10 on a page. If there are more than ten posts, a “Next” button should appear to take the user to the next page of posts (which should be older than the current page of posts). If not on the first page, a “Previous” button should appear to take the user to the previous page of posts as well.  
  
    - See the Hints section for some suggestions on how to implement this.  
  
6. **Edit Post:** Users should be able to click an “Edit” button or link on any of their own posts to edit that post.  
  
    - When a user clicks “Edit” for one of their own posts, the content of their post should be replaced with a textarea where the user can edit the content of their post.  
    - The user should then be able to “Save” the edited post. Using JavaScript, you should be able to achieve this without requiring a reload of the entire page.  
    - For security, ensure that your application is designed such that it is not possible for a user, via any route, to edit another user’s posts.  

7. **“Like” and “Unlike”:** Users should be able to click a button or link on any post to toggle whether or not they “like” that post.  
  
    - Using JavaScript, you should asynchronously let the server know to update the like count (as via a call to fetch) and then update the post’s like count displayed on the page, without requiring a reload of the entire page.  
  
The project should be based on **Python's Django Web Framework**, and utilize **HTML**, **CSS** (with and without **Bootstrap**), and **JavaScript** to implement application functionality and display to the browser. Models for the data base should be implemented, and a User Registration, Login and Logout system should exist. The project should be configured to run in *DEBUG = True* mode (development) on localhost:8000, primarily, though conversion to production for deployment could be enabled.  
  
#### Note to Evaluators  
  
The course (CS50W) is from 2020, and therefore some updates and changes have since, inevitably, been made to versions of both Python and the Django Framework. This translated into a few minor issues being experienced utilizing the provided distribution code. Therefore, the project was built from scratch using **Python 3.11.3** and **Django 4.2.1**. The structure of the project, however, was maintained, and where possible, HTML templates were imported manually to the new project from the original distribution code, subsequently being modified to accomodate the requirements of the specifications. Additionally, the version of **Bootstrap** was updated to the latest (**5**) in the *layout.html* file. This, to ensure the highest possible level of functionality, currency, and compatibility in running the project. The project was developed entirely on a Linux OS PC, running Lubuntu 22.04 LTS. Additionally, the project adds a couple of enhanced features over the specification requirements, one of which requires the inclusion of the **Python Pillow** package in the environment the program is run from. The environment should comply with Python 3.11.3 and Django 4.2.1, therefore it is recommended that a virtual environment be set up running these prerequisites. Specific details are contained in the included *requirements.txt* file, which is here recreated for reference:  
  
- *asgiref==3.7.2*
- *Django==4.2.1*
- *Pillow==9.5.0*
- *sqlparse==0.4.4*
  
## Features  
  
### Models  
  
The project allowed the candidate to develop the application setting up the Django models as best suited the specifications. Therefore, models for the User, Profile, and Post were implemented. Theses contained, between them, all the fields that would enable complete functionality. Additionally, all of the ORM relationships were utilized (ForeignKey, OneToOne, and ManyToMany) to demonstrate the understanding and applicability of each. In addition, reverse "related names" were included (and used in the code) to accomplish some of the specifications.
  
### URLS and View Functions  
  
Special care was taken to efficiently use the functions contained in the Python/Django *views.py* file, and avoid as much as possible duplication of code. Therefore, multiple routes were specified for the same functions in the application *urls.py* file, in order that functions could be reused from different application routes. A most notable employment of this technique is demonstrated between the *index* and *view_profile* functions, related to the All Posts and Profile pages.  
  
### Asynchronous JavaScript  
  
**Asynchronous functions** were utilized rather more than actually required by the specification, primarily to improve the efficiency of the application, and secondarily to demonstrate comprehension of the method. Great pains were taken to properly understand how asynchronous functions in JavaScript actually work, and to this end, most of the fucntions that use the technique included in the JavaScript code do so employing the expanded function method. Where the more compact *chaining* method of effecting promises is more efficient in saving space, it hardly provides a good basis to observe, with any readability, what is going on "under the hood". The expanded method is much better suited to aiding the learning process, and permits the uncomplicated inclusion of AbortControllers and Timeout functions, as well as effective and clearly discernable error trapping. Additionally, it is clear when **await** statements need to be included in the code, and why they are necessarily there. That said, one example of a chained function is included in the code, just so that it is obvious that these, too, were understood by the candidate (that is, me), though preference decidedly falls on the more traditional **async** function, for the time being. Also, extensive use of arrow (=>) function definition shortcuts were also kept to a minimum, again not because they were not (eventually) understood, but because they do not collaborate to proper learner level understanding. There will be plenty of opportunities to use them in the future, but in this project everything constitutes look back and review reference that should be as self-explanatory as possible to the candidate if temporary Alka Seltzer strikes.  
  
### CSRF Tokens  
  
Where the project permitted (even, encouraged) the use of the *csrf_exempt* decorator, the candidate chose to avoid using it. There are to reasons for this. The first, csrf tokens are a safety feature. Making them work during the API fetch routines was a laborious concept to grasp, learn, and implement, but was deemed worth the extra effort. Examples of it can be seen in the "PUT" or "POST" functions. The second reason was that the functionality of the *csrf_exempt* decorator seemed somewhat erratic. Notably, on one specific occasion, it refused to work for a given "PUT" request, which tipped the balance on the decision to eliminate its use completely. So much the better. All csrf tokens are, therefore, passed with all fetch requests that require them, in the header.  
  
### Forms  
  
The project specifications do not require (nor actively encourages) use of Django Forms. However, they were developed and implemented in this submission because, first, they should ideally be used as they are an integral part of the Django Framework, and, second, they provide added security in the form of automatic client-side validation. Therefore, these forms were utilized anywhere they could be used, including replacing the distribution code's handcrafted HTML Register and Login forms.  
  
### Added Features  
  
In addition to complying with the specifications, five additional features were added to the project:  
  
- **User image:** The user may upload a picture at registration-time that will be displayed on each post, next to the username, in the All Posts and Following pages. Additionally, the same image will be displayed once on the Profile page for each respective user. If the user opts not to upload a picture, a default image will be provided automatically.  
  
- **Change Password Form:** On the profile page, is the user opens at their own profile, there will be a button to enable changing the password. The user will be asked to enter the new password twice, for confirmation, and will be returned to the profile page, still logged in, after the procedure.  
  
 - **Edit Profile Form:** Also, on the profile page of their own, the user will have an option to edit their profile. This will provide a form, preloaded with the current data, that the user may edit and save.  
  
- **Reference Post Number:** Only on the own profile page, the user will see a number under the Subject Title of the post. This is a maintenance feature that the user can benefit from if ever they need to request to admin the deletion of one of their own posts (as self initiated deletion of a post is not enabled).  
  
- **Modal Terms Window:** Clicking on the title (**PhiQuips**) in the nav bar, in any view, will open a modal pop up window that contains some information about the site. The modal window can be closed either by manually clicking the close button, or scrolling the screen.  
  
## Concludes  
  
The project was completed by William Shearer, student of EDX's HarvardX CS50W course, June, 2023, who resides in Quito, Ecuador.  
  
