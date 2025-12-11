# 🎫 Ticketing System – Full Stack Project

A full-stack Ticketing System built with **Django (Backend)** and **React (Frontend)**.  
The project allows users to create, manage and track support tickets.

---

## 🚀 Tech Stack

### 🔹 Backend (API)
- Python 3.11
- Django / Django REST Framework
- SQLite (dev) / PostgreSQL (production)
- JWT Authentication

### 🔹 Frontend
- React.js
- Axios
- React Router
- Tailwind CSS (optional)

---

## 📁 Project Structure

ticketing-system/
│
├── backend/
│ ├── config/
│ ├── tickets/
│ ├── venv/
│ ├── manage.py
│
├── frontend/
│ ├── src/
│ ├── public/
│ └── package.json
│
└── README.md


---

## ⚙️ Backend Setup (Django)

### 1️⃣ Create & activate virtual environment

```bash
cd backend
python -m venv venv
venv\Scripts\activate

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Run migrations
python manage.py migrate

4️⃣ Start backend server
python manage.py runserver


Backend will run on:

http://127.0.0.1:8000/

🖥️ Frontend Setup (React)
1️⃣ Install dependencies
cd frontend
npm install

2️⃣ Run the React app
npm start


Frontend runs on:

http://localhost:3000/

🔗 API Endpoints
Method	Endpoint	Description
POST	/api/register/	User registration
POST	/api/login/	User login (JWT)
GET	/api/tickets/	List tickets
POST	/api/tickets/	Create a new ticket
GET	/api/tickets/{id}/	Get a ticket
PUT	/api/tickets/{id}/	Update a ticket
DELETE	/api/tickets/{id}/	Delete a ticket
🛠️ Features

🔐 User Authentication (JWT)

🎫 Ticket creation & assignment

📝 Comment/update history

🗂️ Ticket list with filters

👤 User-friendly React interface

🔄 Fully connected REST API

🌍 Environment Variables
Backend

Create a .env file in backend/config/ :

SECRET_KEY=your_secret_key_here
DEBUG=True

Frontend

Create .env in frontend/ :

REACT_APP_API_URL=http://127.0.0.1:8000/api

📦 Production Deployment
Recommended

Backend: Render / Railway / Heroku

Frontend: Vercel / Netlify

Database: PostgreSQL

👨‍💻 Author

Oussama Soumri
Full Stack Developer (React + Django)

