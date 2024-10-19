import React, { useState } from "react";

const EntryScreen = ({ onSubmitPlate }) => {
  const [plateNumber, setPlateNumber] = useState("");

  const handleInputChange = (event) => {
    setPlateNumber(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (plateNumber.trim() === "") {
      alert("enter your license plate");
      return;
    }

    onSubmitPlate(plateNumber);
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
          placeholder="Ej: SN66 CMZ"
        />
        <button onClick={handleSubmit}>Enter</button>
      </div>
    </div>
  );
};

export default EntryScreen;
