import React, { useState, useEffect } from "react";
import HomeLayout from "../Layouts/HomeLayout";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";

// page for vehicle list
function Page2() {
  return (
    <HomeLayout>
      <VehiclePage />
    </HomeLayout>
  );
}

function VehiclePage() {
  const [vehicles, setVehicles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedVehicle, setSelectedVehicle] = useState(null);

  console.log("selectedvehicle", selectedVehicle);

  useEffect(() => {
    const fetchVehicles = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8002/vehicles");
        setVehicles(response.data);
        console.log("vehicles", response.data);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching vehicles:", error);
        setLoading(false);
      }
    };

    fetchVehicles();
  }, []);

  return (
    <div className="bg-gray-700 min-h-screen p-6 text-white">
      <h1 className="text-2xl font-semibold mb-6">Vehicle List</h1>

      {loading ? (
        <Shimmer />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {vehicles.map((vehicle) => (
            <VehicleCard
              key={vehicle.id}
              vehicle={vehicle}
              onSelect={() => setSelectedVehicle(vehicle)}
            />
          ))}
        </div>
      )}

      {selectedVehicle && (
        <VehicleDetails
          vehicle={selectedVehicle}
          onClose={() => setSelectedVehicle(null)}
        />
      )}
    </div>
  );
}

// Shimmer component for loading effect
function Shimmer() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {[...Array(6)].map((_, index) => (
        <div
          key={index}
          className="bg-gray-800 p-4 rounded-md animate-pulse h-40"
        ></div>
      ))}
    </div>
  );
}

// Vehicle Card component for list view
function VehicleCard({ vehicle, onSelect }) {
  return (
    <div
      className="bg-gray-800 p-4 rounded-lg shadow-lg transform hover:scale-105 hover:shadow-xl transition-all duration-300 cursor-pointer relative"
      onClick={onSelect}
    >
      {/* Image with a subtle overlay effect */}
      <div className="relative overflow-hidden rounded-md">
        <img
          src={vehicle.image_url}
          alt={`${vehicle.make} ${vehicle.model}`}
          className="w-full h-40 object-cover rounded-md transition-all duration-300"
        />
        <div className="absolute inset-0 bg-black bg-opacity-20 rounded-md hover:bg-opacity-30 transition-opacity duration-300" />
      </div>

      {/* Vehicle Information */}
      <div className="mt-4 text-center">
        <h2 className="text-xl font-bold text-blue-400">
          {`${vehicle.make} ${vehicle.model}`}
        </h2>
        <p className="text-gray-400 mt-1">{vehicle.fuel_type}</p>
        <p className="text-sm text-gray-500">{vehicle.year}</p>
      </div>

      {/* Button or Additional Action */}
      <button className="mt-4 bg-blue-600 text-white px-4 py-2 rounded-md w-full transition-all duration-300 hover:bg-blue-700">
        View Details
      </button>
    </div>
  );
}

// Vehicle Details component for expanded view
function VehicleDetails({ vehicle, onClose }) {
  const navigate = useNavigate();
  return (
    <div className="fixed inset-0 bg-gray-900 bg-opacity-75 flex items-center justify-center p-4">
      <div className="bg-gray-800 p-6 rounded-md shadow-lg max-w-md w-full">
        <button onClick={onClose} className="text-right text-gray-400 mb-4">
          Close
        </button>
        <img
          src={vehicle.image_url}
          alt={`${vehicle.make} ${vehicle.model}`}
          className="w-full h-40 object-cover rounded-md mb-4"
        />
        <h2 className="text-xl font-semibold mb-2">{`${vehicle.make} ${vehicle.model}`}</h2>
        <div className="text-gray-400 mb-4">{vehicle.year}</div>
        <h3 className="font-semibold text-lg mb-1">Specifications</h3>
        <ul className="text-gray-400 mb-4">
          <li>Price: ${vehicle.price}</li>
          <li>Fuel Type: {vehicle.fuel_type}</li>
          <li>Transmission: {vehicle.transmission}</li>
          <li>Body Type: {vehicle.body_type}</li>
        </ul>

        <div className="flex justify-center mt-4 space-x-4">
          <button
            className="bg-indigo-500 text-white px-4 py-2 rounded-md hover:bg-indigo-600"
            onClick={() => {
              navigate("/testdrivebook", {
                state: {
                  vehicle: vehicle,
                },
              });
            }}
          >
            Book for Test Drive
          </button>
          <button
            className="bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600"
            onClick={() => {
              navigate("/book", {
                state: {
                  vehicle: vehicle,
                },
              });
            }}
          >
            Book The Vehicle
          </button>
        </div>
      </div>
    </div>
  );
}

export default Page2;
