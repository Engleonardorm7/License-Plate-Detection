import React, { useState } from "react";
import EntryScreen from "./components/EntryScreen";
import PaymentScreen from "./components/paymentScreen";
import axios from "axios";

const App = () => {
  const [plateNumber, setPlateNumber] = useState("");
  const [vehicleData, setVehicleData] = useState(null);
  const [isPaymentScreen, setIsPaymentScreen] = useState(false);

  const handlePlateSubmit = async (plate) => {
    try {
      const response = await axios.get(
        `http://127.0.0.1:5000/api/vehicle/${plate}`
      );
      setPlateNumber(plate);
      setVehicleData(response.data);
      setIsPaymentScreen(true);
    } catch (error) {
      console.error(
        "Error: ",
        error.response ? error.response.data : error.message
      );
      alert("Vehicle not found.");
    }
  };

  const handlePaymentComplete = () => {
    setPlateNumber("");
    setVehicleData(null);
    setIsPaymentScreen(false);
  };

  return (
    <div className="app">
      {isPaymentScreen ? (
        <PaymentScreen
          plateNumber={plateNumber}
          vehicleData={vehicleData}
          onPaymentComplete={handlePaymentComplete}
        />
      ) : (
        <EntryScreen onSubmitPlate={handlePlateSubmit} />
      )}
    </div>
  );
};

export default App;
