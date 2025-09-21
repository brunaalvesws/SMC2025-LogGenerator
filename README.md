# SMC2025-LogGenerator
Multi-perspective log generator presented on SMC 2025

To access online, go to https://smc2025-log-generator.vercel.app/generate

## File Templates

To generate logs, you will need three models: **Process Model**, **Data Access Model**, and **Organizational Model**. Templates for these models are available in the `Examples` directory of this repository.

---

### Process Model (DECLARE)

The DECLARE template is composed of activities and rules.

* To add more activities, include new lines at the beginning with the keyword `activity` followed by the activity name.
* To add rules, write the rule name and the activities affected by it, followed by optional activation parameters.

> Note: Some DECLARE rules may not yet be supported.

---

### Data Access Model

* The **first column** of this template contains the data objects that can be accessed. Please keep the column title as **`Data Objects`** when customizing your own.
* The **other columns** define the permitted operations of each activity on the data objects listed in the first column.

Use the following notation:

* Place the **activity name** at the top of the column.
* List the permitted operations separated by commas for each data object:

  * `c` = create
  * `u` = update
  * `r` = read
  * `d` = delete

**Capital letters** indicate mandatory operations, **lowercase letters** indicate optional operations, and the absence of a letter indicates the operation is **forbidden**.

---

### Organizational Model

In this template, do not change the column headers, since they match the log column names for easier processing.

* The **first column** refers to the case name. Add a profile and resources to each case, following the pattern `case_{number}` starting from `case_0`. Remember to verify the number of cases you want to generate.
* The **second column** specifies the profile name.
* The **third column** lists the resources for this profile, separated by commas.


All activity names, resources, profiles, and data objects can be customized. The generator will issue warnings if something is not valid.


---

# 🚀 Running Locally

Follow these steps to run the project locally.

## 🔧 Prerequisites

Make sure you have the following installed:

* Python (3.8 or newer)
* Node.js (14.x or newer) + npm or yarn
* Angular CLI
* Git

---

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
