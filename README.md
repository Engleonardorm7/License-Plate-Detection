# License Plate Detection Project

This is a full-stack project for managing vehicle entries and exits with license plate detection. The project includes a backend implemented with Flask (Python) and a frontend built with React.

## Project Structure

```
tu_proyecto/
├── backend/
│   ├── app/
│   ├── database.db
│   ├── vehicle.py
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── README.md
└── README.md
```

## Prerequisites

- Python 3.8+
- Node.js and npm

## Getting Started

Follow the steps below to install and run the project locally.

### 1. Clone the Repository

```bash
git clone https://gitlab.hof-university.de/leonardo/license-plate-detection-project.git
cd license-plate-detection-project
```

### 2. Setting Up the Backend

1. Navigate to the backend directory:

   ```bash
   cd project_backend
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate     # For Windows
   ```

3. Install the required Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the backend server:

   ```bash
   python main.py
   ```

   The backend server will start on `http://localhost:5000`.

### 3. Setting Up the Frontend

1. Navigate to the frontend directory:

   ```bash
   cd ../frontend
   ```

2. Install the Node.js dependencies:

   ```bash
   npm install
   ```

3. Run the frontend development server:

   ```bash
   npm start
   ```

   The frontend will start on `http://localhost:3000`.

### 4. Accessing the Application

- Open your browser and go to `http://localhost:3000` to view the frontend.
- The backend API will be available at `http://localhost:5000/api`.

## Available Scripts (Frontend)

In the frontend directory, you can run:

- **`npm start`**: Runs the app in development mode.
- **`npm build`**: Builds the app for production.
- **`npm test`**: Launches the test runner.

## Backend API Endpoints

| Method | Endpoint                     | Description                          |
| ------ | ---------------------------- | ------------------------------------ |
| POST   | `/api/vehicle/<plate>/entry` | Register a vehicle entry             |
| POST   | `/api/vehicle/<plate>/exit`  | Process vehicle exit and delete data |

## Contributing

Feel free to fork this repository and submit pull requests. Any contribution is highly appreciated.
