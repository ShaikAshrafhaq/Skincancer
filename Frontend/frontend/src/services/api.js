// API service for connecting to the backend
const API_BASE_URL = 'http://localhost:8000/api';

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  // Helper method to get auth headers
  getAuthHeaders() {
    const token = localStorage.getItem('authToken');
    return {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Token ${token}` })
    };
  }

  // Helper method to get multipart headers for file uploads
  getMultipartHeaders() {
    const token = localStorage.getItem('authToken');
    return {
      ...(token && { 'Authorization': `Token ${token}` })
    };
  }

  // Generic request method
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: this.getAuthHeaders(),
      ...options
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Authentication endpoints
  async login(email, password) {
    return this.request('/auth/login/', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    });
  }

  async register(userData) {
    return this.request('/auth/register/', {
      method: 'POST',
      body: JSON.stringify(userData)
    });
  }

  async verifyOTP(otp) {
    return this.request('/auth/verify-otp/', {
      method: 'POST',
      body: JSON.stringify({ otp })
    });
  }

  async resendOTP(email) {
    return this.request('/auth/resend-otp/', {
      method: 'POST',
      body: JSON.stringify({ email })
    });
  }

  // Image upload and analysis
  async uploadImage(imageFile) {
    const formData = new FormData();
    formData.append('image', imageFile);

    const token = localStorage.getItem('authToken');
    const response = await fetch(`${this.baseURL}/uploads/`, {
      method: 'POST',
      headers: {
        ...(token && { 'Authorization': `Token ${token}` })
      },
      body: formData
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }

  // Get upload history
  async getUploadHistory(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const endpoint = `/uploads/${queryString ? `?${queryString}` : ''}`;
    return this.request(endpoint);
  }

  // Get upload statistics
  async getUploadStatistics() {
    return this.request('/uploads/statistics/');
  }

  // Delete specific upload
  async deleteUpload(uploadId) {
    return this.request(`/uploads/${uploadId}/`, {
      method: 'DELETE'
    });
  }

  // Clear all uploads
  async clearUploadHistory() {
    return this.request('/uploads/clear/', {
      method: 'DELETE'
    });
  }

  // Get specific upload details
  async getUploadDetails(uploadId) {
    return this.request(`/uploads/${uploadId}/`);
  }
}

// Create and export a singleton instance
const apiService = new ApiService();
export default apiService;
