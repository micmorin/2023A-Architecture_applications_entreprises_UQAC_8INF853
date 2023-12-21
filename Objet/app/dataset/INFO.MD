CASAS
_______________________________________________________
WSU Smart Apartment 2010-2012 Two Resident Testbed

Description

This dataset represents sensor events collected in the WSU smart apartment
testbed from 2010 to 2012.  The apartment housed two residents
at this time and they performed their normal daily activities.

Although the same two residents lived in the apartment during this time,
on weekdays between 9am and 5pm occasionally the residents left the apartment
while experiments and participants were in the apartment conducting focused
experiments.

File format

The text file, called "data", is included in this release.  The file contains
sensor events that were generated in the testbed. No activities are annotated
in this dataset.

Sensor layouts

The sensors can be categorized by:

   Mxxx:      motion sensor
   MAxxx:     motion area sensor (covers a larger region)
   Ixxx:      item sensor for selected items in the kitchen
   Dxxx:      door sensor
   AD1-A:     burner sensor
   AD1-B:     hot water sensor
   AD1-C:     cold water sensor
   Txxx:      temperature sensors
   P001:      electricity usage
   BAxxxxx:   battery level
   LLxxx:     light level
   SSxxx:     shake sensor
   LSxxx:     light sensor
   SGxxx:     gyro sensor
   Exxx:      experimenter switch (manual trigger)
   Fxxx:      fan

The sensor layout of the apartment for the data set is shown in the file
sensorlayout.jpg.  The sensors are the same but some renumbering was done
and power usage was added.

All use of the data must cite the WSU CASAS smart home project.

D. Cook, A. Crandall, B. Thomas, and N. Krishnan.
CASAS: A smart home in a box. IEEE Computer, 46(7):62-69, 2013.

NURSE
_______________________________________________________
About Dataset
Dataset for Continuous Stress Monitoring of Hospital Nurses

The growing accessibility of wearable tech has opened doors to continuously monitor various physiological factors. Detecting stress early has become pivotal, aiding individuals in proactively managing their health against the detrimental effects of prolonged stress exposure. This paper presents an exclusive stress detection dataset cultivated within the natural environment of a hospital. Compiled during the COVID-19 outbreak, this dataset encompasses the biometric data of nurses. Analyzing stress in a workplace setting is intricate due to the multifaceted social, cultural, and psychological elements inherent in dealing with stressful circumstances. Hence, our dataset not only encompasses physiological data but also contextual information surrounding stress events. Key physiological metrics such as electrodermal activity, heart rate, and skin temperature of the nurse subjects were continuously monitored. Additionally, a periodic survey administered via smartphones captured contributing factors linked to detected stress events. The database housing these signals, stress occurrences, and survey responses is publicly accessible on Dryad.

Project Overview
This project delves into leveraging wearable device-derived physiological signals to gauge stress levels among nurses operating within a hospital environment. The dataset comprises details acquired from nurses wearing watches that tracked their heart rate, skin temperature, and electrodermal activity (EDA) while simultaneously reporting their stress levels.

The primary goal revolves around evaluating various machine learning models to forecast stress levels based on recorded physiological signals. Additionally, the project investigates the most pertinent physiological indicators for stress detection and offers insights to enhance the accuracy and dependability of stress detection via wearable tech.

Dataset Description:

Data Collection Context:
Period: Data gathered over one week from 15 female nurses aged 30 to 55 years, during regular shifts at a hospital.
Collection Phases: Two phases - Phase-I (April 15, 2020, to August 6, 2020) and Phase-II (October 8, 2020, to December 11, 2020).
Exclusion Criteria: Pregnancy, heavy smoking, mental disorders, chronic or cardiovascular diseases.

Data Captured:
Physiological Variables Monitored: Electrodermal activity, Heart Rate, and skin temperature of the nurse subjects.
Survey Responses: Periodic smartphone-administered surveys capturing contributing factors to detected stress events.
Measurement Technologies: Utilized Empatica E4 for data collection, specifically focusing on Galvanic Skin Response and Blood Volume Pulse (BVP) readings.

Study Procedure:
Approval: University's Institutional Review Board approved the study protocol (FA19–50 INFOR).
Consent and Enrollment: Nurse subjects were enrolled after expressing interest and obtaining hospital compliance.
Study Design: Conducted in three phases, each including 7 nurses. No incentives were provided, and anonymization of data was ensured.

Data Availability:
Public Release: A database containing signals, stress events, and survey responses is publicly available on Dryad.
Anonymization: Unique identifiers assigned to subjects to maintain anonymity.

Merge CSV File Information:
This dataset comprises approximately 11.5 million entries across nine columns:
X, Y, Z: Orientation data (256 unique entries each).
EDA, HR, TEMP: Physiological measurements (EDA: 274,452 unique, HR: 6,268 unique, TEMP: 599 unique).
id: 18 categorical identifiers.
datetime: Extensive date and time entries (10.6 million unique).
label: Categorical states or classes (three unique entries).
The dataset offers a wide array of continuous physiological measurements alongside orientation data, facilitating stress detection, health monitoring, and related research endeavours.

Requirements
Python 3.7 or higher and Jupyter Notebook are prerequisites. The necessary Python packages are enumerated in the requirements.txt file. To execute the code, installation of the following libraries is mandatory: pandas, numpy, sci-kit-learn, and matplotlib.

AIR
_______________________________________________________
About Dataset
Context
This dataset contains the responses of a gas multisensor device deployed on the field in an Italian city. Hourly responses averages are recorded along with gas concentrations references from a certified analyzer. This dataset was taken from UCI Machine Learning Repository: https://archive.ics.uci.edu/ml/index.php

Content
The dataset contains 9357 instances of hourly averaged responses from an array of 5 metal oxide chemical sensors embedded in an Air Quality Chemical Multisensor Device. The device was located on the field in a significantly polluted area, at road level,within an Italian city. Data were recorded from March 2004 to February 2005 (one year) representing the longest freely available recordings of on field deployed air quality chemical sensor devices responses. Ground Truth hourly averaged concentrations for CO, Non Metanic Hydrocarbons, Benzene, Total Nitrogen Oxides (NOx) and Nitrogen Dioxide (NO2) and were provided by a co-located reference certified analyzer. Evidences of cross-sensitivities as well as both concept and sensor drifts are present as described in De Vito et al., Sens. And Act. B, Vol. 129,2,2008 (citation required) eventually affecting sensors concentration estimation capabilities. Missing values are tagged with -200 value.
This dataset can be used exclusively for research purposes. Commercial purposes are fully excluded.

Attribute Information
0 Date (DD/MM/YYYY)
1 Time (HH.MM.SS)
2 True hourly averaged concentration CO in mg/m^3 (reference analyzer)
3 PT08.S1 (tin oxide) hourly averaged sensor response (nominally CO targeted)
4 True hourly averaged overall Non Metanic HydroCarbons concentration in microg/m^3 (reference analyzer)
5 True hourly averaged Benzene concentration in microg/m^3 (reference analyzer)
6 PT08.S2 (titania) hourly averaged sensor response (nominally NMHC targeted)
7 True hourly averaged NOx concentration in ppb (reference analyzer)
8 PT08.S3 (tungsten oxide) hourly averaged sensor response (nominally NOx targeted)
9 True hourly averaged NO2 concentration in microg/m^3 (reference analyzer)
10 PT08.S4 (tungsten oxide) hourly averaged sensor response (nominally NO2 targeted)
11 PT08.S5 (indium oxide) hourly averaged sensor response (nominally O3 targeted)
12 Temperature in Â°C
13 Relative Humidity (%)
14 AH Absolute Humidity

Acknowledgements
Saverio De Vito (saverio.devito '@' enea.it), ENEA - National Agency for New Technologies, Energy and Sustainable Economic Development

Citation Request
S. De Vito, E. Massera, M. Piga, L. Martinotto, G. Di Francia, On field calibration of an electronic nose for benzene estimation in an urban pollution monitoring scenario, Sensors and Actuators B: Chemical, Volume 129, Issue 2, 22 February 2008, Pages 750-757, ISSN 0925-4005.
(https://www.sciencedirect.com/science/article/abs/pii/S0925400507007691)

AIR POLUTION 
_______________________________________________________

The dataset is taken from https://app.cpcbccr.com/.

It includes data for Air Pollution in Delhi from 2011 to 2021 (latest)

IOT Telemetry
_______________________________________________________

About Dataset
Context
Environmental sensor telemetry data, detailed in the blog post, Getting Started with IoT Analytics on AWS, published on Towards Data Science.

Content
The data was generated from a series of three identical, custom-built, breadboard-based sensor arrays. Each array was connected to a Raspberry Pi devices. Each of the three IoT devices was placed in a physical location with varied environmental conditions.

| device            | environmental conditions                 |
|-------------------|------------------------------------------|
| 00:0f:00:70:91:0a | stable conditions, cooler and more humid |
| 1c:bf:ce:15:ec:4d | highly variable temperature and humidity |
| b8:27:eb:bf:9d:51 | stable conditions, warmer and dryer      |
Each IoT device collected a total of seven different readings from the four sensors on a regular interval. Sensor readings include temperature, humidity, carbon monoxide (CO), liquid petroleum gas (LPG), smoke, light, and motion. The data spans the period from 07/12/2020 00:00:00 UTC – 07/19/2020 23:59:59 UTC. There is a total of 405,184 rows of data.

The sensor readings, along with a unique device ID and timestamp, were published as a single message, using the ISO standard Message Queuing Telemetry Transport (MQTT) network protocol. Below is an example of an MQTT message payload.

{
  "data": {
    "co": 0.006104480269226063,
    "humidity": 55.099998474121094,
    "light": true,
    "lpg": 0.008895956948783413,
    "motion": false,
    "smoke": 0.023978358312270912,
    "temp": 31.799999237060547
  },
  "device_id": "6e:81:c9:d4:9e:58",
  "ts": 1594419195.292461
}
Columns
There are nine columns in the dataset.

| column   | description          | units      |
|----------|----------------------|------------|
| ts       | timestamp of event   | epoch      |
| device   | unique device name   | string     |
| co       | carbon monoxide      | ppm (%)    |
| humidity | humidity             | percentage |
| light    | light detected?      | boolean    |
| lpg      | liquid petroleum gas | ppm (%)    |
| motion   | motion detected?     | boolean    |
| smoke    | smoke                | ppm (%)    |
| temp     | temperature          | Fahrenheit |