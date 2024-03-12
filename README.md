# Eco-Scheduler for Kubernetes

## Overview

This project, developed as a final year project at ENSEEIHT, introduces an eco-friendly scheduler for Kubernetes named Eco Scheduler. The goal of Eco Scheduler is to enhance Kubernetes' scheduling process by prioritizing energy efficiency without compromising performance. This is achieved through monitoring and analyzing energy consumption data of Kubernetes pods, and making informed scheduling decisions to minimize the overall energy footprint.

## Installation

Before you can utilize Eco Scheduler, you must ensure your Kubernetes environment is set up correctly. The project includes several scripts to help with this:

- `start_minikube.sh`: Starts a Minikube cluster.
- `stop_minikube.sh`: Stops the Minikube cluster.
- `install_package.sh`: Installs required packages (Prometheus + Grafana + kepler)
- `destroy_minikube.sh`: Completely removes the Minikube cluster.

Make sure to execute these scripts in your terminal according to your setup needs.

## Usage

### Data Collection

`keplerData.py` is a crucial component of the project. It lists all pods starting with "kepler-", collects their energy consumption metrics from a specified port (default is 9102), and filters the data to focus on energy usage.

### Scheduling

`my-scheduler-python.py` implements the scheduling logic based on the collected data. It interfaces with Kubernetes to make scheduling decisions that optimize for energy efficiency.

### Visualization

`visualizeKepler.py` provides a visual representation of the energy consumption data, aiding in the analysis and understanding of the energy usage patterns of the scheduled pods.

### Testing

`test-pods.yaml` includes definitions for test pods. You can use this file to deploy sample pods to your cluster and observe the Eco Scheduler in action.
