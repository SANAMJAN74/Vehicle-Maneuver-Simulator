# Optimality Analysis of Ahead Vehicle Maneuver in Front of Emergency Vehicle

This repository contains the code and documentation for my Master's thesis project on analyzing optimal maneuvers of vehicles ahead of an emergency vehicle. The project involves simulating traffic scenarios using Pygame, generating datasets for training machine learning models, and analyzing vehicle behaviors for safety and efficiency.
The simulation models an ego vehicle (controlled by the user) interacting with other vehicles, including an ambulance, in a multi-lane road environment. Data is collected on positions, velocities, and accelerations to create datasets for further analysis or ML training.

## Repository Structure

- ```simulator/:``` Contains the simulation scripts (e.g., one_vehicle_control.py).

- ```data/:``` Generated datasets (e.g., CSV files like Right for longitudinal/lateral distances, velocities, etc.).

- ```Image/:``` Image for the simulation (e.g., car.png, amu.png, car1.png, etc.).

- ```thesis/:``` PDF of the full thesis (Master_Thesis-1.pdf).

- ```README.md:``` This file.

## Prerequisites

- Python 3.8+
- Required libraries: pygame, numpy. Install via:


## Dataset Generation
The first step in the project is generating a dataset using the simulation. The script ```one_vehicle_control.py``` runs a Pygame-based traffic simulation where:

* The ego vehicle can be controlled using arrow keys (UP/DOWN for acceleration/braking, LEFT/RIGHT for steering).
  
* Other vehicles (including the ambulance) move at constant velocities.
  
* Data is logged to a file (Right) including:
  - Longitudinal and lateral distances between the ambulance and ego vehicle.
  - Ego vehicle velocity and acceleration.

The simulation ends on collision or when the ambulance reaches the end of the screen.
Run the script multiple times to generate varied data (due to random initial positions).

How to Run

Navigate to the simulator/ directory.
Run the script:textpython one_vehicle_control.py
Control the ego vehicle with arrow keys.
Data is appended to /home/m/Paper/Code/Simulator/Right (update the path as needed for your environment).
To generate a full dataset, run the simulation repeatedly (e.g., in a loop or manually) and process the output file into a clean CSV.

Example Output Data Format
The output file (Right) is a CSV-like text file with columns:

Longitudinal distance (ambulance - ego)
Lateral distance (ambulance - ego)
Ego longitudinal velocity
Ego acceleration

Sample row: 10.5,1.2,8.31,0.5
Notes on Dataset

Data is generated in real-time based on simulation physics (kinematic bicycle model for ego vehicle).
Randomness is introduced in ego initial position for variability.
For ML training, preprocess the data (e.g., normalize, label optimal maneuvers based on thesis criteria).
In the thesis (page 20-35), this dataset is used to train models for predicting optimal lane changes or speed adjustments.

Next Steps

Clean and preprocess the generated data (e.g., using Pandas).
Train ML models (e.g., decision trees or neural networks) as described in the thesis.
For full details, refer to the thesis PDF.

License
MIT License - Feel free to use and modify for educational purposes.


  
  ``` pip install pygame,numpy```
- Place images in the same directory as the script or update paths accordingly.
