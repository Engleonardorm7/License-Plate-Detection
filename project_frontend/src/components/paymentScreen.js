const exitVehicle = async (plateNumber, endTime) => {
  try {
    const response = await axios.post(
      `http://127.0.0.1:5000/api/vehicle/${plateNumber}/exit`,
      {
        end_time: endTime,
      }
    );
    console.log("total time:", response.data.total_time);
    console.log("total cost: ", response.data.total_cost);
  } catch (error) {
    console.error(
      "Error: ",
      error.response ? error.response.data : error.message
    );
  }
};
