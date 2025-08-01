import React, { useState } from 'react';
import { Link,useLocation } from 'react-router-dom';
import { ArrowLeft, MapPin, Loader2, Navigation, Brain, Network } from 'lucide-react';
import { predictLSTM, predictGNN } from '../utils/api';

interface LocationResult {
  predicted_tower_id: string;
  latitude: number;
  longitude: number;
  address?: string;
  timestamp: string;
}

const LastKnownLocation: React.FC = () => {
 const location = useLocation();
const initialAccountId = (location.state as any)?.accountId?.toString() || '20002';
const [accountId, setAccountId] = useState(initialAccountId);

  const [loadingLSTM, setLoadingLSTM] = useState(false);
  const [loadingGNN, setLoadingGNN] = useState(false);
  const [lstmResult, setLstmResult] = useState<LocationResult | null>(null);
  const [gnnResult, setGnnResult] = useState<LocationResult | null>(null);

  const handleLSTMSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!accountId.trim()) return;

    setLoadingLSTM(true);
    setLstmResult(null);

    try {
      const locationData = await predictLSTM(parseInt(accountId));
      setLstmResult({
        ...locationData,
        timestamp: new Date().toLocaleString()
      });
    } catch (error) {
      console.error('LSTM prediction failed:', error);
    } finally {
      setLoadingLSTM(false);
    }
  };

  const handleGNNSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!accountId.trim()) return;

    setLoadingGNN(true);
    setGnnResult(null);

    try {
      const locationData = await predictGNN(parseInt(accountId));
      setGnnResult({
        ...locationData,
        timestamp: new Date().toLocaleString()
      });
    } catch (error) {
      console.error('GNN prediction failed:', error);
    } finally {
      setLoadingGNN(false);
    }
  };

  const ResultCard = ({ result, title, icon }: { result: LocationResult; title: string; icon: React.ReactNode }) => (
    <div className="bg-blue-50 border border-blue-200 p-6 rounded-xl">
      <div className="flex items-center justify-center mb-4">
        {icon}
        <h3 className="text-2xl font-bold text-sbi-blue ml-3">
          {title} Result
        </h3>
      </div>
      
      <div className="space-y-4">
        <div className="text-center">
          <h4 className="font-semibold text-gray-700 mb-2">Predicted Tower ID</h4>
          <p className="text-2xl font-bold text-sbi-blue bg-white px-4 py-2 rounded-lg inline-block">
            {result.predicted_tower_id}
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          <div className="text-center">
            <h4 className="font-semibold text-gray-700 mb-2">Latitude</h4>
            <p className="text-xl font-bold text-sbi-blue">
              {result.latitude.toFixed(6)}
            </p>
          </div>
          <div className="text-center">
            <h4 className="font-semibold text-gray-700 mb-2">Longitude</h4>
            <p className="text-xl font-bold text-sbi-blue">
              {result.longitude.toFixed(6)}
            </p>
          </div>
        </div>

        {result.address && (
          <div className="text-center">
            <h4 className="font-semibold text-gray-700 mb-2">Tower Location</h4>
            <p className="text-gray-600">{result.address}</p>
          </div>
        )}

        <div className="text-center">
          <p className="text-sm text-gray-500">
            Predicted at: {result.timestamp}
          </p>
        </div>

        {/* Map Link */}
        <div className="text-center">
          <a
            href={`https://www.google.com/maps?q=${result.latitude},${result.longitude}`}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center bg-sbi-blue text-white px-6 py-2 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
          >
            <MapPin className="w-4 h-4 mr-2" />
            View on Google Maps
          </a>
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-white">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex items-center mb-8">
          <Link 
            to="/" 
            className="flex items-center text-sbi-blue hover:text-blue-700 transition-colors mr-4"
          >
            <ArrowLeft className="w-5 h-5 mr-2" />
            Back to Home
          </Link>
        </div>

        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-8">
            <div className="flex items-center justify-center mb-4">
              <MapPin className="w-8 h-8 text-sbi-blue mr-3" />
              <h1 className="text-3xl font-bold text-sbi-blue">Location Prediction</h1>
            </div>
            <p className="text-gray-600">
              Predict customer location using LSTM and GNN models
            </p>
          </div>

          {/* Account ID Input */}
          <div className="bg-white rounded-2xl shadow-lg p-6 mb-8">
            <div className="max-w-md mx-auto">
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Account ID
              </label>
              <input
                type="number"
                value={accountId}
                onChange={(e) => setAccountId(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-sbi-blue focus:border-transparent transition-all text-center text-lg font-semibold"
                placeholder="Enter Account ID"
                required
              />
            </div>
          </div>

          {/* Prediction Sections */}
          <div className="grid lg:grid-cols-2 gap-8">
            {/* LSTM Prediction */}
            <div className="bg-white rounded-2xl shadow-lg p-8">
              <div className="text-center mb-6">
                <div className="flex items-center justify-center mb-4">
                  <Brain className="w-8 h-8 text-sbi-blue mr-3" />
                  <h2 className="text-2xl font-bold text-sbi-blue">LSTM Prediction</h2>
                </div>
                <p className="text-gray-600">
                  Long Short-Term Memory neural network prediction
                </p>
              </div>

              <form onSubmit={handleLSTMSubmit} className="space-y-6">
                <div className="flex justify-center">
                  <button
                    type="submit"
                    disabled={!accountId.trim() || loadingLSTM}
                    className="bg-sbi-blue text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-all duration-200 flex items-center min-w-[200px] justify-center"
                  >
                    {loadingLSTM ? (
                      <>
                        <Loader2 className="w-5 h-5 animate-spin mr-2" />
                        Predicting...
                      </>
                    ) : (
                      <>
                        <Brain className="w-5 h-5 mr-2" />
                        Predict with LSTM
                      </>
                    )}
                  </button>
                </div>
              </form>

              {/* LSTM Result */}
              {lstmResult && (
                <div className="mt-8 pt-8 border-t border-gray-200">
                  <ResultCard 
                    result={lstmResult} 
                    title="LSTM" 
                    icon={<Brain className="w-8 h-8 text-sbi-blue" />} 
                  />
                </div>
              )}
            </div>

            {/* GNN Prediction */}
            <div className="bg-white rounded-2xl shadow-lg p-8">
              <div className="text-center mb-6">
                <div className="flex items-center justify-center mb-4">
                  <Network className="w-8 h-8 text-sbi-blue mr-3" />
                  <h2 className="text-2xl font-bold text-sbi-blue">GNN Prediction</h2>
                </div>
                <p className="text-gray-600">
                  Graph Neural Network prediction
                </p>
              </div>

              <form onSubmit={handleGNNSubmit} className="space-y-6">
                <div className="flex justify-center">
                  <button
                    type="submit"
                    disabled={!accountId.trim() || loadingGNN}
                    className="bg-sbi-blue text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-all duration-200 flex items-center min-w-[200px] justify-center"
                  >
                    {loadingGNN ? (
                      <>
                        <Loader2 className="w-5 h-5 animate-spin mr-2" />
                        Predicting...
                      </>
                    ) : (
                      <>
                        <Network className="w-5 h-5 mr-2" />
                        Predict with GNN
                      </>
                    )}
                  </button>
                </div>
              </form>

              {/* GNN Result */}
              {gnnResult && (
                <div className="mt-8 pt-8 border-t border-gray-200">
                  <ResultCard 
                    result={gnnResult} 
                    title="GNN" 
                    icon={<Network className="w-8 h-8 text-sbi-blue" />} 
                  />
                </div>
              )}
            </div>
          </div>

          {/* Comparison Section */}
          {lstmResult && gnnResult && (
            <div className="mt-8 bg-white rounded-2xl shadow-lg p-8">
              <div className="text-center mb-6">
                <h3 className="text-2xl font-bold text-sbi-blue mb-2">Model Comparison</h3>
                <p className="text-gray-600">Compare predictions from both models</p>
              </div>
              
              <div className="grid md:grid-cols-2 gap-6">
                <div className="text-center p-4 bg-blue-50 rounded-lg">
                  <h4 className="font-semibold text-sbi-blue mb-2">LSTM Model</h4>
                  <p className="text-lg font-bold">{lstmResult.predicted_tower_id}</p>
                  <p className="text-sm text-gray-600">{lstmResult.address}</p>
                </div>
                <div className="text-center p-4 bg-blue-50 rounded-lg">
                  <h4 className="font-semibold text-sbi-blue mb-2">GNN Model</h4>
                  <p className="text-lg font-bold">{gnnResult.predicted_tower_id}</p>
                  <p className="text-sm text-gray-600">{gnnResult.address}</p>
                </div>
              </div>

              {lstmResult.predicted_tower_id === gnnResult.predicted_tower_id ? (
                <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg text-center">
                  <p className="text-green-800 font-semibold">✓ Both models agree on the prediction</p>
                </div>
              ) : (
                <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg text-center">
                  <p className="text-yellow-800 font-semibold">⚠ Models have different predictions</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default LastKnownLocation;