# Authentication System Guide

## Overview
The authentication system now includes proper user validation for both login and signup processes.

## Features

### 🔐 **Login Validation**
- ✅ Checks if user account exists
- ✅ Validates email and password format
- ✅ Shows "Invalid user - Account does not exist" for non-existent accounts
- ✅ Requires minimum 6-character password
- ✅ Proceeds to 2FA after successful validation

### 📝 **Signup Validation**
- ✅ Checks if email already exists
- ✅ Shows "Account already exists with this email" for existing accounts
- ✅ Validates email format with regex
- ✅ Requires minimum 6-character password
- ✅ Creates new user account after OTP verification
- ✅ Stores user data in localStorage

### 💾 **User Storage**
- Users are stored in browser's localStorage
- Each user has: id, name, email, password, createdAt, isVerified
- Data persists between browser sessions

## How It Works

### Login Flow:
1. User enters email and password
2. System checks if user exists
3. If not found: Shows "Invalid user - Account does not exist"
4. If found: Generates OTP and proceeds to 2FA
5. After OTP verification: User is logged in

### Signup Flow:
1. User enters name, email, and password
2. System validates email format
3. System checks if email already exists
4. If exists: Shows "Account already exists with this email"
5. If new: Creates user object and proceeds to 2FA
6. After OTP verification: User account is created and user is logged in

## Error Messages

### Login Errors:
- "Please enter both email and password"
- "Invalid user - Account does not exist"
- "Password must be at least 6 characters"

### Signup Errors:
- "Please fill in all fields"
- "Please enter a valid email address"
- "Account already exists with this email"
- "Password must be at least 6 characters"

## Testing

### Test Panel
A test panel is available in the top-right corner for development:
- Test if a user exists by email
- View current user information
- Debug user storage

### Test Scenarios:
1. **New User Signup**: Try signing up with a new email
2. **Existing User Login**: Try logging in with an existing account
3. **Invalid Login**: Try logging in with non-existent email
4. **Duplicate Signup**: Try signing up with existing email
5. **Invalid Email**: Try signing up with invalid email format

## Data Structure

```javascript
// User object stored in localStorage
{
  id: "timestamp",
  name: "User Name",
  email: "user@example.com",
  password: "password123",
  createdAt: "2024-01-01T00:00:00.000Z",
  isVerified: false
}
```

## Security Notes

⚠️ **Important**: This is a demo implementation. In production:
- Passwords should be hashed before storage
- Use secure backend authentication
- Implement proper session management
- Add rate limiting for login attempts
- Use HTTPS for all communications

## Development

To test the authentication system:
1. Start the frontend: `npm start`
2. Use the test panel to check user data
3. Try different login/signup scenarios
4. Check browser localStorage for stored users
