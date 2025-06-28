# TopicToday - Personal Dashboard API

A Flask-based REST API that provides personalized news feeds and motivational quotes based on user preferences. Built with modern Python practices and comprehensive API documentation.

## 🚀 Features

- **🔐 User Authentication** - JWT-based secure authentication
- **📰 Personalized News Feed** - News articles based on user-selected topics
- **💬 Motivational Quotes** - Daily inspirational quotes
- **⚙️ User Preference Management** - Customizable topic preferences
- **🏥 Health Check Endpoint** - API status monitoring
- **📚 Interactive API Documentation** - Swagger UI integration
- **🛡️ Security** - Password hashing, JWT tokens, input validation

## 🛠 Tech Stack

- **Backend Framework**: Flask 3.0.0
- **API Documentation**: Flask-RESTX
- **Authentication**: Flask-JWT-Extended
- **Database ORM**: Flask-SQLAlchemy
- **Database**: SQLite (development) / PostgreSQL (production)
- **Environment Management**: python-dotenv
- **HTTP Requests**: requests
- **Password Security**: bcrypt

## 📋 Prerequisites

- Python 3.8 or higher
- pip package manager
- Git

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/topic-today.git
cd topic-today
```

### 2. Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the root directory:

```env
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-super-secret-key-change-this-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-this-in-production

# External API Keys (Optional - app works with mock data without these)
GNEWS_API_KEY=your-gnews-api-key
ZENQUOTES_API_KEY=your-zenquotes-api-key

# Database (Optional - defaults to SQLite)
DATABASE_URL=sqlite:///instance/topic_today.db
```

### 5. Run the Application

```bash
python run.py
```

The API will be available at:
- **API Base URL**: `http://localhost:5001`
- **Interactive Documentation**: `http://localhost:5001/api/docs/`
- **Health Check**: `http://localhost:5001/api/health`

## 📚 API Documentation

### Interactive Documentation

Visit `http://localhost:5001/api/docs/` for the complete interactive API documentation with Swagger UI.

### API Endpoints

#### 🔐 Authentication Endpoints

##### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "phone_number": "+1234567890",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "message": "User registered successfully",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "john_doe",
    "phone_number": "+1234567890",
    "preferred_topics": [],
    "created_at": "2024-01-01T00:00:00"
  }
}
```

##### Login User
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "john_doe",
    "phone_number": "+1234567890",
    "preferred_topics": ["technology", "health"],
    "created_at": "2024-01-01T00:00:00"
  }
}
```

##### Get User Profile
```http
GET /api/auth/profile
Authorization: Bearer <your-jwt-token>
```

**Response:**
```json
{
  "id": 1,
  "username": "john_doe",
  "phone_number": "+1234567890",
  "preferred_topics": ["technology", "health"],
  "created_at": "2024-01-01T00:00:00"
}
```

#### 📊 Dashboard Endpoints

##### Update User Preferences
```http
PUT /api/dashboard/preferences
Authorization: Bearer <your-jwt-token>
Content-Type: application/json

{
  "topics": ["technology", "health", "sports", "business"]
}
```

**Available Topics:**
- `technology` - Tech news and innovations
- `health` - Health and wellness
- `sports` - Sports news and updates
- `business` - Business and finance
- `science` - Scientific discoveries
- `entertainment` - Movies, music, celebrity news

**Response:**
```json
{
  "message": "Preferences updated successfully",
  "topics": ["technology", "health", "sports", "business"]
}
```

##### Get Personalized Feed
```http
GET /api/dashboard/feed
Authorization: Bearer <your-jwt-token>
```

**Response:**
```json
{
  "news": [
    {
      "title": "Latest AI Breakthrough in Machine Learning",
      "description": "Scientists discover new algorithm that improves AI accuracy by 25%",
      "url": "https://example.com/ai-breakthrough",
      "image": "https://via.placeholder.com/300x200",
      "publishedAt": "2024-01-01T10:00:00Z",
      "source": "Tech Daily",
      "topic": "technology"
    }
  ],
  "quotes": [
    {
      "quote": "The only way to do great work is to love what you do.",
      "author": "Steve Jobs",
      "source": "ZenQuotes"
    }
  ],
  "user_topics": ["technology", "health", "sports", "business"]
}
```

#### 🏥 Health Check

##### API Health Status
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-01T00:00:00.123456"
}
```

## 🔐 Authentication

### JWT Token Usage

1. **Register or Login** to get an access token
2. **Include the token** in the Authorization header:
   ```
   Authorization: Bearer <your-jwt-token>
   ```
3. **Token expires** after 1 hour (configurable)

### Example with curl

```bash
# Register a new user
curl -X POST http://localhost:5001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "phone_number": "+1234567890",
    "password": "password123"
  }'

# Login
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'

# Use the token to access protected endpoints
curl -X GET http://localhost:5001/api/auth/profile \
  -H "Authorization: Bearer <your-jwt-token>"
```

## 🛡️ Database Schema

### User Table
```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    username VARCHAR(64) UNIQUE NOT NULL,
    phone_number VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    preferred_topics TEXT DEFAULT '[]'
);
```

## 🛠 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Flask environment | `development` |
| `SECRET_KEY` | Flask secret key | Auto-generated |
| `JWT_SECRET_KEY` | JWT secret key | Auto-generated |
| `DATABASE_URL` | Database connection string | SQLite |
| `GNEWS_API_KEY` | GNews API key | Mock data |
| `ZENQUOTES_API_KEY` | ZenQuotes API key | Mock data |

### Configuration Classes

- **DevelopmentConfig**: Debug mode, SQL logging, no token expiration
- **ProductionConfig**: Secure settings, token expiration, environment validation
- **TestingConfig**: In-memory database, CSRF disabled

## 🧪 Testing

### Run Tests
```bash
# Install test dependencies
pip install pytest pytest-flask

# Run tests
pytest

# Run with coverage
pytest --cov=app
```

### Test Endpoints
```bash
# Health check
curl http://localhost:5001/api/health

# Register user
curl -X POST http://localhost:5001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","phone_number":"+1234567890","password":"test123"}'
```

## 🚀 Deployment

### Development
```bash
python run.py
```

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

### Docker Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:create_app()"]
```

## 📁 Project Structure


## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Visit `/api/docs/` for interactive API documentation
- **Issues**: Report bugs and feature requests on GitHub
- **Questions**: Open a GitHub discussion

## 🔄 API Versioning

Current API version: `v1.0.0`

API endpoints are versioned through the URL structure:
- Current: `/api/`
- Future versions: `/api/v2/`, `/api/v3/`, etc.

## 📊 API Status

- **Health Check**: `GET /api/health`
- **Status Page**: Available at `/api/docs/`
- **Uptime**: Monitor via health endpoint

---

**Built with ❤️ using Flask and modern Python practices**

