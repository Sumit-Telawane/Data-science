
Weather Data Aggregator and Analyzer
====================================

Description
-----------
This project fetches weather data from the OpenWeatherMap API, stores it in a local SQLite database, and provides analysis and visualization of weather trends over time using Jupyter Notebook.

Requirements
------------
- Python 3.x
- Jupyter Notebook
- Required Python packages: `requests`, `schedule`, `sqlite3`, `pandas`, `matplotlib`, `seaborn`

Setup Instructions
------------------

1. Clone the Repository
   --------------------
   Clone the repository from GitHub and navigate to the project directory.
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install Required Packages
   -------------------------
   Install the required Python packages using `pip`.
   ```bash
   pip install requests schedule pandas matplotlib seaborn opencage folium
   ```

3. Set Up the Jupyter Notebook Environment
   ----------------------------------------
   Ensure Jupyter Notebook is installed on your system. If not, install it using `pip`.
   ```bash
   pip install notebook
   ```

4. Start Jupyter Notebook
   -----------------------
   Start Jupyter Notebook from the project directory.
   ```bash
   jupyter notebook
   ```

5. Open the Notebooks
   -------------------
   - Open `weather_records.ipynb` to fetch and store weather data.
   - Open `weather_analysis.ipynb` to analyze and visualize the weather data.

Fetch and Store Weather Data
----------------------------
1. `weather_records.ipynb`
   - This notebook is responsible for fetching weather data from the OpenWeatherMap API and storing it in a SQLite database.
   - Ensure you have a valid API key from OpenWeatherMap and replace `'ea642ff5d0165717d77c25f8bdb605da'` with your API key.
   - Run the notebook cells to create the database, fetch data, and store it in the database.
   
   Key sections in `weather_records.ipynb`:
   - Import necessary libraries.
   - Create the SQLite database and table.
   - Define functions to fetch and store weather data.
   - Schedule the data fetching process.

Analyze and Visualize Weather Data
----------------------------------
2. `weather_analysis.ipynb`
   - This notebook provides analysis and visualization of the stored weather data.
   - Run the notebook cells to load the data from the SQLite database, perform statistical analysis, and generate visualizations.
   
   Key sections in `weather_analysis.ipynb`:
   - Import necessary libraries.
   - Fetch weather data from the SQLite database.
   - Calculate basic statistics.
   - Filter data by date range.
   - Visualize temperature and humidity trends.

Example Outputs
---------------
Temperature Trends
![Temperature Trends](example_temperature_trends.png)

Humidity Trends
![Humidity Trends](example_humidity_trends.png)

Statistics
----------
- Average Temperature: ...
- Average Humidity: ...
- Average Wind Speed: ...

Conclusion
----------
By following the above steps, you will be able to set up the environment, fetch and store weather data, and perform analysis and visualization using Jupyter Notebook.

Author
------
Sumit Telawane
