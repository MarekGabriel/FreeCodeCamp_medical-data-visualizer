# Medical Data Visualizer

This project is part of the ***Data Analysis with Python*** certification from freeCodeCamp.

## Project Description

The goal of this project is to analyze a dataset of medical examination records and visualize relationships between various health indicators.

The analysis includes:

* Calculating and normalizing BMI-related data
* Cleaning the dataset by removing incorrect or extreme values
* Converting data into appropriate formats for visualization
* Creating plots to identify patterns, like categorical plot that:
    * Displays value counts of selected health-related variables
    * Compares distributions between people with and without cardiovascular disease
    * Built using Seaborn's `catplot()`
* also heatmap that:
    * Shows the correlation matrix between numerical variables
    * Helps identify relationships between health indicators
    * Built using Seaborn's `heatmap()`

## Technologies Used

* Python
* Pandas
* NumPy
* Seaborn
* Matplotlib

## Dataset

https://raw.githubusercontent.com/freeCodeCamp/boilerplate-medical-data-visualizer/refs/heads/main/medical_examination.csv

It contains anonymized medical examination data, including:

* Age, height, weight
* Blood pressure (systolic and diastolic)
* Cholesterol and glucose levels
* Lifestyle indicators (smoking, alcohol intake, physical activity)
* Presence or absence of cardiovascular disease

## How to Run

1. Clone the repository:
   git clone https://github.com/MarekGabriel/FreeCodeCamp_medical-data-visualizer.git

2. Navigate to the project folder:
   cd FreeCodeCamp_medical-data-visualizer

3. Run the script:
   medical_data_visualizer.py

## Example Usage

Input:

no input needed (when running medical_data_visualizer.py it imports proper data from .csv)

Output:

To be reached when calling both functions implemented:
* `medical_data_visualizer.draw_cat_plot()`
* `medical_data_visualizer.draw_heat_map()`

![plots](/catplot_heatmap.png)

## Project Structure

* medical_data_visualizer.py — main functions: `draw_cat_plot()` & `draw_heat_map()` implementation
* main.py — An entrypoint file to be used in development. It imports main functions implemented and runs unit tests automatically.
* test_module.py — unit tests provided by freeCodeCamp

## License

This project is licensed under the MIT License.
