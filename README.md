# 🔥 Free Fire Spam Master

Ultimate Free Fire UID Spammer with VIP services and modern cyber gaming interface.

## 🚀 Features

- **Free Fire UID Spam** - Target specific Free Fire UIDs with VIP spam services
- **Real-time Dashboard** - Monitor all active and stopped spam operations
- **Session Management** - Track, stop, and delete spam sessions
- **Data Persistence** - All data automatically saved to JSON with backup system
- **Modern UI** - Stunning cyber gaming interface with animations
- **API Endpoints** - Full REST API for programmatic access
- **Developer Credits** - Built by DEV JNIYEN & DEV CH9AYFA

## 🛠️ Technology Stack

- **Backend**: Python 3.11, Flask 3.0
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript ES6+
- **Database**: JSON file storage with automatic backups
- **Deployment**: Railway, Gunicorn
- **Icons**: Bootstrap Icons

## 📱 Contact Developers

- **DEV JNIYEN** (Lead Developer): [@dev_jniyen](https://t.me/dev_jniyen)
- **DEV CH9AYFA** (Co-Developer): [@CH9AYFAX1](https://t.me/CH9AYFAX1)

## 🎮 Free Fire UID Format

Valid UIDs are 9-12 digits only:
- ✅ `123456789` (9 digits)
- ✅ `1234567890` (10 digits)
- ✅ `123456789012` (12 digits)

## 🔧 Local Development

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python main.py`
4. Open `http://localhost:5000`

## 🚀 Deployment

This application is configured for Railway deployment with:
- `Procfile` for process management
- `railway.json` for Railway configuration
- `runtime.txt` for Python version
- Automatic data persistence with JSON storage

## 📊 API Endpoints

- `GET /api/spam_vip/<freefire_uid>` - Start spam for Free Fire UID
- `GET /api/stop/<session_id_or_uid>` - Stop spam session
- `GET /api/spam_list` - List all sessions
- `GET /api/session/<session_id>` - Get session details
- `GET /api/sessions/target/<freefire_uid>` - Get sessions by UID
- `DELETE /api/delete/<session_id>` - Delete session

## 💾 Data Management

- Automatic JSON file storage (`data.json`)
- Automatic backups before each save
- Manual backup creation
- Data statistics and monitoring

## 🎨 Interface Features

- Cyber gaming theme with orange/gold colors
- Floating animations and particle effects
- Responsive design for all devices
- Real-time updates and notifications
- Interactive modals and forms

## 📝 License

Built with ❤️ by DEV JNIYEN & DEV CH9AYFA

---

**© 2024 Free Fire Spam Master - Elite Development Team**
