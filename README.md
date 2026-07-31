# CSV Cleaning Agent

This project is an AI-assisted CSV cleaning application that allows users to upload a CSV file, view dataset information, clean the data using natural-language instructions, and download the cleaned result.

The application uses a locally trained TF-IDF text classifier to predict supported cleaning actions. The trained model is included with the project, so retraining is not required to run the application.

## Features

- Upload CSV files
- View rows, columns, missing values, and duplicate rows
- Preview the dataset
- View the full dataset with pagination
- Clean data using natural-language instructions
- Use supported action shortcuts in the AI Cleaning Assistant
- View the latest cleaning result and model confidence
- Download the cleaned CSV file

## Supported Cleaning Actions

- Remove duplicate rows
- Remove rows with missing values
- Fill missing values with the mean
- Fill missing values with the median
- Drop a column
- Rename a column

## Installation & Setup

Before running the project, make sure you have Python 3.x, Node.js, and npm installed.

### 1. Clone the Repository

```bash
git clone https://github.com/Juan-jjv/csv-cleaning-agent.git
cd csv-cleaning-agent
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

## Run the Application

The easiest way to start both the backend and frontend is:

```bash
./run.sh
```

If needed, make the script executable first:

```bash
chmod +x run.sh
```

Then open:

```text
http://localhost:5173
```

The backend runs at:

```text
http://localhost:8000
```

FastAPI documentation is available at:

```text
http://localhost:8000/docs
```

## Run Manually

Backend:

```bash
source .venv/bin/activate
fastapi dev backend/main.py
```

Frontend:

```bash
cd frontend
npm run dev
```

## Running Tests

From the project root:

```bash
pytest
```

## Retraining the Model

The trained model is already included in the project.

Retraining is only required if the training data or model configuration is changed.

```bash
python model/generate_training_data.py
python model/train.py
```

## Main Technologies

- Python
- pandas
- scikit-learn
- FastAPI
- React
- Vite
- pytest
