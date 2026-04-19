# Smart Waste Management System

Built by **Team Hex Protocol**

Most cities still run garbage trucks on fixed schedules, down the same streets, whether there's waste or not. This project flips that. Citizens report waste in real time, an AI model classifies it, a route engine figures out the most efficient path for each truck, and admins watch everything unfold on a live dashboard. IoT bins feed into the same pipeline automatically.

This repo contains three working modules — each independently runnable, each designed to slot into a unified system.

---

## What's Inside

| Module | What it does |
|--------|-------------|
| `ml model/` | Real-time waste classification via webcam using YOLOv8 |
| `Route Optimization/` | Multi-truck route planning on Delhi's actual road network |
| `Waste Management System/` | Full-stack resident + driver + admin platform (React + Node + MongoDB) |

---

## Module 1 — AI Waste Classification

A YOLOv8s model running live on a webcam feed. Point it at waste, it tells you what category it is, with a color-coded bounding box and confidence score.

### Waste Categories

| Class | Label | Box Color |
|-------|-------|-----------|
| 0 | Biodegradable | Green |
| 1 | Recyclable | Blue |
| 2 | Hazardous | Red |

### Setup

```bash
pip install ultralytics opencv-python
python app.py
```

> Uses camera index `1` by default. Switch to `cv2.VideoCapture(0)` if you're on a laptop with a built-in webcam.

### Model Config

| Parameter | Value | What it controls |
|-----------|-------|-----------------|
| `conf` | 0.5 | Minimum confidence to show a detection |
| `iou` | 0.4 | Overlap threshold for NMS |
| Weights | `best-yolov8s.pt` | Custom-trained on waste categories |

Press `q` to exit cleanly.

### Structure

```
ml model/
├── app.py
├── best-yolov8s.pt
└── README.md
```

---

## Module 2 — Route Optimization Engine

The routing brain of the system. It loads Delhi's real road network from OpenStreetMap, distributes houses across it, takes garbage reports (simulated or live from IoT bins), and computes optimized multi-truck collection routes using KMeans + TSP + Dijkstra.

### How the Routing Works

1. Houses are placed on valid road nodes using grid-based sampling — one node per grid cell, minimum 50m apart
2. Community bins are placed near house clusters
3. When garbage is reported, the system clusters locations by truck using KMeans
4. TSP finds the best visit order within each cluster
5. Dijkstra computes the actual shortest road path between stops
6. All trucks deploy from a central processing center in North Delhi

TSP optimization cuts route distance by roughly 20–35% compared to naive sequential visits. Running multiple trucks in parallel cuts total collection time by 60–80%.

### IoT Integration

ESP32 boards with ultrasonic sensors push bin fill levels to the backend in real time. The dashboard reflects changes in under a second.

```cpp
const char* ssid     = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* server_url = "http://YOUR_LAPTOP_IP:5000/api/bin_status";

#define TRIG1 5
#define ECHO1 18
#define TRIG2 17
#define ECHO2 16
```

### Visual Feedback

The map uses a clear icon progression so you always know what's been done:

- 🏠 → 🟠 (garbage reported) → 🟢 (queued for collection) → ✅ (collected)
- 🗑️ → 🟠 (bin full) → ✅ (emptied)

Checkmarks are permanent — they don't revert on polling.

### Setup

```bash
git clone https://github.com/Siva-Barath/Route-Optimization-for-Smart-Waste-Management-System.git
cd "Route Optimization"
pip install -r requirements.txt
python smart_waste_demo.py
```

Open `http://localhost:5000` in your browser.

### Dashboard Workflow

1. Generate City — spreads 65+ houses across Delhi on real road nodes
2. Start Reporting Window — 2-minute window for citizens to report waste
3. Report Garbage — click houses on the map to flag them
4. IoT Updates — ESP32 sensors push bin status automatically
5. Optimize Routes — TSP + Dijkstra calculates the best paths
6. Deploy Fleet — trucks move in real time from the processing center
7. Monitor — watch progress per truck, per zone, per stop

### Tech Stack

| Layer | Tools |
|-------|-------|
| Backend | Python, Flask |
| Routing | OSMnx, NetworkX, Dijkstra, TSP, KMeans (scikit-learn) |
| Frontend | Leaflet.js, HTML5, CSS3, JavaScript |
| IoT | ESP32, Ultrasonic Sensors, HTTP/WiFi |
| Map Data | OpenStreetMap |

### Structure

```
Route Optimization/
├── smart_waste_demo.py
├── requirements.txt
├── test_iot.py
├── simple_iot.py
└── templates/
    ├── admin.html
    ├── user_registration.html
    └── user_app.html
```

---

## Module 3 — EcoCircle Web Platform

The full-stack application that ties residents, drivers, and admins together. Built with React + Express + MongoDB, with JWT auth, role-based access, an incentive system, and real-time notifications.

### Roles

**Resident**
- Register with address, ward, and household size
- Report daily garbage with waste type (biodegradable, recyclable, hazardous, mixed)
- Track today's collection status and driver assignment
- See their position in the route queue
- View 30-day collection history
- Earn incentive points for proper segregation
- Get notifications for reminders, confirmations, and alerts
- View personal stats with charts (segregation score, waste type breakdown, collection rate)

**Driver**
- View today's assigned route and stop list
- Mark each stop as `collected` or `skipped`
- Get notified when new garbage is reported nearby

**Admin**
- Live dashboard: total households, reporting today, collected, skipped, pending, active routes, efficiency %
- Ward-wise reporting breakdown
- 7-day trend chart (reported vs collected)
- Waste type distribution chart
- Manage all households, drivers, and collections

### Setup

**Backend**
```bash
cd server
npm install
cp .env.example .env
npm run dev
```
Runs on `http://localhost:5000`

**Frontend**
```bash
cd client
npm install
npm run dev
```
Runs on `http://localhost:5173`

MongoDB is optional — if it's not running locally, the server falls back to an in-memory instance automatically.

### Environment Variables

| Variable | Description |
|----------|-------------|
| `PORT` | Server port (default: 5000) |
| `JWT_SECRET` | JWT signing secret |
| `NODE_ENV` | `development` or `production` |
| `MONGO_ATLAS_URL` | Atlas connection string (optional) |
| `LOCAL_MONGO_URI` | Override local MongoDB URI |
| `SKIP_SEED` | Set `true` to skip demo data seeding |

### Demo Credentials

| Role | Phone | Password |
|------|-------|----------|
| Admin | `9999999999` | `admin123` |
| Driver | `8000000001` | `driver123` |
| Resident | `7000000000` | `user123` |

### API Reference

| Method | Path | Role | Description |
|--------|------|------|-------------|
| POST | `/api/auth/register` | Public | Register new user |
| POST | `/api/auth/login` | Public | Login |
| GET | `/api/auth/profile` | Any | Get own profile |
| PUT | `/api/auth/profile` | Any | Update name/language/password |
| GET | `/api/auth/lookup?phone=` | Public | Check if phone exists |
| POST | `/api/garbage/report` | Resident | Submit daily garbage report |
| GET | `/api/garbage/today` | Resident | Today's report status |
| GET | `/api/garbage/history` | Resident | Last 30 reports |
| GET | `/api/garbage/collection-status` | Resident | Collection status + route position |
| GET | `/api/garbage/my-stats` | Resident | Personal stats and chart data |
| GET | `/api/garbage/incentives` | Resident | Points history and total |
| GET | `/api/admin/stats` | Admin | Dashboard overview + charts |
| GET | `/api/admin/households` | Admin | All households |
| GET | `/api/admin/drivers` | Admin | All drivers |
| GET | `/api/admin/collections` | Admin | Today's collections |
| GET | `/api/admin/routes` | Admin | Today's routes |
| GET | `/api/notifications` | Any | Get own notifications |
| PUT | `/api/notifications/:id/read` | Any | Mark notification as read |
| GET | `/api/health` | Public | Server + DB health check |

### Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 19, Vite, Tailwind CSS v4, React Router v7, Recharts |
| Backend | Node.js, Express 5, Mongoose 7 |
| Database | MongoDB (local or in-memory fallback) |
| Auth | JWT (7-day tokens), bcryptjs |
| Tunneling | localtunnel (LAN/mobile access) |

### Scripts

```bash
# Server
npm run dev          # Start dev server
npm run tunnel       # Expose via localtunnel for mobile testing
npm run test:atlas   # Test MongoDB Atlas connection
npm run migrate:atlas # Migrate local data to Atlas

# Client
npm run dev          # Vite dev server
npm run build        # Production build
npm run lint         # ESLint
```

### Structure

```
Waste Management System/
├── client/
│   └── src/
│       ├── pages/
│       │   ├── admin/
│       │   ├── driver/
│       │   ├── resident/
│       │   └── login/
│       ├── components/
│       ├── context/
│       └── api.js
└── server/
    ├── models/index.js
    ├── routes/
    │   ├── auth.js
    │   ├── garbage.js
    │   ├── admin.js
    │   ├── notifications.js
    │   └── routes.js
    ├── middleware/auth.js
    └── index.js
```

---

## Full Project Structure

```
Smart Waste Management System/
├── ml model/                    # YOLOv8 waste classification
│   ├── app.py
│   └── best-yolov8s.pt
├── Route Optimization/          # Flask routing engine
│   ├── smart_waste_demo.py
│   ├── requirements.txt
│   └── templates/
└── Waste Management System/     # Full-stack web platform
    ├── client/                  # React frontend
    └── server/                  # Node.js backend
```

---

## How the Modules Connect

```
Resident App  ──→  Backend (Node)  ──→  Route Optimization (Flask)  ──→  Driver App
                        │                          │
                   Admin Dashboard          IoT Bin Data (ESP32)
                        │
                   AI Classification (YOLOv8)
```

In the current prototype, each module runs independently. The integration path is:
- Resident reports from EcoCircle feed into the Route Optimization engine
- AI classification runs at the point of reporting to auto-tag waste type
- IoT bin data supplements citizen reports with real fill-level data
- Drivers follow routes generated by the optimization engine
- Admins monitor everything through the EcoCircle dashboard

---

## What's Next

- Live GPS tracking for trucks
- Full integration of all three modules into one deployed system
- Edge deployment of the YOLOv8 model (on-device inference)
- Predictive analytics for waste generation patterns
- ML-based route improvement over time
- Segregation-based reward system tied to EcoCircle incentive points
- City-scale deployment with real municipal data

---

## License

MIT

---

*Team Hex Protocol*