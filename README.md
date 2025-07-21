# Business Manager Prototype

A modern, responsive Django-based business management tool for teams. Features include:
- Team overview with roles (Head, Manager, Employee, Admin)
- Assigning and tracking tasks
- Beautiful glassmorphism UI with circular progress bars
- Role-based permissions and actions
- Responsive, mobile-friendly design

## Features
- Tabbed team overview (All, Employees, Managers, Heads)
- Assign tasks with a modern, interactive UI
- Circular progress bars for visual progress tracking
- Glassmorphism and gradient backgrounds
- Authentication and role-based access

## Installation & Setup

### 1. Clone the repository
```bash
 git clone <your-repo-url>
 cd BussinessManger_PB
```

### 2. Create and activate a virtual environment
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install django
```

### 4. Apply migrations
```bash
python manage.py migrate
```

### 5. Create a superuser (admin)
```bash
python manage.py createsuperuser
```

### 6. Run the development server
```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Usage
- Log in with your user or superuser account.
- View and manage team members by role.
- Assign tasks using the interactive UI.
- Track progress visually with circular progress bars.

## Project Structure
- `department/` - Main app with models, views, and templates
- `templates/` - All HTML templates
- `business_manager/` - Django project settings and URLs

## Notes
- Media uploads and static files are stored locally (see `.gitignore`).
- For production, configure proper static/media hosting and security settings.

## License

This project is licensed under the [MIT License](LICENSE).

Open to all contributors! For contributions or questions, contact: adii54ti23@gmail.com

---

Enjoy your modern business management dashboard! 