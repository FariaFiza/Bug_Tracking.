##🐛Bug Tracking System

A Django-based web application that helps users submit their buggy code and get it fixed by professional developers. Users can choose their preferred developer, track bug status in real time, comment on reports, and give website feedback.



## 🚀 Features

* 🐛 Submit bug reports with code snippets
* 👨‍💻 Choose your own developer to fix the bug
* 🔧 Developers analyze and submit fixed code with explanation
* 💬 Comment on any bug report
* 📣 Give feedback about the website
* 🔐 Role-based access — User, Developer, Admin
* 🏷️ Priority & status badges — Critical, High, Medium, Low
* 🔍 Filter bugs by status, priority, and language
* ⚡ Fast and clean light-themed UI
  

## 🛠️ Technologies Used

* Python 3.x
* Django 4.2
* HTML5
* CSS3
* SQLite3
* Google Fonts (Plus Jakarta Sans, JetBrains Mono)


## 📖 Sections Included

**Home**
Hero section with stats (total bugs, open bugs, resolved, developers), recent bug reports, and public feedback.

**Bug List**
All submitted bugs with filter options by status, priority, and programming language.

**Bug Detail**
Full bug report view with code snippet, error message, developer fix, and comment section.

**Submit Bug**
Form to submit a new bug — title, description, code, language, priority, error message, and developer selection.

**Developers**
List of all registered developers with their assigned bug count.
**Feedback**
Users can submit ratings and comments about the website.

**Profile**
Shows user info and their submitted or assigned bugs based on role.


## 👥 User Roles

* **Normal User** — Submit bugs, choose developer, comment, give feedback
* **Developer** — View assigned bugs, submit fixes with explanation, update status
* **Admin** — Full control via `/admin` panel


## 🔗 Database Relationships

* `BugReport.submitted_by` → `CustomUser` (ForeignKey)
* `BugReport.assigned_developer` → `CustomUser` (ForeignKey)
* `Comment.author` → `CustomUser` (ForeignKey)
* `Comment.bug` → `BugReport` (ForeignKey)
* `Feedback.submitted_by` → `CustomUser` (ForeignKey)


## 🚀 How to Run

1. Clone or download the repository
2. Open the project in PyCharm or any editor
3. Create a virtual environment and activate it
4. Run `pip install -r requirements.txt`
5. Run `python manage.py makemigrations accounts`
6. Run `python manage.py makemigrations bugs`
7. Run `python manage.py migrate`
8. Run `python manage.py createsuperuser`
9. Run `python manage.py runserver`
10. Open `http://127.0.0.1:8000` in your browser


## 📌 Future Improvements

* Make fully responsive for mobile
* Add email notification when bug is assigned
* Add dark mode toggle
* Add file/screenshot upload for bug reports
* Add developer rating system
* Add real-time chat between user and developer
* Add PDF export of bug reports
* Deploy on Railway or Render





## 📦 Getting Started

Follow these steps to run the project locally:

### 1. Clone the Repository

```bash
git clone https://github.com/FariaFiza/Bug_Tracking..git
cd bugtracker
