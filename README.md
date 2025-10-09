# Taxi prediction lab

This is a school project which aims to predict the fare amount of a taxi ride based on various features such as trip distance, base fare, time of day and day of week. It includes data cleaning, exploratory analysis, simple feature engineering and a small FastAPI + Streamlit demo.

> **Note:** This project use Google Maps API for geocoding and distance calculations. Make sure to set up your Google Maps API key in the `.env` file as described below.

---

## Requirements

- **Python 3.11+**
- **`uv`** command-line utility (Optional, but used for fast dependency management)
- **Google Maps API key** (with Geocoding API & Distance Matrix API enabled)

---

## Project Setup

Follow these steps to get the environment ready and install dependencies.

### 1. Clone the repository

    Open a terminal and run:
    ```bash
    git clone https://github.com/Sandstrom96/taxi_prediction_fullstack_andreas_s_opa24.git
    cd taxi_prediction_fullstack_andreas_s_opa24
    ```

### 2. Create and activate a virtual environment

Use `uv` to create the environment and activate it.

    | Operating System | Commands |
    | :--- | :--- |
    | **Windows** (Powershell) | 
    ```bash
    uv env venv 
    venv\Scripts\activate 
    ``` |
    | **macOS/Linux** | 
    ```bash
    uv env venv
    source venv/bin/activate
    ``` |

### 3. Install the required packages

With the virtual environment activated, install all project dependencies:
    ```bash
    uv pip install -e .
    ```

---

## Google Maps API Key Setup

### 1. Configure Google Maps API key

    - Go to the [Google Cloud Console](https://console.cloud.google.com/).
    - Create a new project or select an existing one.
    - Navigate to the "APIs & Services" > "Credentials" section.
    - Click on "Create Credentials" and select "API Key".
    - Navigate to "Library" and enable the following APIs:
        - Geocoding API
        - Distance Matrix API
    - Restrict the API key to the necessary APIs (e.g., Geocoding API, Distance Matrix API) for security purposes.

### 2. Configure Enviroment File

    - Create a `.env` file in the root directory and add the following line:
    ```env
    GOOGLE_MAPS_API_KEY="your_google_maps_api_key_here"
    ```
    Replace `your_google_maps_api_key_here` with your actual Google Maps API key.

---

## Run application

The application requires the backend and frontend to run in **two separate terminal windows**. Ensure the virtual environment is **active** in both.

### Terminal 1: Start the FastAPI server

    Open the first terminal (with the virtual environment activated) and run:
    ```bash
    uvicorn src.taxipred.backend.api:app --reload
    ```

### Terminal 2: Start the Streamlit dashboard

    Open the second terminal (with the virtual environment activated) and launch the Streamlit app:
    ```bash
    streamlit run src/taxipred/frontend/dashboard.py
    ```
    The Streamlit application should now open automatically in your web browser (typically at `http://localhost:8501`).
