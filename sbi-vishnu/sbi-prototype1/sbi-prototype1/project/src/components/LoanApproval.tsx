import React, { useState } from 'react';
import axios from 'axios';

const LoanApprover: React.FC = () => {
  const [userId, setUserId] = useState('');
  const [prediction, setPrediction] = useState('');
  const [error, setError] = useState('');

 const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();
  setPrediction('');
  setError('');

  try {
    const res = await axios.get(`http://localhost:8000/target/${userId}`);
    const target = res.data?.TARGET;
    console.log("API Response:", res.data);

    if (target === 0) {
      setPrediction('Low Risk');
    } else if (target === 1) {
      setPrediction('High Risk');
    } else {
      setPrediction(`Unknown Risk Level (TARGET=${target})`);
    }
  } catch (err) {
    setError('User not found or API error');
  }
};


  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 p-4">
      <div className="bg-white shadow-xl rounded-2xl p-8 w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6 text-center">Loan Approver</h2>
        <form onSubmit={handleSubmit}>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Enter Unique ID
          </label>
          <input
            type="text"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            className="w-full px-4 py-2 border rounded-lg mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="e.g., 1234"
            required
          />
          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Predict
          </button>
        </form>

        {prediction && (
          <div className="mt-6 p-4 bg-green-100 border border-green-400 text-green-700 rounded-lg">
            <strong>Prediction:</strong> {prediction}
          </div>
        )}

        {error && (
          <div className="mt-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
            <strong>Error:</strong> {error}
          </div>
        )}
      </div>
    </div>
  );
};

export default LoanApprover;
