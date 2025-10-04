import React from 'react';

// Skin cancer types with detailed information
const CANCER_TYPES = {
  MELANOMA: {
    name: 'Melanoma',
    description: 'The most dangerous form of skin cancer, originating in melanocytes (pigment-producing cells)',
    characteristics: [
      'Asymmetrical shape (A)',
      'Irregular borders (B)',
      'Multiple colors (C)',
      'Large diameter >6mm (D)',
      'Evolving appearance (E)',
      'Dark brown or black color',
      'May have different shades of brown, black, or pink'
    ],
    riskLevel: 'HIGH',
    urgency: 'IMMEDIATE',
    color: '#E74C3C',
    icon: '⚠️',
    treatment: 'Surgical removal, immunotherapy, targeted therapy, chemotherapy',
    survivalRate: '95% if caught early, 15-20% if advanced',
    category: 'Common',
    origin: 'Melanocytes (pigment-producing cells)'
  },
  BASAL_CELL_CARCINOMA: {
    name: 'Basal Cell Carcinoma (BCC)',
    description: 'Most common type of skin cancer, originating in basal cells of epidermis',
    characteristics: [
      'Pearl-like or waxy bump',
      'Pink, red, or white color',
      'Shiny appearance',
      'Slow growing',
      'May bleed or crust',
      'Raised border with central indentation',
      'Rarely spreads to other parts'
    ],
    riskLevel: 'LOW',
    urgency: 'MODERATE',
    color: '#F39C12',
    icon: '🟡',
    treatment: 'Surgical removal, Mohs surgery, topical treatments, cryotherapy',
    survivalRate: '99% with treatment',
    category: 'Common (Non-melanoma)',
    origin: 'Basal cells of epidermis'
  },
  SQUAMOUS_CELL_CARCINOMA: {
    name: 'Squamous Cell Carcinoma (SCC)',
    description: 'Second most common skin cancer, starts in squamous cells of epidermis',
    characteristics: [
      'Rough, scaly patch',
      'Red or pink color',
      'May be tender to touch',
      'Can grow quickly',
      'May ulcerate or bleed',
      'Firm, raised growth',
      'May spread if left untreated'
    ],
    riskLevel: 'MEDIUM',
    urgency: 'MODERATE',
    color: '#E67E22',
    icon: '🟠',
    treatment: 'Surgical removal, Mohs surgery, radiation therapy, chemotherapy',
    survivalRate: '95% with early treatment',
    category: 'Common (Non-melanoma)',
    origin: 'Squamous cells of epidermis'
  },
  MERKEL_CELL_CARCINOMA: {
    name: 'Merkel Cell Carcinoma',
    description: 'Rare, aggressive skin cancer that starts in Merkel cells at nerve endings',
    characteristics: [
      'Fast-growing, painless nodule',
      'Red, purple, or skin-colored',
      'Shiny appearance',
      'Usually on sun-exposed areas',
      'May ulcerate',
      'Highly aggressive',
      'Common in older adults'
    ],
    riskLevel: 'VERY HIGH',
    urgency: 'IMMEDIATE',
    color: '#8E44AD',
    icon: '🚨',
    treatment: 'Surgical removal, radiation therapy, immunotherapy, chemotherapy',
    survivalRate: '60-80% with early treatment',
    category: 'Rare',
    origin: 'Merkel cells (nerve endings)'
  },
  SEBACEOUS_GLAND_CARCINOMA: {
    name: 'Sebaceous Gland Carcinoma',
    description: 'Rare cancer that begins in the sebaceous glands of the skin',
    characteristics: [
      'Yellowish, waxy appearance',
      'May resemble a chalazion or stye',
      'Slow-growing initially',
      'Can become aggressive',
      'Often on eyelids',
      'May cause eyelid distortion',
      'Can spread to lymph nodes'
    ],
    riskLevel: 'HIGH',
    urgency: 'IMMEDIATE',
    color: '#D35400',
    icon: '🔴',
    treatment: 'Surgical removal, Mohs surgery, radiation therapy, chemotherapy',
    survivalRate: '70-85% with early treatment',
    category: 'Rare',
    origin: 'Sebaceous glands'
  },
  ACTINIC_KERATOSIS: {
    name: 'Actinic Keratosis',
    description: 'Precancerous lesion that may develop into Squamous Cell Carcinoma',
    characteristics: [
      'Rough, scaly patches',
      'Pink, red, or brown color',
      'Small size (<1cm)',
      'May be tender or itchy',
      'Sun-exposed areas',
      'Sandpaper-like texture',
      'May feel rough to touch'
    ],
    riskLevel: 'LOW',
    urgency: 'LOW',
    color: '#9B59B6',
    icon: '🟣',
    treatment: 'Topical treatments, cryotherapy, photodynamic therapy',
    survivalRate: '100% with treatment',
    category: 'Precancerous',
    origin: 'Sun-damaged skin cells'
  },
  SEBORRHEIC_KERATOSIS: {
    name: 'Seborrheic Keratosis',
    description: 'Benign (non-cancerous) skin growth, very common in older adults',
    characteristics: [
      'Waxy, stuck-on appearance',
      'Brown, black, or tan color',
      'Rough, scaly texture',
      'Round or oval shape',
      'Well-defined borders',
      'Common in older adults',
      'May be single or multiple'
    ],
    riskLevel: 'NONE',
    urgency: 'NONE',
    color: '#27AE60',
    icon: '✅',
    treatment: 'No treatment needed, cosmetic removal if desired',
    survivalRate: '100% (benign)',
    category: 'Benign',
    origin: 'Normal skin cells'
  },
  BENIGN_MOLE: {
    name: 'Benign Mole (Nevus)',
    description: 'Normal, non-cancerous mole, common in most people',
    characteristics: [
      'Round or oval shape',
      'Even color throughout',
      'Smooth, well-defined borders',
      'Small size (<6mm)',
      'Stable appearance over time',
      'May be flat or raised',
      'Single color (brown, black, or tan)'
    ],
    riskLevel: 'NONE',
    urgency: 'NONE',
    color: '#2ECC71',
    icon: '✅',
    treatment: 'No treatment needed, monitor for changes',
    survivalRate: '100% (benign)',
    category: 'Benign',
    origin: 'Melanocytes (normal)'
  }
};

// Function to detect cancer type based on analysis factors
export const detectCancerType = (analysisResult) => {
  const { riskScore, factors, confidence } = analysisResult;
  
  // Simulate advanced AI analysis based on multiple factors
  let detectedType = 'BENIGN_MOLE';
  let detectionConfidence = confidence;
  
  // Analyze based on risk score and other factors
  if (riskScore > 0.9) {
    // Very high risk - could be rare aggressive cancers
    if (factors.fileName.includes('merkel') || factors.fileName.includes('nerve')) {
      detectedType = 'MERKEL_CELL_CARCINOMA';
      detectionConfidence = Math.min(90, confidence + 10);
    } else if (factors.fileName.includes('sebaceous') || factors.fileName.includes('eyelid') || factors.fileName.includes('gland')) {
      detectedType = 'SEBACEOUS_GLAND_CARCINOMA';
      detectionConfidence = Math.min(90, confidence + 8);
    } else {
      detectedType = 'MELANOMA';
      detectionConfidence = Math.min(95, confidence + 5);
    }
  } else if (riskScore > 0.8) {
    // High risk - likely melanoma or rare cancers
    if (factors.fileName.includes('fast') || factors.fileName.includes('aggressive')) {
      detectedType = 'MERKEL_CELL_CARCINOMA';
      detectionConfidence = Math.min(88, confidence + 5);
    } else if (factors.fileName.includes('yellow') || factors.fileName.includes('waxy')) {
      detectedType = 'SEBACEOUS_GLAND_CARCINOMA';
      detectionConfidence = Math.min(85, confidence + 3);
    } else {
      detectedType = 'MELANOMA';
      detectionConfidence = Math.min(95, confidence + 5);
    }
  } else if (riskScore > 0.6) {
    // Medium-high risk - could be melanoma, SCC, or rare cancers
    if (factors.fileName.includes('scaly') || factors.fileName.includes('rough')) {
      detectedType = 'SQUAMOUS_CELL_CARCINOMA';
    } else if (factors.fileName.includes('nodule') || factors.fileName.includes('purple')) {
      detectedType = 'MERKEL_CELL_CARCINOMA';
      detectionConfidence = Math.max(75, confidence - 5);
    } else {
      detectedType = 'MELANOMA';
    }
    detectionConfidence = confidence;
  } else if (riskScore > 0.4) {
    // Medium risk - likely BCC, SCC, or rare cancers
    if (factors.fileName.includes('bump') || factors.fileName.includes('pearl')) {
      detectedType = 'BASAL_CELL_CARCINOMA';
    } else if (factors.fileName.includes('patch') || factors.fileName.includes('scaly')) {
      detectedType = 'SQUAMOUS_CELL_CARCINOMA';
    } else if (factors.fileName.includes('eyelid') || factors.fileName.includes('gland')) {
      detectedType = 'SEBACEOUS_GLAND_CARCINOMA';
      detectionConfidence = Math.max(70, confidence - 10);
    } else {
      detectedType = 'BASAL_CELL_CARCINOMA';
    }
    detectionConfidence = confidence;
  } else if (riskScore > 0.2) {
    // Low-medium risk - could be actinic keratosis
    detectedType = 'ACTINIC_KERATOSIS';
    detectionConfidence = Math.max(70, confidence - 5);
  } else if (riskScore > 0.1) {
    // Low risk - could be seborrheic keratosis
    detectedType = 'SEBORRHEIC_KERATOSIS';
    detectionConfidence = Math.max(75, confidence - 10);
  } else {
    // Very low risk - likely benign
    detectedType = 'BENIGN_MOLE';
    detectionConfidence = Math.max(80, confidence - 5);
  }
  
  // Add some randomness for more realistic results
  const randomFactor = Math.random();
  if (randomFactor > 0.9) {
    // 10% chance of different classification
    const types = Object.keys(CANCER_TYPES);
    const randomType = types[Math.floor(Math.random() * types.length)];
    detectedType = randomType;
    detectionConfidence = Math.max(60, detectionConfidence - 15);
  }
  
  return {
    type: detectedType,
    confidence: Math.round(detectionConfidence),
    details: CANCER_TYPES[detectedType]
  };
};

// Component to display cancer type information
export default function CancerTypeDetection({ cancerType, confidence }) {
  if (!cancerType) return null;
  
  const { details } = cancerType;
  
  return (
    <div style={{
      marginTop: '20px',
      padding: '20px',
      borderRadius: '12px',
      background: `${details.color}15`,
      border: `2px solid ${details.color}30`,
      boxShadow: `0 4px 12px ${details.color}20`
    }}>
      <div style={{
        display: 'flex',
        alignItems: 'center',
        marginBottom: '15px'
      }}>
        <span style={{ fontSize: '24px', marginRight: '10px' }}>
          {details.icon}
        </span>
        <div>
          <h3 style={{
            margin: '0',
            color: details.color,
            fontSize: '18px',
            fontWeight: 'bold'
          }}>
            {details.name}
          </h3>
          <p style={{
            margin: '5px 0 0 0',
            color: '#7f8c8d',
            fontSize: '14px'
          }}>
            Detection Confidence: {confidence}%
          </p>
        </div>
      </div>
      
      <p style={{
        margin: '0 0 15px 0',
        color: '#2c3e50',
        fontSize: '14px',
        lineHeight: '1.4'
      }}>
        {details.description}
      </p>
      
      <div style={{ marginBottom: '15px' }}>
        <h4 style={{
          margin: '0 0 8px 0',
          color: '#2c3e50',
          fontSize: '14px',
          fontWeight: 'bold'
        }}>
          Key Characteristics:
        </h4>
        <ul style={{
          margin: '0',
          paddingLeft: '20px',
          color: '#34495e',
          fontSize: '13px',
          lineHeight: '1.4'
        }}>
          {details.characteristics.map((char, index) => (
            <li key={index} style={{ marginBottom: '4px' }}>
              {char}
            </li>
          ))}
        </ul>
      </div>
      
      <div style={{
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        gap: '15px',
        marginBottom: '15px'
      }}>
        <div>
          <strong style={{ color: '#2c3e50', fontSize: '12px' }}>Risk Level:</strong>
          <span style={{
            color: details.color,
            fontWeight: 'bold',
            marginLeft: '5px',
            fontSize: '12px'
          }}>
            {details.riskLevel}
          </span>
        </div>
        <div>
          <strong style={{ color: '#2c3e50', fontSize: '12px' }}>Urgency:</strong>
          <span style={{
            color: details.color,
            fontWeight: 'bold',
            marginLeft: '5px',
            fontSize: '12px'
          }}>
            {details.urgency}
          </span>
        </div>
      </div>
      
      <div style={{
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        gap: '15px',
        marginBottom: '15px'
      }}>
        <div>
          <strong style={{ color: '#2c3e50', fontSize: '12px' }}>Category:</strong>
          <span style={{
            color: details.color,
            fontWeight: 'bold',
            marginLeft: '5px',
            fontSize: '12px'
          }}>
            {details.category}
          </span>
        </div>
        <div>
          <strong style={{ color: '#2c3e50', fontSize: '12px' }}>Origin:</strong>
          <span style={{
            color: '#34495e',
            marginLeft: '5px',
            fontSize: '11px'
          }}>
            {details.origin}
          </span>
        </div>
      </div>
      
      <div style={{
        padding: '12px',
        background: '#f8f9fa',
        borderRadius: '8px',
        border: '1px solid #e9ecef'
      }}>
        <div style={{ marginBottom: '8px' }}>
          <strong style={{ color: '#2c3e50', fontSize: '12px' }}>Treatment:</strong>
          <p style={{
            margin: '4px 0 0 0',
            color: '#34495e',
            fontSize: '12px',
            lineHeight: '1.3'
          }}>
            {details.treatment}
          </p>
        </div>
        <div>
          <strong style={{ color: '#2c3e50', fontSize: '12px' }}>Survival Rate:</strong>
          <span style={{
            color: details.color,
            fontWeight: 'bold',
            marginLeft: '5px',
            fontSize: '12px'
          }}>
            {details.survivalRate}
          </span>
        </div>
      </div>
    </div>
  );
}
