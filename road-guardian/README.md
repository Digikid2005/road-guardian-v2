<<<<<<< HEAD
# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
=======
🚑 Road Guardian

AI + IoT Powered Real-Time Emergency Response System

Road Guardian is a smart accident response platform designed to reduce emergency response time and improve coordination between vehicles, hospitals, ambulances, and victims’ families.
The system detects road accidents using IoT sensors and machine learning, then instantly notifies nearby hospitals and dispatches emergency services in real time.

The platform provides a centralized dashboard for hospitals that visualizes accident locations, allows hospitals to claim incidents, and coordinates ambulance dispatch while preventing duplicate emergency responses.

🌍 Problem Statement

Road accidents often suffer from delayed emergency response and poor coordination between hospitals and rescue services. Multiple hospitals may respond to the same incident, wasting precious time and resources.

Road Guardian solves this by creating a real-time intelligent coordination system that automatically manages accident detection, hospital response, and ambulance routing.

⚙️ Core Features
🚨 Accident Detection

Accidents are detected through IoT-enabled devices mounted in vehicles that monitor:

Sudden impact

Vehicle tilt

Abnormal vibration

GPS location

Machine learning models analyze these signals to determine whether an accident has occurred.

🏥 Hospital Dashboard

Hospitals access a real-time emergency dashboard that displays incoming accident alerts.

Features include:

Live accident notifications
Victim details and vehicle information
Accident severity level
Interactive map showing accident location
Ability to claim an incident
Prevents multiple hospitals from responding to the same accident

🔒 Atomic Incident Locking
Once a hospital claims an incident:
The system locks the incident
Other hospitals immediately see it as “Locked – Handled by another hospital”
Prevents duplicate ambulance dispatch

🗺️ Live Map Visualization
The dashboard includes an interactive map interface showing:
Accident location
Nearby hospital locations
Ambulance route to the accident site
Real-time geographical context
This helps hospitals quickly assess and respond to emergencies.

🚑 Ambulance Dispatch System

After claiming an incident, hospitals can dispatch ambulances.
The system supports:
Ambulance assignment
Status updates
Emergency route tracking
Status progression includes:
Dispatched
On Scene
Patient Picked Up
Reached Hospital

👨‍👩‍👧 Family Tracking System
Road Guardian provides a tracking link for victims’ families.
Using a secure link, family members can view:
Accident status
Responding hospital
Ambulance progress
Estimated arrival time

This reduces panic and improves transparency.

🖥️ System Architecture

The platform combines IoT, machine learning, and real-time web technologies.
Hardware Layer
Raspberry Pi / Microcontroller
Impact and vibration sensors
GPS module
AI Layer
Machine learning model detects accidents from sensor data.
Backend Layer
Event processing
Real-time incident broadcasting
Incident locking system
Frontend Layer
Hospital dashboard built with React
Interactive map visualization
Real-time incident updates

🛠️ Technologies Used
Frontend
React (JavaScript)
Vite
Leaflet Maps
CSS (Linear Gradient UI)
Realtime Communication
BroadcastChannel API (demo)
WebSocket architecture (production)
Hardware / IoT
Raspberry Pi
Vibration / impact sensors
GPS module
AI / ML
Accident detection model (sensor data classification)

🎯 Key Benefits

Reduces emergency response time
Prevents duplicate hospital dispatch
Provides real-time situational awareness
Improves coordination between hospitals and emergency services
Keeps victims’ families informed

🚀 Future Improvements

AI-based accident severity prediction
Automatic ambulance routing using traffic data
Integration with emergency services (police / fire department)
Mobile application for hospitals and responders
Cloud-based real-time infrastructure

📌 Project Goal

Road Guardian aims to create a faster, smarter, and more coordinated emergency response ecosystem, ultimately helping save lives during road accidents.
>>>>>>> 400fc64b1da380c9f8434a8442cde2efbd4e39ab
