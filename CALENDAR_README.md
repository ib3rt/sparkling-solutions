# 🔐 Sparkling Solutions Secure Calendar

**Date:** 2026-02-05  
**Purpose:** Host & Cleaner schedule coordination with secure authentication

---

## 🎯 Features

### 🔐 Security
- **JWT Authentication** - Secure token-based login
- **Role-Based Access** - Host and Cleaner roles
- **API Keys** - Secure API access
- **Password Hashing** - SHA-256 encrypted passwords

### 📅 Calendar Features
- **Interactive Calendar** - Visual booking management
- **Check-in/Check-out** - Coordinate guest departures and arrivals
- **Booking Status** - Pending, Confirmed, In Progress, Completed
- **Dual Confirmation** - Both host AND cleaner must confirm

### 👥 User Roles
- **Host** - Create bookings, manage properties, confirm cleanings
- **Cleaner** - View schedule, confirm bookings, update status
- **Admin** - Full system access

---

## 📁 Files

| File | Purpose |
|------|---------|
| `calendar-secure.html` | Frontend calendar UI with login |
| `calendar-api.py` | Backend API with authentication |
| `dashboard.html` | Host dashboard overview |
| `index.html` | Main landing page |

---

## 🚀 Quick Start

### 1. Access the Calendar

```bash
# Open in browser
open brands/sparkling-solutions/calendar-secure.html
```

### 2. Demo Login

**Host Account:**
- Email: `host@sparklingsolutions.biz`
- Password: `host123`

**Cleaner Account:**
- Email: `cleaner@sparklingsolutions.biz`
- Password: `cleaner123`

### 3. Create a Booking

1. Sign in as Host
2. Click "+ New Booking"
3. Select property
4. Choose check-in/check-out dates
5. Add notes (access codes, instructions)
6. Click "Create Booking"

### 4. Confirm Booking

1. Cleaner receives notification
2. Cleaner signs in and confirms
3. Host confirms (or vice versa)
4. Booking status changes to "Confirmed"

---

## 📊 Dashboard Features

### Overview Stats
- Upcoming cleanings
- Pending confirmations
- Completed this month
- Properties managed

### Calendar View
- Monthly calendar with booking dots
- Green = Check-in
- Red = Check-out
- Yellow = Pending

### Booking Management
- Create new bookings
- Confirm/cancel bookings
- View booking history
- Property assignment

---

## 🔧 API Endpoints

### Authentication
```
POST /calendar-api.py
Body: { "action": "login", "email": "...", "password": "..." }
Response: { "token": "...", "user_id": "...", "name": "...", "role": "..." }
```

### Bookings
```
GET /calendar-api.py?action=bookings&user_id=...
POST /calendar-api.py (create booking)
PUT /calendar-api.py (update booking)
```

### Calendar Data
```
GET /calendar-api.py?action=calendar&month=2&year=2026
```

---

## 💾 Data Storage

**Location:** `brands/sparkling-solutions/calendar_data.json`

**Structure:**
```json
{
  "users": [...],
  "properties": [...],
  "bookings": [...],
  "api_keys": {...}
}
```

---

## 🎨 Design Features

- **Dark Theme** - Easy on the eyes
- **Responsive** - Works on mobile
- **Interactive** - Smooth animations
- **Accessible** - Clear status indicators

---

## 🔒 Security Measures

1. **Password Hashing** - SHA-256 encryption
2. **Session Tokens** - API key authentication
3. **Role Separation** - Host vs Cleaner access
4. **Dual Confirmation** - Both parties must agree

---

## 📅 Workflow

```
Host Creates Booking
     ↓
Pending Status
     ↓
Cleaner Reviews & Confirms
     ↓
Host Confirms
     ↓
Booking Confirmed ✓
     ↓
Cleaner Completes Job
     ↓
Status: Completed
```

---

## 🚀 Deployment

### Vercel (Recommended)
```bash
cd brands/sparkling-solutions
vercel deploy
```

### Static Hosting
Upload these files to any static host:
- `calendar-secure.html`
- `calendar-api.py` (requires Python backend)
- `dashboard.html`

---

## 📝 Notes

- Demo mode works without backend (uses JavaScript data)
- Full security requires Python backend deployment
- All data stored locally in `calendar_data.json`
- Easy to extend with database backend

---

**Built with 🔐 Security First Approach**
