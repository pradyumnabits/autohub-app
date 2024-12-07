import React, { useState } from "react";
import HomeLayout from "../Layouts/HomeLayout";
import { useLocation } from "react-router-dom";
import axios from "axios";
import { AllUrl } from "../Helpers/allUrl";

function Page6() {
  const location = useLocation();
  const vehicleData = location.state.vehicle;
  return (
    <HomeLayout>
      <CarPurchasePage vehicle={vehicleData} />
    </HomeLayout>
  );
}

function CarPurchasePage({ vehicle }) {
  const [transactionId, setTransactionId] = useState("");
  const [transactionDate, setTransactionDate] = useState("");
  const [transactionPrice, setTransactionPrice] = useState(vehicle.price || 0);
  const [transactionMethod, setTransactionMethod] = useState("");
  const [isPurchasing, setIsPurchasing] = useState(false);
  const [purchaseStatus, setPurchaseStatus] = useState(null);

  const handlePurchase = () => {
    if (!transactionId || !transactionDate || !transactionMethod) {
      alert("Please fill in all required fields.");
      return;
    }

    setIsPurchasing(true);
    const user = localStorage.getItem("user");
    const userId = JSON.parse(user);

    const data = {
      user_name: userId.userName,
      vehicle_id: vehicle.id,
      transaction_id: transactionId,
      transaction_date: transactionDate,
      transaction_price: Number(transactionPrice),
      transaction_method: transactionMethod,
    };

    axios
      .post(`${AllUrl.bookingServiceUrl}/bookings`, data)
      .then((response) => {
        setPurchaseStatus(response.data.message || "Purchase successful!");
        setIsPurchasing(false);
      })
      .catch((error) => {
        console.error("Purchase error:", error);
        setPurchaseStatus("Purchase failed. Please try again.");
        setIsPurchasing(false);
      });
  };

  return (
    <div className="bg-gray-700 min-h-screen p-8 text-white">
      {/* Car Details Section */}
      <section className="bg-gray-800 p-6 rounded-md shadow-md mb-6">
        <img
          src={vehicle.image_url}
          alt={vehicle.model}
          className="w-full h-64 object-cover rounded-md mb-4"
        />
        <h3 className="text-2xl font-semibold">{vehicle.model}</h3>
        <p className="text-lg font-semibold text-gray-400 mb-2">
          Price: ₹{vehicle.price}
        </p>
        <p className="text-gray-400 mb-1">Fuel Type: {vehicle.fuel_type}</p>
        <p className="text-gray-400 mb-1">Body Type: {vehicle.body_type}</p>
        <p className="text-gray-400 mb-1">Year: {vehicle.year}</p>
        <p className="text-gray-400">Transmission: {vehicle.transmission}</p>
      </section>

      {/* Updated Purchase Section */}
      <section className="bg-gray-800 p-6 rounded-md shadow-md">
        <h4 className="text-xl font-semibold mb-4">Complete Your Purchase</h4>

        <div className="space-y-4">
          <div>
            <label className="block text-gray-300 mb-2">
              Transaction Reference ID
            </label>
            <input
              type="text"
              placeholder="Enter Transaction Reference ID"
              value={transactionId}
              onChange={(e) => setTransactionId(e.target.value)}
              className="w-full p-2 rounded-md bg-gray-900 text-white"
              required
            />
          </div>

          <div>
            <label className="block text-gray-300 mb-2">Transaction Date</label>
            <input
              type="date"
              value={transactionDate}
              onChange={(e) => setTransactionDate(e.target.value)}
              className="w-full p-2 rounded-md bg-gray-900 text-white"
              required
            />
          </div>

          <div>
            <label className="block text-gray-300 mb-2">
              Transaction Ammount (₹)
            </label>
            <input
              type="number"
              value={transactionPrice}
              onChange={(e) => setTransactionPrice(e.target.value)}
              className="w-full p-2 rounded-md bg-gray-900 text-white"
              min="0"
              step="0.01"
              required
            />
          </div>

          <div>
            <label className="block text-gray-300 mb-2">Payment Method</label>
            <select
              value={transactionMethod}
              onChange={(e) => setTransactionMethod(e.target.value)}
              className="w-full p-2 rounded-md bg-gray-900 text-white"
              required
            >
              <option value="">Select payment method</option>
              <option value="credit_card">Credit Card</option>
              <option value="debit_card">Debit Card</option>
              <option value="bank_transfer">Bank Transfer</option>
              <option value="cash">Cash</option>
            </select>
          </div>

          <button
            onClick={handlePurchase}
            disabled={isPurchasing}
            className="bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded-md w-full mt-4"
          >
            {isPurchasing ? "Processing..." : "Confirm Purchase"}
          </button>

          {purchaseStatus && (
            <p className="text-center mt-4">{purchaseStatus}</p>
          )}
        </div>
      </section>
    </div>
  );
}

export default Page6;
