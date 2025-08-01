export interface PredictionResult {
  isDefaulter: boolean;
  confidence: number;
}

export interface LocationResult {
  predicted_tower_id: string;
  latitude: number;
  longitude: number;
  address?: string;
}

let towerData: Record<string, { latitude: number; longitude: number; address: string }> = {};

const loadTowerData = async () => {
  const response = await fetch('/fake_tower_logs_with_indian_cities.json');
  const rawData = await response.json();

  towerData = rawData.reduce((acc: typeof towerData, item: any) => {
    acc[item.tower_id] = {
      latitude: item.latitude,
      longitude: item.longitude,
      address: item.city // Use city as address
    };
    return acc;
  }, {});
};

// Load data immediately
loadTowerData();



// Mock API delay function
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

// Mock Defaulter Prediction API
export const predictDefaulter = async (formData: any): Promise<PredictionResult> => {
  // Simulate API delay
  await delay(2000 + Math.random() * 1000);

  // Mock logic based on some form data
  const income = parseInt(formData.income) || 0;
  const loanAmount = parseInt(formData.loanAmount) || 0;
  const creditScore = parseInt(formData.creditScore) || 0;
  const age = parseInt(formData.age) || 0;
  const existingLoans = parseInt(formData.existingLoans) || 0;

  // Simple mock algorithm
  let riskScore = 0;

  // Income to loan ratio risk
  const incomeRatio = loanAmount / income;
  if (incomeRatio > 5) riskScore += 30;
  else if (incomeRatio > 3) riskScore += 20;
  else if (incomeRatio > 2) riskScore += 10;

  // Credit score risk
  if (creditScore < 600) riskScore += 35;
  else if (creditScore < 700) riskScore += 20;
  else if (creditScore < 750) riskScore += 10;

  // Age risk
  if (age < 25 || age > 60) riskScore += 15;

  // Existing loans risk
  riskScore += existingLoans * 5;

  // Employment type risk
  if (formData.employmentType === 'unemployed') riskScore += 40;
  else if (formData.employmentType === 'self-employed') riskScore += 15;

  // Add some randomness
  riskScore += Math.random() * 20 - 10;

  // Ensure score is between 0 and 100
  riskScore = Math.max(0, Math.min(100, riskScore));

  const isDefaulter = riskScore > 50;
  const confidence = Math.round(isDefaulter ? riskScore : 100 - riskScore);

  return {
    isDefaulter,
    confidence
  };
};

// LSTM Prediction API

export const predictLSTM = async (accountId: number): Promise<LocationResult> => {
  try {
    const response = await fetch('http://localhost:9000/predict/lstm', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({ account_id: accountId })
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    const { predicted_tower_id } = await response.json();

const tower = towerData[predicted_tower_id];

    if (!tower) {
      throw new Error(`Unknown tower ID: ${predicted_tower_id}`);
    }

    // Add random offset to simulate LSTM variation
    const latVariation = (Math.random() - 0.5) * 0.01;
    const lonVariation = (Math.random() - 0.5) * 0.01;

    return {
      predicted_tower_id,
      latitude: tower.latitude + latVariation,
      longitude: tower.longitude + lonVariation,
      address: tower.address
    };
  } catch (error) {
    console.error("Failed to fetch LSTM prediction:", error);
    throw error;
  }
};
//  GNN Prediction API
export const predictGNN = async (accountId: number): Promise<LocationResult> => {
  try {
    const response = await fetch('http://localhost:9000/predict/gnn', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({ account_id: accountId })
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    const { predicted_tower_id } = await response.json();

const tower = towerData[predicted_tower_id];

    if (!tower) {
      throw new Error(`Unknown tower ID: ${predicted_tower_id}`);
    }

    // Add random offset to simulate LSTM variation
    const latVariation = (Math.random() - 0.5) * 0.01;
    const lonVariation = (Math.random() - 0.5) * 0.01;

    return {
      predicted_tower_id,
      latitude: tower.latitude + latVariation,
      longitude: tower.longitude + lonVariation,
      address: tower.address
    };
  } catch (error) {
    console.error("Failed to fetch GNN prediction:", error);
    throw error;
  }
};