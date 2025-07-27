
# 💬 Real-Time Chat App with Django & Channels

A modern real-time chat application built using Django, Channels (WebSockets), and ASGI. Users can register, log in, send direct messages, and view past conversations — all in real-time.

---

## 🚀 Features

- ✅ Real-time messaging with Django Channels & WebSockets  
- ✅ User authentication (Signup/Login/Logout)  
- ✅ User profiles with profile pictures  
- ✅ Message editing & deletion  
- ✅ Responsive UI with HTML/CSS/JavaScript  
- ✅ SQLite3 for lightweight storage  
- ✅ ASGI-powered backend with Daphne  
- ✅ Admin panel with extended user management  

---

## 🛠 Tech Stack

| Backend        | Frontend       | Database     | Other             |
|----------------|----------------|--------------|--------------------|
| Python         | HTML / CSS     | SQLite 3     | Django ASGI        |
| Django         | JavaScript     |              | Django Channels    |
| Django ORM     | Jinja 2        |              | Pillow (image upload) |

---

## 🔧 Setup Instructions

1. **Clone the repo**

```bash
git clone https://github.com/ahadsts9901/chat-app-django.git
cd chat-app-django
```

2. **Create and activate a virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
cd chatapp
```

4. **Apply migrations and run server (no realtime chat)**

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver  # or use Daphne below
```

5. **To run with Daphne (ASGI server with realtime websockets)**

```bash
daphne chatapp.asgi:application
```

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙌 Show Some Love

If you found this useful, consider giving it a ⭐ on GitHub – it helps a lot!
