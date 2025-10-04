# Skin Cancer Detection Backend

A comprehensive Django REST API backend for the Skin Cancer Detection application.

## Features

- **User Authentication & 2FA**: Secure user registration, login, and OTP verification
- **Image Upload & Analysis**: Advanced skin lesion image analysis with AI-powered detection
- **Medical Recommendations**: Automated doctor consultation recommendations based on analysis results
- **Search & Filtering**: Comprehensive search and filtering for upload history
- **Dashboard Analytics**: Detailed statistics and risk assessment
- **RESTful API**: Complete REST API with proper authentication and permissions

## Technology Stack

- **Django 4.2.7**: Web framework
- **Django REST Framework**: API development
- **Pillow**: Image processing
- **OpenCV**: Computer vision
- **TensorFlow**: Machine learning (ready for integration)
- **PostgreSQL**: Database (production)
- **Redis**: Caching and task queue
- **Celery**: Background tasks

## Installation

### Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)

### Setup

1. **Clone and navigate to backend directory:**
   ```bash
   cd Backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run setup script:**
   ```bash
   python setup.py
   ```

5. **Configure environment:**
   ```bash
   cp env_example.txt .env
   # Edit .env with your settings
   ```

6. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

8. **Start development server:**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/verify-otp/` - OTP verification
- `POST /api/auth/resend-otp/` - Resend OTP
- `GET /api/auth/profile/` - User profile
- `POST /api/auth/logout/` - User logout

### Image Uploads
- `POST /api/uploads/` - Upload and analyze image
- `GET /api/uploads/list/` - List user uploads (with search/filter)
- `GET /api/uploads/<id>/` - Get upload details
- `DELETE /api/uploads/<id>/` - Delete upload
- `GET /api/uploads/statistics/` - Upload statistics
- `DELETE /api/uploads/clear-history/` - Clear upload history

### Analysis
- `GET /api/analysis/dashboard-stats/` - Dashboard statistics
- `GET /api/analysis/trends/` - Analysis trends
- `GET /api/analysis/risk-assessment/` - Risk assessment

## API Usage Examples

### User Registration
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "user123",
    "first_name": "John",
    "last_name": "Doe",
    "password": "securepassword",
    "password_confirm": "securepassword"
  }'
```

### Image Upload
```bash
curl -X POST http://localhost:8000/api/uploads/ \
  -H "Authorization: Token your-token-here" \
  -F "image=@path/to/image.jpg"
```

### Search Uploads
```bash
curl -X GET "http://localhost:8000/api/uploads/list/?search=benign&filter_type=benign" \
  -H "Authorization: Token your-token-here"
```

## Database Models

### User
- Custom user model with email as username
- Profile information and medical history
- OTP verification system

### ImageUpload
- Stores uploaded images and analysis results
- Medical recommendations and urgency levels
- Analysis factors and metadata

### AnalysisHistory
- Tracks search queries and filter usage
- Analytics for user behavior

## Analysis Features

### Image Analysis
- **Resolution Assessment**: Evaluates image quality
- **Color Analysis**: Analyzes color distribution patterns
- **Texture Analysis**: Examines surface texture
- **Border Analysis**: Checks border irregularity
- **Symmetry Analysis**: Evaluates lesion symmetry
- **Size Analysis**: Considers lesion dimensions

### Risk Scoring
- Multi-factor risk assessment algorithm
- Confidence scoring based on analysis quality
- Medical-grade recommendations

### Results Classification
- **Benign**: Low risk, routine monitoring
- **Suspicious**: Medium risk, schedule appointment
- **Malignant**: High risk, immediate consultation

## Security Features

- Token-based authentication
- CORS configuration for frontend integration
- File upload validation and size limits
- Input sanitization and validation
- Secure password handling

## Development

### Running Tests
```bash
python manage.py test
```

### Code Quality
```bash
# Install development dependencies
pip install flake8 black isort

# Format code
black .
isort .

# Lint code
flake8 .
```

### Database Management
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset database (development only)
python manage.py flush
```

## Production Deployment

### Environment Variables
- Set `DEBUG=False`
- Configure production database
- Set up email service for OTP
- Configure Redis for caching
- Set up static file serving

### Database
- Use PostgreSQL for production
- Set up database backups
- Configure connection pooling

### Security
- Use HTTPS in production
- Configure proper CORS settings
- Set up rate limiting
- Enable security headers

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please contact the development team.
