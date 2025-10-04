# MySQL Database Setup for Skin Cancer Detection Backend

This guide will help you set up MySQL database for your Django backend.

## Prerequisites

1. **MySQL Server** installed and running on your system
2. **Python 3.8+** installed
3. **Virtual environment** activated (recommended)

## Database Configuration

The database is configured with the following settings:
- **Host**: localhost
- **Port**: 3306
- **Username**: root
- **Password**: Ashraf@12
- **Database Name**: skincancer_db

## Setup Steps

### 1. Install Dependencies

```bash
# Navigate to the backend directory
cd Backend

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Create MySQL Database

Make sure MySQL is running and create the database:

```sql
-- Connect to MySQL as root
mysql -u root -p

-- Create the database
CREATE DATABASE skincancer_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Exit MySQL
EXIT;
```

### 3. Run Database Setup Script

```bash
# Run the automated setup script
python setup_database.py
```

This script will:
- Create the database (if it doesn't exist)
- Run Django migrations
- Create a superuser account

### 4. Test Database Connection

```bash
# Test the database connection
python test_db_connection.py
```

### 5. Start the Django Server

```bash
# Start the development server
python manage.py runserver
```

## Manual Setup (Alternative)

If you prefer to set up manually:

### 1. Create Database
```sql
mysql -u root -p
CREATE DATABASE skincancer_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### 2. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser
```bash
python manage.py createsuperuser
```

## Database Schema

The following Django apps will create tables:
- **accounts**: User authentication and profiles
- **uploads**: File upload management
- **analysis**: Skin cancer analysis results

## Troubleshooting

### Common Issues

1. **MySQL Connection Error**
   - Ensure MySQL server is running
   - Check username/password
   - Verify port 3306 is accessible

2. **Database Not Found**
   - Run the database creation SQL manually
   - Check database name in settings.py

3. **Migration Errors**
   - Delete existing migrations: `rm -rf */migrations/`
   - Recreate migrations: `python manage.py makemigrations`
   - Apply migrations: `python manage.py migrate`

4. **Permission Issues**
   - Ensure MySQL user has proper privileges
   - Grant all privileges: `GRANT ALL PRIVILEGES ON skincancer_db.* TO 'root'@'localhost';`

### Testing Connection

```bash
# Test MySQL connection directly
mysql -u root -p -h localhost -P 3306 skincancer_db

# Test Django connection
python manage.py dbshell
```

## Default Admin Account

After running the setup script, you can access the admin panel at:
- **URL**: http://localhost:8000/admin/
- **Username**: admin
- **Password**: admin123

## Security Notes

⚠️ **Important**: Change the default admin password and database credentials before deploying to production!

```bash
# Change admin password
python manage.py changepassword admin
```

## Environment Variables (Optional)

For better security, you can use environment variables:

1. Create a `.env` file:
```env
DB_NAME=skincancer_db
DB_USER=root
DB_PASSWORD=Ashraf@12
DB_HOST=localhost
DB_PORT=3306
```

2. Update `settings.py` to use environment variables:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME', default='skincancer_db'),
        'USER': config('DB_USER', default='root'),
        'PASSWORD': config('DB_PASSWORD', default='Ashraf@12'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}
```
