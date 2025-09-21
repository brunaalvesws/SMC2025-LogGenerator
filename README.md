# SMC2025-LogGenerator
Multi-perspective log generator presented on SMC 2025

To access online, go to https://smc2025-log-generator.vercel.app/generate

## Files templates

To generate some logs, you will need the specified models: Process model, Data Access Model and Organizational Model. The templates for this models are available in the directory "Examples" of this repository. 

# Declare Process Model
The DECLARE template is composed by activities and rules. You can add more activities adding lines in the begining with 'activity' before the activity name. You can add rules adding the Rule name and the activities affected by it followed by optional activation parameters. Some DECLARE rules may not be supported yet.

# Data Access Model
The first column of this template contains the Data Objects that can be accessed, please, keep the column title 'Data Objects' when customizing your own. The other columns are the activities permited operations to each data object of the first column. Put the activity name in the begining of the column and its permited operations separated by comma, the available operations are c (create), u (update), r (read) and d (delete). Capital letters indicate mandatory operations, small letters indicate optional operation and the absense of the letter indicates the operation is forbidden.

# Organizational Model
In this template, please do not change the column header, it has the same name of the log columns to make it easier. The first column refers to the case name, so you need to add an profile and resources to each case. Follow the pattern 'case_{number of the case}' starting by 0. Then, in the second column, add a profile name and in the third column, add a resource list for this profile separated by comma.

All the activity names, resources, profiles and data objects can be customized. The generator will warn you if something is not right.

---

# Running Locally:

## 🔧 Prerequisites

Make sure you have the following installed:

* Python (3.8 or newer)
* Node.js (14.x or newer) + npm or yarn
* Angular CLI
* Git

---

## 🚀 Running Locally

Follow these steps to run the project locally.

### 1. Clone the repository

```bash
git clone https://github.com/brunaalvesws/SMC2025-LogGenerator.git
cd SMC2025-LogGenerator
```

### 2. Setup backend (Flask)

1. **Go to the backend directory**

   ```bash
   cd log-generator
   ```

2. **Create a virtual environment**

   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment**

   * On macOS / Linux:

     ```bash
     source venv/bin/activate
     ```
   * On Windows (PowerShell):

     ```powershell
     .\venv\Scripts\Activate
     ```

4. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Set environment variables** (if needed)

   ```bash
   export FLASK_APP=app.py
   export FLASK_ENV=development
   ```


6. **Run the backend server**

   ```bash
   flask run
   ```

   or

   ```bash
   python app.py
   ```

   The backend should now be running on `http://127.0.0.1:5000`.

*(It is also possible to run the app.py file without the virtual environment, just using the last step)*

### 3. Setup frontend (Angular)

1. **Go to frontend directory**

   ```bash
   cd ../log-generator-web
   ```

2. **Install dependencies**

   ```bash
   npm install
   ```

   or

   ```bash
   yarn install
   ```

3. **Configure API base URL, if needed**
   Update the API URL in `src/environments/environment.ts` (or similar) to point to the backend, e.g. `http://localhost:5000/api`.

4. **Serve the frontend in dev mode**

   ```bash
   ng serve
   ```

   or

   ```bash
   npm start
   ```

   The frontend will be available at `http://localhost:4200`.

### 4. Run both together

* Flask backend: `http://localhost:5000`
* Angular frontend: `http://localhost:4200`

Open the frontend in your browser and interact with the app.

---

## ⚙️ Troubleshooting

* **CORS errors** → Ensure `flask-cors` is installed and enabled.
* **Port conflicts** → Change the ports if 5000 or 4200 are already in use.

---

## ✅ Quick Start Summary

```bash
git clone https://github.com/brunaalvesws/SMC2025-LogGenerator.git
cd SMC2025-LogGenerator

# Backend setup
cd log-generator
python3 -m venv venv
source venv/bin/activate     # Windows: .\venv\Scripts\Activate
pip install -r requirements.txt
export FLASK_APP=app.py
export FLASK_ENV=development
flask run

# Frontend setup
cd ../log-generator-web
npm install
ng serve
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
