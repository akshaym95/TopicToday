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
- **📊 Logging** - Comprehensive request and error logging

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Flask (Python) |
| **API Documentation** | Flask-RESTX (Swagger/OpenAPI) |
| **Authentication** | Flask-JWT-Extended |
| **Database** | SQLite + SQLAlchemy |
| **API Calls** | requests + external APIs (GNews, ZenQuotes) |
| **Configuration** | python-dotenv for API keys & secrets |

## 📋 API Endpoints

All endpoints are prefixed with `/api/` and documented with Swagger UI at `/api/docs/`.

### 🔐 Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/api/auth/register` | User registration | No |
| `POST` | `/api/auth/login` | User login | No |
| `GET` | `/api/auth/profile` | Get user profile | Yes |

### 📊 Dashboard Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `PUT` | `/api/dashboard/preferences` | Update user topics | Yes |
| `GET` | `/api/dashboard/feed` | Get personalized feed | Yes |

### 🏥 Health Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/health` | API health status | No |

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/topic-today.git
cd topic-today
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys
```

5. **Run the application**
```bash
python run.py
```

6. **Access the API**
- **API Documentation**: http://localhost:5001/api/docs/
- **Health Check**: http://localhost:5001/api/health
- **Base URL**: http://localhost:5001/api/

## 📖 API Usage Examples

### 🔐 Authentication

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "testuser",
  "phone_number": "+1234567890",
  "password": "password123"
}
```

**Response:**
```json
{
  "message": "User registered successfully",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "testuser",
    "phone_number": "+1234567890",
    "preferred_topics": []
  }
}
```

#### Login User
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "testuser",
  "password": "password123"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "testuser",
    "phone_number": "+1234567890",
    "preferred_topics": ["technology", "health"]
  }
}
```

#### Get User Profile
```http
GET /api/auth/profile
Authorization: Bearer <your-jwt-token>
```

**Response:**
```json
{
  "id": 1,
  "username": "testuser",
  "phone_number": "+1234567890",
  "preferred_topics": ["technology", "health"],
  "created_at": "2024-01-01T00:00:00"
}
```

### 📊 Dashboard Operations

#### Update User Preferences
```http
PUT /api/dashboard/preferences
Authorization: Bearer <your-jwt-token>
Content-Type: application/json

{
  "topics": ["technology", "health", "sports", "business"]
}
```

**Response:**
```json
{
  "message": "Preferences updated successfully",
  "topics": ["technology", "health", "sports", "business"]
}
```

#### Get Personalized Feed
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

```
topic-today/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Database models
│   ├── middleware.py        # Request logging middleware
│   ├── api/                 # Flask-RESTX API endpoints
│   │   ├── __init__.py      # API initialization
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── dashboard.py     # Dashboard endpoints
│   │   └── health.py        # Health check endpoint
│   └── services/            # External API services
│       ├── __init__.py
│       ├── news_service.py  # GNews API integration
│       └── quotes_service.py # ZenQuotes API integration
├── config.py                # Configuration classes
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
└── README.md               # Project documentation
```

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

