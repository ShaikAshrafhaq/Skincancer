import React, { useState, useEffect } from "react";

export default function HistoryUploads() {
  const [uploadHistory, setUploadHistory] = useState([]);
  const [filteredHistory, setFilteredHistory] = useState([]);
  const [selectedImage, setSelectedImage] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [filterType, setFilterType] = useState("all");

  // Load history from localStorage on component mount
  useEffect(() => {
    const savedHistory = localStorage.getItem('skinCancerUploadHistory');
    if (savedHistory) {
      setUploadHistory(JSON.parse(savedHistory));
    }
  }, []);

  // Filter history based on search term and filter type
  useEffect(() => {
    let filtered = uploadHistory;

    // Filter by search term (filename, result, or cancer type)
    if (searchTerm) {
      filtered = filtered.filter(upload => 
        upload.filename.toLowerCase().includes(searchTerm.toLowerCase()) ||
        upload.result.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (upload.cancerTypeName && upload.cancerTypeName.toLowerCase().includes(searchTerm.toLowerCase()))
      );
    }

    // Filter by result type
    if (filterType !== "all") {
      filtered = filtered.filter(upload => {
        const result = upload.result.toLowerCase();
        const cancerType = upload.cancerTypeName ? upload.cancerTypeName.toLowerCase() : '';
        
        switch (filterType) {
          case "malignant":
            return result.includes("malignant");
          case "benign":
            return result.includes("benign");
          case "suspicious":
            return result.includes("suspicious");
          case "high-risk":
            return result.includes("malignant") || result.includes("suspicious");
          case "melanoma":
            return cancerType.includes("melanoma");
          case "basal-cell":
            return cancerType.includes("basal cell carcinoma");
          case "squamous-cell":
            return cancerType.includes("squamous cell carcinoma");
          case "merkel-cell":
            return cancerType.includes("merkel cell carcinoma");
          case "sebaceous-gland":
            return cancerType.includes("sebaceous gland carcinoma");
          case "actinic-keratosis":
            return cancerType.includes("actinic keratosis");
          case "seborrheic-keratosis":
            return cancerType.includes("seborrheic keratosis");
          case "benign-mole":
            return cancerType.includes("benign mole") || cancerType.includes("nevus");
          default:
            return true;
        }
      });
    }

    setFilteredHistory(filtered);
  }, [uploadHistory, searchTerm, filterType]);

  // Clear all history
  const clearHistory = () => {
    if (window.confirm('Are you sure you want to clear all upload history?')) {
      setUploadHistory([]);
      localStorage.removeItem('skinCancerUploadHistory');
    }
  };

  // Delete a specific upload
  const deleteUpload = (id) => {
    if (window.confirm('Are you sure you want to delete this upload?')) {
      const updatedHistory = uploadHistory.filter(upload => upload.id !== id);
      setUploadHistory(updatedHistory);
      localStorage.setItem('skinCancerUploadHistory', JSON.stringify(updatedHistory));
    }
  };

  // Format date for display
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
  };

  // Get confidence color based on percentage
  const getConfidenceColor = (confidence) => {
    const num = parseInt(confidence);
    if (num >= 80) return '#4CAF50'; // Green
    if (num >= 60) return '#FF9800'; // Orange
    return '#F44336'; // Red
  };

  // Get doctor recommendation based on result
  const getDoctorRecommendation = (result, confidence) => {
    const resultLower = result.toLowerCase();
    const confidenceNum = parseInt(confidence);
    
    if (resultLower.includes("malignant")) {
      return {
        shouldConsult: true,
        urgency: "high",
        message: "⚠️ URGENT: Consult a dermatologist immediately",
        color: "#F44336"
      };
    } else if (resultLower.includes("suspicious")) {
      return {
        shouldConsult: true,
        urgency: "medium",
        message: "🔍 RECOMMENDED: Schedule a dermatologist appointment within 1-2 weeks",
        color: "#FF9800"
      };
    } else if (resultLower.includes("benign") && confidenceNum < 80) {
      return {
        shouldConsult: true,
        urgency: "low",
        message: "💡 SUGGESTED: Consider a routine check-up for peace of mind",
        color: "#2196F3"
      };
    } else {
      return {
        shouldConsult: false,
        urgency: "none",
        message: "✅ No immediate concern, but regular skin checks are always recommended",
        color: "#4CAF50"
      };
    }
  };

  return (
    <div className="card" style={{ 
      margin: "0", 
      maxWidth: "100%",
      height: "fit-content",
      maxHeight: "100vh",
      overflowY: "auto"
    }}>
      <div style={{ marginBottom: '20px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
          <h2>Upload History</h2>
          {uploadHistory.length > 0 && (
            <button 
              onClick={clearHistory}
              style={{ 
                background: '#f44336', 
                color: 'white', 
                border: 'none', 
                padding: '8px 16px', 
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Clear All
            </button>
          )}
        </div>
        
        {/* Search and Filter Controls */}
        <div style={{ display: 'flex', gap: '10px', marginBottom: '15px', flexWrap: 'wrap' }}>
          <input
            type="text"
            placeholder="Search by filename, result, or cancer type..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={{
              flex: '1',
              minWidth: '200px',
              padding: '8px 12px',
              borderRadius: '4px',
              border: '1px solid #ddd',
              background: 'white',
              color: '#333'
            }}
          />
          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            style={{
              padding: '8px 12px',
              borderRadius: '4px',
              border: '1px solid #ddd',
              background: 'white',
              color: '#333',
              cursor: 'pointer'
            }}
          >
            <option value="all">All Results</option>
            <option value="malignant">Malignant</option>
            <option value="suspicious">Suspicious</option>
            <option value="benign">Benign</option>
            <option value="high-risk">High Risk</option>
            <option value="melanoma">Melanoma</option>
            <option value="basal-cell">Basal Cell Carcinoma</option>
            <option value="squamous-cell">Squamous Cell Carcinoma</option>
            <option value="merkel-cell">Merkel Cell Carcinoma</option>
            <option value="sebaceous-gland">Sebaceous Gland Carcinoma</option>
            <option value="actinic-keratosis">Actinic Keratosis</option>
            <option value="seborrheic-keratosis">Seborrheic Keratosis</option>
            <option value="benign-mole">Benign Mole</option>
          </select>
        </div>
        
        {/* Results count */}
        <p style={{ margin: '0', color: '#666', fontSize: '14px' }}>
          Showing {filteredHistory.length} of {uploadHistory.length} uploads
        </p>
      </div>

      {uploadHistory.length === 0 ? (
        <div style={{ textAlign: 'center', color: '#999', padding: '40px' }}>
          <p>No upload history yet.</p>
          <p>Upload some images to see your analysis history here.</p>
        </div>
      ) : filteredHistory.length === 0 ? (
        <div style={{ textAlign: 'center', color: '#999', padding: '40px' }}>
          <p>No uploads match your search criteria.</p>
          <p>Try adjusting your search terms or filters.</p>
        </div>
      ) : (
        <div style={{ display: 'grid', gap: '16px' }}>
          {filteredHistory.map((upload) => {
            const doctorRec = getDoctorRecommendation(upload.result, upload.confidence);
            return (
            <div 
              key={upload.id} 
              className="card" 
              style={{ 
                padding: '16px', 
                border: '1px solid #e0e0e0',
                borderRadius: '8px',
                cursor: 'pointer',
                transition: 'all 0.2s ease'
              }}
              onClick={() => setSelectedImage(selectedImage === upload.id ? null : upload.id)}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '8px' }}>
                    <div style={{ 
                      width: '60px', 
                      height: '60px', 
                      borderRadius: '8px',
                      overflow: 'hidden',
                      border: '2px solid #e0e0e0'
                    }}>
                      <img 
                        src={upload.imagePreview} 
                        alt="Upload preview"
                        style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                      />
                    </div>
                    <div style={{ flex: 1 }}>
                      <h4 style={{ margin: '0 0 4px 0', fontSize: '16px' }}>
                        {upload.filename}
                      </h4>
                      <p style={{ margin: '0', color: '#666', fontSize: '14px' }}>
                        {formatDate(upload.timestamp)}
                      </p>
                    </div>
                  </div>
                  
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '8px' }}>
                    <span style={{ 
                      background: getConfidenceColor(upload.confidence),
                      color: 'white',
                      padding: '4px 8px',
                      borderRadius: '4px',
                      fontSize: '12px',
                      fontWeight: 'bold'
                    }}>
                      {upload.result}
                    </span>
                    <span style={{ color: '#666', fontSize: '14px' }}>
                      Confidence: {upload.confidence}
                    </span>
                  </div>
                  
                  {/* Cancer Type Information */}
                  {upload.cancerTypeName && upload.cancerTypeName !== 'Unknown' && (
                    <div style={{ 
                      marginBottom: '8px',
                      padding: '6px 10px',
                      borderRadius: '4px',
                      background: '#f8f9fa',
                      border: '1px solid #e9ecef'
                    }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <span style={{ 
                          fontSize: '12px', 
                          fontWeight: 'bold', 
                          color: '#2c3e50' 
                        }}>
                          Cancer Type:
                        </span>
                        <span style={{ 
                          fontSize: '12px', 
                          color: '#e74c3c',
                          fontWeight: 'bold'
                        }}>
                          {upload.cancerTypeName}
                        </span>
                        <span style={{ 
                          fontSize: '11px', 
                          color: '#666' 
                        }}>
                          ({upload.cancerTypeConfidence}% confidence)
                        </span>
                      </div>
                    </div>
                  )}
                  
                  {/* Doctor Recommendation */}
                  <div style={{ 
                    marginBottom: '8px',
                    padding: '8px 12px',
                    borderRadius: '4px',
                    background: doctorRec.color + '20',
                    border: `1px solid ${doctorRec.color}40`
                  }}>
                    <p style={{ 
                      margin: '0', 
                      fontSize: '13px', 
                      color: doctorRec.color,
                      fontWeight: '500'
                    }}>
                      {doctorRec.message}
                    </p>
                  </div>

                  {selectedImage === upload.id && (
                    <div style={{ 
                      marginTop: '12px', 
                      padding: '12px', 
                      background: '#f5f5f5', 
                      borderRadius: '4px',
                      border: '1px solid #e0e0e0'
                    }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <div>
                          <p style={{ margin: '0 0 8px 0', fontWeight: 'bold' }}>Analysis Details:</p>
                          <p style={{ margin: '0', fontSize: '14px' }}>
                            <strong>Result:</strong> {upload.result}
                          </p>
                          <p style={{ margin: '0', fontSize: '14px' }}>
                            <strong>Confidence:</strong> {upload.confidence}
                          </p>
                          {upload.cancerTypeName && upload.cancerTypeName !== 'Unknown' && (
                            <p style={{ margin: '0', fontSize: '14px' }}>
                              <strong>Cancer Type:</strong> {upload.cancerTypeName} ({upload.cancerTypeConfidence}% confidence)
                            </p>
                          )}
                          <p style={{ margin: '0', fontSize: '14px' }}>
                            <strong>Uploaded:</strong> {formatDate(upload.timestamp)}
                          </p>
                          <div style={{ 
                            marginTop: '12px',
                            padding: '8px 12px',
                            borderRadius: '4px',
                            background: doctorRec.color + '20',
                            border: `1px solid ${doctorRec.color}40`
                          }}>
                            <p style={{ 
                              margin: '0', 
                              fontSize: '14px', 
                              color: doctorRec.color,
                              fontWeight: 'bold'
                            }}>
                              Medical Recommendation:
                            </p>
                            <p style={{ 
                              margin: '4px 0 0 0', 
                              fontSize: '13px', 
                              color: doctorRec.color
                            }}>
                              {doctorRec.message}
                            </p>
                          </div>
                        </div>
                        <div style={{ textAlign: 'center' }}>
                          <img 
                            src={upload.imagePreview} 
                            alt="Full size preview"
                            style={{ 
                              maxWidth: '150px', 
                              maxHeight: '150px', 
                              borderRadius: '4px',
                              border: '1px solid #ddd'
                            }}
                          />
                        </div>
                      </div>
                    </div>
                  )}
                </div>
                
                <button 
                  onClick={(e) => {
                    e.stopPropagation();
                    deleteUpload(upload.id);
                  }}
                  style={{ 
                    background: 'transparent', 
                    border: 'none', 
                    color: '#f44336', 
                    cursor: 'pointer',
                    padding: '4px',
                    fontSize: '18px'
                  }}
                  title="Delete upload"
                >
                  ×
                </button>
              </div>
            </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
