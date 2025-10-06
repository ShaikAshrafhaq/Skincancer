# 🩺 Skin Cancer Detection System

A comprehensive web application for detecting and classifying skin cancer types using AI-powered image analysis.

## 🌟 Features

- **8 Cancer Types Detection**: Melanoma, Basal Cell Carcinoma, Squamous Cell Carcinoma, and more
- **Advanced AI Analysis**: Multi-factor risk assessment with confidence scoring
- **User Authentication**: Secure login with 2FA (Two-Factor Authentication)
- **Medical Recommendations**: Tailored advice based on cancer type and risk level
- **History Management**: Searchable and filterable analysis history
- **Real-time Analysis**: Live image processing and results
- **Database Storage**: All data persisted in PostgreSQL (production) or MySQL (development)

## 🏗️ Architecture

### Backend (Django + PostgreSQL)
- **Framework**: Django 4.2.7 with Django REST Framework
- **Database**: PostgreSQL (production) / MySQL (development)
- **Authentication**: Token-based with 2FA support
- **API**: RESTful endpoints with comprehensive filtering
- **File Storage**: Secure image upload and processing

### Frontend (React + Vite)
- **Framework**: React 18 with Vite
- **UI**: Modern, responsive design
- **State Management**: Context API with localStorage fallback
- **API Integration**: Seamless backend communication
- **Real-time Updates**: Live analysis results

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- MySQL (development) or PostgreSQL (production)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd SKIN-CANCER
   ```

2. **Backend Setup**
   ```bash
   cd Backend
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

3. **Frontend Setup**
   ```bash
   cd Frontend/@
   npm install
   npm run dev
   ```

4. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000/api
   - Admin Panel: http://localhost:8000/admin

## 🌐 Production Deployment

### Render.com Deployment

This project is configured for automatic deployment on Render.com:

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Deploy to Render.com"
   git push origin main
   ```

2. **Deploy on Render.com**
   - Go to [render.com](https://render.com)
   - Connect your GitHub repository
   - Select "Blueprint" deployment
   - Render will automatically detect the `render.yaml` file

3. **Your app will be live at**:
   - **Frontend**: `https://skincancer-frontend.onrender.com`
   - **Backend**: `https://skincancer-backend.onrender.com`

## 📊 Cancer Types Detected

1. **Melanoma** - High risk, immediate urgency
2. **Basal Cell Carcinoma** - Low risk, medium urgency
3. **Squamous Cell Carcinoma** - Medium risk, high urgency
4. **Merkel Cell Carcinoma** - Very high risk, immediate urgency
5. **Sebaceous Gland Carcinoma** - High risk, immediate urgency
6. **Actinic Keratosis** - Low risk, low urgency
7. **Seborrheic Keratosis** - No risk, no urgency
8. **Benign Mole** - No risk, no urgency

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration
- `POST /api/auth/verify-otp/` - OTP verification

### Image Analysis
- `POST /api/uploads/` - Upload image and analyze
- `GET /api/uploads/` - Get user's analysis history
- `GET /api/uploads/{id}/` - Get specific analysis details
- `DELETE /api/uploads/{id}/` - Delete analysis
- `GET /api/uploads/statistics/` - Get user analytics

### Query Parameters
- `search` - Search by filename, result, or cancer type
- `filter_type` - Filter by result type or cancer type
- `cancer_type` - Filter by specific cancer type
- `risk_level` - Filter by risk level
- `ordering` - Sort by field

## 🗄️ Database Schema

### Key Models
- **User**: Custom user model with extended fields
- **ImageUpload**: Analysis results with cancer type detection
- **UserProfile**: Extended medical information
- **AnalysisHistory**: Search and filter history

### Cancer Type Fields
```sql
cancer_type VARCHAR(30)           -- melanoma, basal_cell_carcinoma, etc.
cancer_type_confidence FLOAT      -- 88.2%
cancer_type_name VARCHAR(100)     -- "Melanoma", "Basal Cell Carcinoma"
risk_level VARCHAR(15)            -- high, medium, low, none
urgency_level VARCHAR(15)         -- immediate, high, medium, low, none
```

## 🔒 Security Features

- **Authentication**: Token-based with 2FA
- **Data Isolation**: User-specific data access
- **File Upload Security**: Type and size validation
- **CORS Protection**: Properly configured for production
- **Environment Variables**: Secure configuration management

## 📈 Performance Features

- **Static File Optimization**: WhiteNoise for production
- **Database Optimization**: Efficient queries with filtering
- **CDN Support**: Global content delivery
- **Caching**: Optimized for repeated requests
- **Lazy Loading**: Efficient frontend data loading

## 🧪 Testing

### Backend Tests
```bash
cd Backend
python manage.py test
python test_mysql_storage.py
python verify_mysql_integration.py
```

### Frontend Tests
```bash
cd Frontend/@
npm test
```

## 📁 Project Structure

```
SKIN-CANCER/
├── Backend/                    # Django backend
│   ├── accounts/              # User management
│   ├── uploads/               # Image analysis
│   ├── analysis/              # Analysis services
│   ├── skincancer_backend/    # Django settings
│   ├── requirements.txt       # Python dependencies
│   └── manage.py              # Django management
├── Frontend/@/                # React frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/            # Page components
│   │   ├── state/            # State management
│   │   └── services/         # API services
│   ├── package.json          # Node dependencies
│   └── vite.config.js        # Vite configuration
├── render.yaml               # Render.com deployment config
├── build.sh                  # Build script
└── README.md                 # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation in `/Backend/RENDER_DEPLOYMENT_GUIDE.md`
- Review the API documentation in `/Backend/API_INTEGRATION_GUIDE.md`

## 🎯 Roadmap

- [ ] Real AI model integration
- [ ] Mobile app development
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Integration with medical databases

---

**Built with ❤️ for early skin cancer detection and prevention.**
