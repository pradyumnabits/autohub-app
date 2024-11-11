import React, { useState, useEffect } from "react";
import axios from "axios";
import HomeLayout from "../Layouts/HomeLayout";
import Lottie from 'lottie-react';
import carAnimation from '../assets/Images/SSO_Icons/car-loading.json'; // Update path as needed
import Snackbar from '../components/Snackbar'; // Add this import
// page for Post seals service management
function Page4() {
  return (
    <HomeLayout>
      <PostSaleServiceManagement />
    </HomeLayout>
  );
}

function PostSaleServiceManagement() {
  const [bookedVehicles, setBookedVehicles] = useState([]);
  const [serviceHistory, setServiceHistory] = useState([]);
  const [loadingVehicles, setLoadingVehicles] = useState(true);
  const [loadingHistory, setLoadingHistory] = useState(true);
  const [selectedVehicle, setSelectedVehicle] = useState(null);
  const [serviceType, setServiceType] = useState("");
  const [appointmentDate, setAppointmentDate] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [showSnackbar, setShowSnackbar] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');

  // Fetch booked vehicles
  useEffect(() => {
    const user = localStorage.getItem("user");
    const userId = JSON.parse(user);
    const fetchBookedVehicles = async () => {
      try {
        const response = await axios.get(
          `http://localhost:8003/bookings?user_name=${userId.userName}`
        );
        setBookedVehicles(response.data);
      } catch (error) {
        console.error("Error fetching booked vehicles:", error);
      } finally {
        setLoadingVehicles(false);
      }
    };
    fetchBookedVehicles();
  }, []);

  // Fetch service history
  useEffect(() => {
    const user = localStorage.getItem("user");
    const userId = JSON.parse(user);
    const fetchServiceHistory = async () => {
      try {
        const response = await axios.get(
          `http://localhost:8004/service/history?user_id=${userId.userName}`
        );
        setServiceHistory(response.data);
      } catch (error) {
        console.error("Error fetching service history:", error);
      } finally {
        setLoadingHistory(false);
      }
    };
    fetchServiceHistory();
  }, []);

  const handleOpenModal = (vehicle) => {
    setSelectedVehicle(vehicle);
  };

  const handleCloseModal = () => {
    setSelectedVehicle(null);
    setServiceType("");
    setAppointmentDate("");
  };

  // Submit new service request
  const handleAppointmentSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    const user = localStorage.getItem("user");
    const userId = JSON.parse(user);
    try {
      const response = await axios.post(
        "http://localhost:8004/service/schedule",
        {
          vehicle_id: selectedVehicle.id,
          service_type: serviceType,
          appointment_date: appointmentDate,
          user_id: userId.userName,
        }
      );
      setServiceHistory([...serviceHistory, response.data]);
      handleCloseModal();
      
      // Show success snackbar
      setSnackbarMessage('Service appointment scheduled successfully!');
      setShowSnackbar(true);
      
      // Hide snackbar after 3 seconds
      setTimeout(() => {
        setShowSnackbar(false);
      }, 3000);
      
    } catch (error) {
      console.error("Error submitting service request:", error);
      // Optionally show error snackbar
      setSnackbarMessage('Failed to schedule appointment. Please try again.');
      setShowSnackbar(true);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (loadingVehicles || loadingHistory) {
    return (
      <div className="p-6 flex items-center justify-center bg-gray-700" style={{ minHeight: "calc(100vh - 64px)" }}>
        <div className="text-center">
          <div className="w-48 h-48 mx-auto"> {/* Adjust size as needed */}
            <Lottie
              animationData={carAnimation}
              loop={true}
              autoplay={true}
            />
          </div>
          <p className="text-xl text-white">Loading support services...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-700 text-white p-6">
      <h1 className="text-2xl font-semibold mb-6 text-center">
        Support Service
      </h1>

      {/* Booked Vehicles */}
      <div className="bg-gray-900 p-6 rounded-md shadow-lg w-full max-w-6xl mx-auto mt-8">
        <h2 className="text-2xl font-semibold mb-6 text-center text-white">
          Booked Vehicles
        </h2>

        {loadingVehicles ? (
          <p className="text-center text-gray-400">
            Loading booked vehicles...
          </p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {bookedVehicles.length > 0 ? (
              bookedVehicles.map((bvehicle) => (
                <div
                  key={bvehicle.id}
                  className="bg-gray-800 p-4 rounded-lg shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 cursor-pointer"
                  onClick={() => handleOpenModal(bvehicle.vehicle)}
                >
                  <img
                    src={bvehicle.vehicle.image_url}
                    alt={bvehicle.vehicle.model}
                    className="w-full h-40 object-cover rounded-md mb-4"
                  />
                  <div className="p-2">
                    <h3 className="text-lg font-semibold text-blue-400">
                      {`${bvehicle.vehicle.make} ${bvehicle.vehicle.model}`}
                    </h3>
                    <p className="text-gray-400 mt-2">
                      <strong>Fuel Type:</strong> {bvehicle.vehicle.fuel_type}
                    </p>
                    <p className="text-gray-400 mt-1">
                      <strong>Body Type:</strong> {bvehicle.vehicle.body_type}
                    </p>
                    <p className="text-gray-400 mt-1">
                      <strong>Year:</strong> {bvehicle.vehicle.year}
                    </p>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-center col-span-full text-gray-400">
                No car is booked. Please book a car for this service.
              </p>
            )}
          </div>
        )}
      </div>

      {/* Service History */}
      <div className="bg-gray-800 p-6 rounded-md shadow-md w-full max-w-6xl mx-auto mt-8">
        <h2 className="text-2xl font-semibold mb-4 text-center text-white">
          Service History
        </h2>

        {loadingHistory ? (
          <p className="text-center text-gray-400">
            Loading service history...
          </p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {serviceHistory.length === 0 ? (
              <p className="text-gray-300 text-center col-span-full">
                No service history available.
              </p>
            ) : (
              serviceHistory.map((service, index) => (
                <div
                  key={index}
                  className="bg-gray-700 rounded-lg shadow-lg overflow-hidden transform transition-all duration-300 hover:scale-105"
                >
                  <img
                    src={service.vehicle_details.image_url}
                    alt={`${service.vehicle_details.make} ${service.vehicle_details.model}`}
                    className="w-full h-48 object-cover"
                  />
                  <div className="p-4">
                    <h3 className="text-lg font-semibold text-blue-400">
                      {service.vehicle_details.make}{" "}
                      {service.vehicle_details.model}
                    </h3>
                    <p className="text-gray-300 mt-2">
                      <strong>Service Type:</strong> {service.service_type}
                    </p>
                    <p className="text-gray-300 mt-2">
                      <strong>Date:</strong> {service.service_date}
                    </p>
                    <p className="text-gray-300 mt-2">
                      <strong>Description:</strong> {service.description}
                    </p>
                  </div>
                </div>
              ))
            )}
          </div>
        )}
      </div>

      {/* Appointment Scheduling Modal */}
      {selectedVehicle && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="bg-gray-800 p-6 rounded-md shadow-md w-full max-w-lg relative">
            <button
              onClick={handleCloseModal}
              className="absolute top-2 right-2 text-gray-400 hover:text-white"
            >
              &times;
            </button>
            <h2 className="text-2xl font-semibold mb-4">
              {`${selectedVehicle.make} ${selectedVehicle.model}`}
            </h2>
            <img
              src={selectedVehicle.image_url}
              alt={selectedVehicle.model}
              className="w-full h-48 object-cover rounded-md mb-4"
            />
            <form onSubmit={handleAppointmentSubmit} className="space-y-4">
              <div>
                <label className="block text-gray-300 mb-2">Service Type</label>
                <input
                  type="text"
                  value={serviceType}
                  onChange={(e) => setServiceType(e.target.value)}
                  className="w-full p-2 bg-gray-700 text-gray-300 rounded-md"
                  placeholder="e.g., Oil Change, Brake Inspection"
                  required
                />
              </div>

              <div>
                <label className="block text-gray-300 mb-2">
                  Appointment Date
                </label>
                <input
                  type="date"
                  value={appointmentDate}
                  onChange={(e) => setAppointmentDate(e.target.value)}
                  className="w-full p-2 bg-gray-700 text-gray-300 rounded-md"
                  required
                />
              </div>

              <button
                type="submit"
                className="w-full bg-blue-600 p-3 rounded-md hover:bg-blue-700 transition"
                disabled={isSubmitting}
              >
                {isSubmitting ? "Submitting..." : "Schedule Appointment"}
              </button>
            </form>
          </div>
        </div>
      )}

      {/* Add Snackbar */}
      <Snackbar
        message={snackbarMessage}
        isVisible={showSnackbar}
        onClose={() => setShowSnackbar(false)}
      />
    </div>
  );
}

export default Page4;
