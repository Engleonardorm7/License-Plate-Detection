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
      // get details
      console.log(plate);
      const vehicleResponse = await axios.get(
        `http://127.0.0.1:5000/api/vehicle/${plate}`
      );
      // update exit time and get the cost
      const exitResponse = await axios.post(
        `http://127.0.0.1:5000/api/vehicle/${plate}/exit`,
        {}
      );

      const updatedVehicleData = {
        ...vehicleResponse.data,
        total_cost: exitResponse.data.total_cost,
        total_time: exitResponse.data.total_time,
        end_time: exitResponse.data.end_time,
      };

      setPlateNumber(plate);
      setVehicleData(updatedVehicleData);
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
