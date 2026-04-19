♻️ Smart Waste Management System
AI + Route Optimization + Citizen Platform

Developed by Team Hex Protocol

📌 Project Overview

This project is a Smart Waste Management System prototype designed to improve how garbage is:

📍 Reported by citizens
🚛 Collected using optimized routes
🧠 Classified using AI
📊 Monitored through a centralized dashboard

The system combines AI, route optimization, full-stack applications, and IoT integration to create a scalable solution for urban waste management.

🧩 Core Idea

Current waste collection systems:

Follow fixed routes ❌
Ignore real-time waste availability ❌
Lack monitoring and transparency ❌
✅ Our Solution:
Citizens report waste in real-time
System optimizes routes dynamically
Drivers follow efficient paths
Admins monitor everything live
AI helps in waste classification
🏗️ System Architecture (Simplified)
Resident App → Backend → Route Optimization → Driver → Collection
                         ↓
                    Admin Dashboard
                         ↓
                    IoT Bin Data
🚀 Implemented Modules (Prototype)
🧠 1. AI Waste Classification
Built using YOLOv8
Detects:
Biodegradable
Recyclable
Hazardous
Runs on webcam (real-time detection)
Displays bounding boxes + confidence
🚛 2. Route Optimization Engine
Uses real road networks (OpenStreetMap via OSMnx)
Algorithms:
KMeans → truck clustering
TSP → optimal visit order
Dijkstra → shortest path
Features:
Multi-truck route planning
Realistic house distribution
Smart bin integration
Interactive map dashboard
Real-time simulation of truck movement
🌐 3. Waste Management Web Platform

A full-stack system connecting Residents, Drivers, and Admins.

👤 Resident
Register with address
Report garbage
View collection status
Track route progress
View history and stats
🚚 Driver
View assigned routes
Mark collection status
🧑‍💼 Admin
Monitor system dashboard
Manage households and drivers
View waste statistics
Key Features:
JWT authentication
Role-based access
Notification system
Incentive tracking
📡 4. IoT Integration (Prototype Level)
ESP32 + ultrasonic sensors
Detects bin fill level
Sends real-time updates to backend
Reflected in dashboard
⚙️ Tech Stack
Layer	Technology
AI	YOLOv8 (Ultralytics)
Backend (Routing)	Flask, OSMnx, NetworkX
Backend (App)	Node.js, Express
Frontend	React, Tailwind CSS
Database	MongoDB
Maps	OpenStreetMap
IoT	ESP32
🔄 How It Works
Residents report garbage via app
Data stored in backend
Route optimization calculates best paths
Trucks follow optimized routes
Drivers update collection status
Admin monitors entire system
IoT bins provide additional real-time input
AI module demonstrates waste classification
📁 Project Structure
Smart Waste Management System/
├── ml model/                  # YOLOv8 waste detection
├── Route Optimization/        # Routing engine (Flask + OSMnx)
├── Waste management System/   # Full-stack app
│   ├── client/                # React frontend
│   └── server/                # Node backend
🛠️ Running the Project
AI Model
pip install ultralytics opencv-python
python app.py
Route Optimization
cd Route Optimization
pip install -r requirements.txt
python smart_waste_demo.py
Full-Stack App

Backend:

cd server
npm install
npm run dev

Frontend:

cd client
npm install
npm run dev
🎯 What This Project Demonstrates
Real-world route optimization using road networks
End-to-end waste reporting → collection pipeline
Multi-role web application system
AI capability for waste classification
IoT-ready architecture
🔮 Future Scope
Full integration of all modules
Real-time GPS tracking
Edge deployment of AI model
Large-scale city deployment
👥 Team

Hex Protocol

📌 Note

This repository contains working prototypes of individual modules.
These modules are designed to be integrated into a complete smart waste management system for real-world deployment.