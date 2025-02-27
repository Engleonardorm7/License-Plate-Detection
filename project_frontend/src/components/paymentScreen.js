import React, { useState } from "react";
import axios from "axios";

const PaymentScreen = ({ plateNumber, vehicleData, onPaymentComplete }) => {
  const [loading, setLoading] = useState(false);

  const handlePayment = async (plate) => {
    try {
      setLoading(true);
      const response = await axios.post(
        `http://127.0.0.1:5000/api/vehicle/${plate}/pay`,
        {}
      );

      if (response.status === 200) {
        setTimeout(() => {
          alert("Payment completed successfully");
          onPaymentComplete();
        }, 1000);
      } else {
        alert("Payment failed. Please try again.");
      }
    } catch (error) {
      console.error(
        "Payment Error: ",
        error.response ? error.response.data : error
      );
      alert("An error occurred during the payment. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  console.log(vehicleData);
  return (
    <div className="payment-screen">
      <h2>Vehicle Details</h2>
      <div>
        <h1>{vehicleData.plate}</h1>
        <img
          src={`http://127.0.0.1:5000/images/${vehicleData.image_path}`}
          alt={`Image of ${vehicleData.plate}`}
          style={{ width: "300px", height: "auto" }}
        />

        <p>License Plate: {plateNumber}</p>
        <p>Check-in time: {vehicleData.entry_time}</p>
        <p>End time: {vehicleData.end_time}</p>
        <p>Total time: {vehicleData.total_time.toFixed(2)} hours</p>
        <p>Total to pay: {vehicleData.total_cost.toFixed(2)} EUR</p>
      </div>
      <div>
        <button
          class="pay"
          onClick={() => handlePayment(plateNumber)}
          disabled={loading}
        >
          {loading ? "Processing..." : "Pay"}
        </button>
        <button class="cancel" onClick={onPaymentComplete}>
          Cancel
        </button>
      </div>
    </div>
  );
};

export default PaymentScreen;
