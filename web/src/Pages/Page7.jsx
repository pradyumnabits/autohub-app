import React, { useState } from 'react';
import HomeLayout from "../Layouts/HomeLayout";
import axios from 'axios';
import { Link } from 'react-router-dom';

function Page7() {
  return (
    <HomeLayout>
      <FeedbackForm />
    </HomeLayout>
  );
}

function FeedbackForm() {
  const [formData, setFormData] = useState({
    user_id: JSON.parse(localStorage.getItem('user'))?.userName || '',
    feedback_type: '',
    reference_id: '',
    details: '',
    rating: '',
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  // Define feedback type options to match backend enum
  const feedbackTypes = [
    "vehicle",
    "service", 
    "dealership"
  ];

  // Define rating options
  const ratingOptions = [1, 2, 3, 4, 5];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      const response = await axios.post(
        "http://localhost:8006/feedback/submit",
        {
          user_id: formData.user_id,
          feedback_type: formData.feedback_type,
          reference_id: formData.reference_id,
          details: formData.details,
          rating: parseInt(formData.rating),
        }
      );

      setSuccess(true);
      setFormData(prev => ({
        user_id: prev.user_id,
        feedback_type: '',
        reference_id: '',
        details: '',
        rating: '',
      }));

    } catch (error) {
      setError(error.response?.data?.message || 'Failed to submit feedback');
      console.error("Error submitting feedback:", error);
    } finally {
      setLoading(false);
      setTimeout(() => setSuccess(false), 2000);
    }
  };

  return (
    <div className="bg-gray-700 min-h-screen p-8 text-white">
      <h1 className="text-2xl font-semibold mb-6 text-center">
        Feedback Form
      </h1>

      {error && (
        <div className="mb-4 p-4 bg-red-500 text-white rounded-md">
          {error}
        </div>
      )}
      
      {success && (
        <div className="mb-4 p-4 bg-green-500 text-white rounded-md">
          Feedback submitted successfully!
        </div>
      )}

      <form onSubmit={handleSubmit} className="max-w-2xl mx-auto bg-gray-800 p-6 rounded-lg shadow-lg">
        <div className="space-y-4">
          <div>
            <label className="block text-gray-300 mb-2">Feedback Type</label>
            <select
              value={formData.feedback_type}
              onChange={(e) => setFormData(prev => ({ ...prev, feedback_type: e.target.value }))}
              className="w-full p-2 bg-gray-700 text-gray-300 rounded-md"
              required
            >
              <option value="">Select Feedback Type</option>
              {feedbackTypes.map((type) => (
                <option key={type} value={type}>
                  {type.charAt(0).toUpperCase() + type.slice(1)} Feedback
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-gray-300 mb-2">Reference ID</label>
            <input
              type="text"
              value={formData.reference_id}
              onChange={(e) => setFormData(prev => ({ ...prev, reference_id: e.target.value }))}
              className="w-full p-2 bg-gray-700 text-gray-300 rounded-md"
              placeholder="Service or Booking Reference ID"
              required
            />
          </div>

          <div>
            <label className="block text-gray-300 mb-2">Details</label>
            <textarea
              value={formData.details}
              onChange={(e) => setFormData(prev => ({ ...prev, details: e.target.value }))}
              className="w-full p-2 bg-gray-700 text-gray-300 rounded-md h-32"
              placeholder="Please provide your feedback details..."
              required
            />
          </div>

          <div>
            <label className="block text-gray-300 mb-2">Rating</label>
            <select
              value={formData.rating}
              onChange={(e) => setFormData(prev => ({ ...prev, rating: e.target.value }))}
              className="w-full p-2 bg-gray-700 text-gray-300 rounded-md"
              required
            >
              <option value="">Select Rating</option>
              {ratingOptions.map((rating) => (
                <option key={rating} value={rating}>
                  {rating} {rating === 1 ? 'Star' : 'Stars'}
                </option>
              ))}
            </select>
          </div>

          <div className="flex justify-center mt-6">
            <button
              type="submit"
              disabled={loading}
              className={`
                bg-blue-600 text-white font-medium py-2 px-6 rounded-md transition duration-200 text-lg
                ${loading ? 'opacity-50 cursor-not-allowed' : 'hover:bg-blue-700'}
              `}
            >
              {loading ? 'Submitting...' : 'Submit Feedback'}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}

export default Page7;