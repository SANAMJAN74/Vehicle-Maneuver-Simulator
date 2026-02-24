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
  
  ``` pip install pygame,numpy```
- Place images in the same directory as the script or update paths accordingly.
