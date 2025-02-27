import React, { useState } from "react";
import axios from "axios";

const EntryScreen = ({ onSubmitPlate }) => {
  const [plateNumber, setPlateNumber] = useState("");
  const [loading, setLoading] = useState(false);
  const [loading2, setLoading2] = useState(false);

  const handleInputChange = (event) => {
    setPlateNumber(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (plateNumber.trim() === "") {
      alert("Enter your license plate");
      return;
    }

    onSubmitPlate(plateNumber);
  };

  //Function to call the input
  const handleInputVehicle = async () => {
    try {
      setLoading(true);
      const response = await axios.post("http://127.0.0.1:5000/input");
      alert(response.data.message);
    } catch (error) {
      console.error("Error registering vehicle:", error);
      if (
        error.response &&
        error.response.data &&
        error.response.data.message
      ) {
        alert(error.response.data.message);
      } else {
        alert("Unexpected error occurred while registering the vehicle.");
      }
    } finally {
      setLoading(false);
    }
  };

  //Funcion to call the output
  const handleVehicleExit = async () => {
    try {
      setLoading2(true);
      const response = await axios.post("http://127.0.0.1:5000/vehicle_exit");

      // Muestra el mensaje devuelto por el backend
      alert(response.data.message);
    } catch (error) {
      console.error("Error processing vehicle exit:", error);

      // Si el error tiene respuesta del backend, muestra el mensaje adecuado
      if (
        error.response &&
        error.response.data &&
        error.response.data.message
      ) {
        alert(error.response.data.message);
      } else {
        // Mensaje genérico para errores inesperados
        alert("Unexpected error while processing vehicle exit.");
      }
    } finally {
      setLoading2(false);
    }
  };

  return (
    <div className="entry-screen">
      <h1>Welcome</h1>
      <div>
        <label htmlFor="plate">Type your license plate:</label>
        <input
          type="text"
          id="plate"
          value={plateNumber}
          onChange={handleInputChange}
          placeholder="Ej: SN66CMZ"
        />
        <button onClick={handleSubmit}>Enter</button>
      </div>
      {/* Botton to start the entrance of the vehicle*/}
      <div class="btns">
        <div>
          <button
            class="register"
            onClick={handleInputVehicle}
            disabled={loading}
          >
            {loading ? "Processing..." : "Register"}
          </button>
        </div>

        {/* Botton to verify payment and allow the exit */}
        <div>
          <button class="exit" onClick={handleVehicleExit} disabled={loading2}>
            {loading2 ? "Processing..." : "Exit"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default EntryScreen;
