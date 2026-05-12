# Injury Risk Analysis in the NFL

## Overview
This project builds an interactive Streamlit app that analyzes NFL tracking data to identify high-intensity movement situations. The app uses speed, acceleration, and movement intensity as a proxy for potential injury-risk conditions.

## Research Question
How can NFL player movement data be used to identify high-intensity movement situations associated with elevated injury-risk conditions?

## Features
- Interactive filters for speed, acceleration, and risk category
- Speed category analysis
- Acceleration category analysis
- Speed vs acceleration visualization
- Movement intensity risk categories
- Interactive risk estimator

## Dataset
The app uses NFL Big Data Bowl tracking data. A sample of the tracking data is stored in the `data` folder.

## Methodology
1. Remove football tracking rows
2. Convert speed from yards/second to miles/hour
3. Categorize speed and acceleration
4. Create movement intensity as speed × acceleration
5. Define risk categories using percentile thresholds

## Important Limitation
This app does not predict confirmed injuries because direct injury labels are not included. Movement intensity is used as a proxy for potential risk.

## Installation
```bash
pip install -r requirements.txt
