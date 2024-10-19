import React, { useState } from "react";
import axios from "axios";

const PaymentScreen = ({ plateNumber, vehicleData, onPaymentComplete }) => {
  const [loading, setLoading] = useState(false);

  const handlePayment = async () => {
    try {
      setLoading(true);
      const endTime = new Date().toISOString();
      const response = await axios.post(
        `http://127.0.0.1:5000/api/vehicle/${plateNumber}/exit`,
        {
          end_time: endTime,
        }
      );
      console.log("Total time:", response.data.total_time);
      console.log("Total cost", response.data.total_cost);
      alert(`El costo total es: ${response.data.total_cost}`);
      onPaymentComplete();
    } catch (error) {
      console.error(
        "Error: ",
        error.response ? error.response.data : error.message
      );
      alert("Failed Payment");
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className="payment-screen">
      <h2>Detalles del Vehículo</h2>
      <div>
        <img src={vehicleData.image} alt="Vehicle" />
        <p>Placa: {plateNumber}</p>
        <p>Hora de entrada: {vehicleData.entry_time}</p>
      </div>
      <div>
        <button onClick={handlePayment} disabled={loading}>
          {loading ? "Procesando..." : "Pagar"}
        </button>
        <button onClick={onPaymentComplete}>Cancelar</button>
      </div>
    </div>
  );
};

export default PaymentScreen;
