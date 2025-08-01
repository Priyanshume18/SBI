import React, { useState } from 'react';
import { ArrowLeft, Loader2, MapPin, Mail } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import Papa from 'papaparse';

const API_URL = "http://localhost:8000/predict_batch"; 
const UNIQUE_ID_FIELD = "UNIQUE_ID"; // Change this to actual column in your CSV

const DefaulterPrediction: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any[]>([]);
  const [predictions, setPredictions] = useState<any[]>([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [sendingEmail, setSendingEmail] = useState<string | null>(null);
  const [emailSent, setEmailSent] = useState<string | null>(null);
  const [showEmailModal, setShowEmailModal] = useState(false);
  const [currentEmailContent, setCurrentEmailContent] = useState<{subject: string; body: string} | null>(null);
  const resultsPerPage = 10;

  const navigate = useNavigate();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.length) setFile(e.target.files[0]);
  };

  const generateEmailContent = (userData: any) => {
    const fields = [
      'UNIQUE_ID', 'OUTS', 'INSTALAMT', 'LOAN_TENURE', 'ACCT_RESIDUAL_TENURE',
      'LATEST_NPA_TENURE', 'CUST_NO_OF_TIMES_NPA', 'LATEST_CR_DAYS',
      'LATEST_DR_DAYS', 'PRODUCT_TYPE', 'INCOME_BAND1', 'TARGET', 'NO_OF_INQUIRIES1'
    ];

    const emailBody = `
Dear Customer,

This is an automated notification regarding your account with State Bank of India.

Account Details:
${fields.map(field => `${field}: ${userData[field] || 'N/A'}`).join('\n')}

Please contact your nearest SBI branch for further assistance.

Best regards,
SBI Analytics Team
State Bank of India
    `.trim();

    return {
      subject: `SBI Account Notification - ${userData.UNIQUE_ID || 'Account Update'}`,
      body: emailBody
    };
  };

  const handleNotifyUser = (userData: Record<string, any>) => {
    const emailContent = generateEmailContent(userData);
    setCurrentEmailContent(emailContent);
    setShowEmailModal(true);
  };

  const handleSendEmail = async () => {
    if (!currentEmailContent) return;
    
    setSendingEmail('sending');
    
    try {
      // Simulate email sending (in production, integrate with Mailtrap API)
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      setEmailSent('sent');
      setShowEmailModal(false);
      
      // Reset the sent status after 3 seconds
      setTimeout(() => setEmailSent(null), 3000);
      
    } catch (error) {
      console.error('Error sending email:', error);
    } finally {
      setSendingEmail(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    setResults([]);
    setPredictions([]);
    setCurrentPage(1);

    Papa.parse(file, {
      header: true,
      skipEmptyLines: true,
      complete: async (parsed) => {
        try {
          const rawData = parsed.data as any[];
          const payload = rawData.map(row => ({ data: row }));

          const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
          });

          if (!response.ok) throw new Error(`HTTP error! ${response.status}`);
          const apiResult = await response.json();

          setResults(rawData);
          setPredictions(apiResult.predictions || []);
        } catch (err) {
          console.error("Prediction error:", err);
        } finally {
          setLoading(false);
        }
      },
      error: (error) => {
        console.error('CSV Parsing Error:', error);
        setLoading(false);
      }
    });
  };

  const paginatedResults = results.slice((currentPage - 1) * resultsPerPage, currentPage * resultsPerPage);
  const paginatedPredictions = predictions.slice((currentPage - 1) * resultsPerPage, currentPage * resultsPerPage);
  const totalPages = Math.ceil(results.length / resultsPerPage);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-white">
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center mb-8">
          <Link to="/" className="flex items-center text-sbi-blue hover:text-blue-700 transition-colors mr-4">
            <ArrowLeft className="w-5 h-5 mr-2" /> Back to Home
          </Link>
        </div>

        <div className="max-w-3xl mx-auto bg-white rounded-2xl shadow-lg p-8">
          <h2 className="text-2xl font-bold text-center text-sbi-blue mb-6">
            Upload CSV for Defaulter Prediction
          </h2>

          <form onSubmit={handleSubmit} className="space-y-4">
            <input
              type="file"
              accept=".csv"
              onChange={handleFileChange}
              required
              className="block w-full text-sm text-gray-700 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-sbi-blue file:text-white hover:file:bg-blue-700"
            />
            <button
              type="submit"
              disabled={loading || !file}
              className="bg-sbi-blue text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-all duration-200 flex items-center justify-center"
            >
              {loading ? (<><Loader2 className="w-5 h-5 animate-spin mr-2" /> Analyzing...</>) : 'Upload and Predict'}
            </button>
          </form>

          {results.length > 0 && (
            <div className="mt-10">
              <h3 className="text-xl font-semibold mb-4">
                Predictions (Page {currentPage}/{totalPages})
              </h3>
              <table className="min-w-full bg-white border">
                <thead>
                  <tr>
                    <th className="border px-4 py-2 text-left text-sm font-medium text-gray-600">{UNIQUE_ID_FIELD}</th>
                    <th className="border px-4 py-2 text-left text-sm font-medium text-gray-600">Prediction</th>
                    <th className="border px-4 py-2 text-left text-sm font-medium text-gray-600">Last Known Location</th>
                    <th className="border px-4 py-2 text-left text-sm font-medium text-gray-600">Notify User</th>
                  </tr>
                </thead>
                <tbody>
                  {paginatedResults.map((row, idx) => (
                    <tr key={idx} className="border-t">
                      <td className="border px-4 py-2 text-sm text-gray-800">{row[UNIQUE_ID_FIELD] ?? "—"}</td>
                      <td className="border px-4 py-2 text-sm font-bold text-blue-600">
                        {paginatedPredictions[idx]?.prediction ?? "—"}
                      </td>
                      <td className="border px-4 py-2 text-center">
                        {paginatedPredictions[idx]?.prediction === 1 && (
                          <button
                            onClick={() => navigate("/last-known-location", { state: { accountId: row[UNIQUE_ID_FIELD] } })}
                            className="bg-green-500 text-white p-2 rounded-full hover:bg-green-600 transition"
                            title="Predict Last Known Location"
                          >
                            <MapPin className="w-4 h-4" />
                          </button>
                        )}
                      </td>
                      <td className="border px-4 py-2 text-center">
                        {paginatedPredictions[idx]?.prediction === 1 && (
                          <button
                            onClick={() => handleNotifyUser(row)}
                            className="bg-blue-500 text-white p-2 rounded-full hover:bg-blue-600 transition"
                            title="Send notification email to user"
                          >
                            <Mail className="w-4 h-4" />
                          </button>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              <div className="flex justify-between items-center mt-6">
                <button onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                  disabled={currentPage === 1}
                  className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300 disabled:opacity-50">Previous</button>
                <button onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                  disabled={currentPage === totalPages}
                  className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300 disabled:opacity-50">Next</button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Email Modal */}
      {showEmailModal && currentEmailContent && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-hidden">
            <div className="p-6 border-b border-gray-200">
              <div className="flex justify-between items-center">
                <h3 className="text-xl font-bold text-sbi-blue">Send Notification Email</h3>
                <button
                  onClick={() => setShowEmailModal(false)}
                  className="text-gray-400 hover:text-gray-600 transition-colors"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
            
            <div className="p-6 overflow-y-auto max-h-[60vh]">
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Subject:</label>
                  <input
                    type="text"
                    value={currentEmailContent.subject}
                    readOnly
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg bg-gray-50 text-gray-700"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Email Content:</label>
                  <div className="border border-gray-300 rounded-lg p-4 bg-gray-50">
                    <pre className="whitespace-pre-wrap text-sm text-gray-700 font-mono">
                      {currentEmailContent.body}
                    </pre>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="p-6 border-t border-gray-200 bg-gray-50">
              <div className="flex justify-end space-x-3">
                <button
                  onClick={() => setShowEmailModal(false)}
                  className="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={handleSendEmail}
                  disabled={sendingEmail === 'sending'}
                  className="bg-sbi-blue text-white px-6 py-2 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-all duration-200 flex items-center space-x-2"
                >
                  {sendingEmail === 'sending' ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      <span>Sending...</span>
                    </>
                  ) : (
                    <>
                      <Mail className="w-4 h-4" />
                      <span>Send Email</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DefaulterPrediction;
