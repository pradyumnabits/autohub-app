import React from 'react';

function Snackbar({ message, isVisible, onClose }) {
  if (!isVisible) return null;

  return (
    <div className="fixed bottom-4 right-4 flex items-center bg-green-500 text-white px-6 py-3 rounded-md shadow-lg animate-slide-up">
      <span>{message}</span>
      <button 
        onClick={onClose} 
        className="ml-4 text-white hover:text-gray-200"
      >
        ×
      </button>
    </div>
  );
}

export default Snackbar; 