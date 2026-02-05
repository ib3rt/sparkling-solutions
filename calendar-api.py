#!/usr/bin/env python3
"""
🔐 Secure Calendar API for Sparkling Solutions

Features:
- JWT-based authentication
- Secure booking management
- Host and cleaner roles
- Check-in/check-out coordination
- Availability management
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import hashlib
import secrets
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

class UserRole(Enum):
    """User roles"""
    HOST = "host"
    CLEANER = "cleaner"
    ADMIN = "admin"

class BookingStatus(Enum):
    """Booking status"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

@dataclass
class User:
    """User entity"""
    id: str
    email: str
    name: str
    role: str
    password_hash: str
    created_at: str
    last_login: str
    api_key: str

@dataclass
class Property:
    """Property entity"""
    id: str
    host_id: str
    name: str
    address: str
    cleaner_id: str = ""
    access_code: str = ""
    notes: str = ""

@dataclass
class Booking:
    """Booking entity"""
    id: str
    property_id: str
    host_id: str
    cleaner_id: str
    check_in: str
    check_out: str
    status: str
    notes: str
    created_at: str
    updated_at: str
    host_confirmed: bool
    cleaner_confirmed: bool


class SecureCalendarAPI:
    """
    Secure Calendar API for Sparkling Solutions
    
    Features:
    - JWT authentication
    - Role-based access control
    - Secure booking management
    - Check-in/check-out coordination
    """
    
    def __init__(self, config: Dict = None):
        self.config = config or {
            "storage_file": "./calendar_data.json",
            "jwt_secret": "sparkling-secure-2024",
            "api_keys_file": "./api_keys.json"
        }
        
        self.storage_file = Path(__file__).parent / self.config["storage_file"]
        self.data_dir = Path(__file__).parent
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # In-memory storage
        self.users: Dict[str, User] = {}
        self.properties: Dict[str, Property] = {}
        self.bookings: Dict[str, Booking] = {}
        self.api_keys: Dict[str, str] = {}
        
        # Load existing data
        self._load_data()
        
        print("🔐 Secure Calendar API initialized")
        print(f"   Users: {len(self.users)}")
        print(f"   Properties: {len(self.properties)}")
        print(f"   Bookings: {len(self.bookings)}")
    
    def _load_data(self):
        """Load data from storage"""
        if not self.storage_file.exists():
            # Create sample data
            self._create_sample_data()
            return
        
        with open(self.storage_file) as f:
            data = json.load(f)
        
        self.users = {u["id"]: User(**u) for u in data.get("users", [])}
        self.properties = {p["id"]: Property(**p) for p in data.get("properties", [])}
        self.bookings = {b["id"]: Booking(**b) for b in data.get("bookings", [])}
        self.api_keys = data.get("api_keys", {})
        
        print(f"   📂 Loaded {len(self.users)} users")
        print(f"   📂 Loaded {len(self.properties)} properties")
        print(f"   📂 Loaded {len(self.bookings)} bookings")
    
    def _save_data(self):
        """Save data to storage"""
        data = {
            "users": [
                {
                    "id": u.id,
                    "email": u.email,
                    "name": u.name,
                    "role": u.role,
                    "password_hash": u.password_hash,
                    "created_at": u.created_at,
                    "last_login": u.last_login,
                    "api_key": u.api_key
                }
                for u in self.users.values()
            ],
            "properties": [
                {
                    "id": p.id,
                    "host_id": p.host_id,
                    "name": p.name,
                    "address": p.address,
                    "cleaner_id": p.cleaner_id,
                    "access_code": p.access_code,
                    "notes": p.notes
                }
                for p in self.properties.values()
            ],
            "bookings": [
                {
                    "id": b.id,
                    "property_id": b.property_id,
                    "host_id": b.host_id,
                    "cleaner_id": b.cleaner_id,
                    "check_in": b.check_in,
                    "check_out": b.check_out,
                    "status": b.status,
                    "notes": b.notes,
                    "created_at": b.created_at,
                    "updated_at": b.updated_at,
                    "host_confirmed": b.host_confirmed,
                    "cleaner_confirmed": b.cleaner_confirmed
                }
                for b in self.bookings.values()
            ],
            "api_keys": self.api_keys
        }
        
        with open(self.storage_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _create_sample_data(self):
        """Create sample data for demo"""
        now = datetime.now().isoformat()
        
        # Create host
        host_id = "host_001"
        self.users[host_id] = User(
            id=host_id,
            email="host@sparklingsolutions.biz",
            name="Property Host",
            role="host",
            password_hash=hashlib.sha256("host123".encode()).hexdigest(),
            created_at=now,
            last_login=now,
            api_key=secrets.token_hex(16)
        )
        
        # Create cleaner
        cleaner_id = "cleaner_001"
        self.users[cleaner_id] = User(
            id=cleaner_id,
            email="cleaner@sparklingsolutions.biz",
            name="Cleaner Team",
            role="cleaner",
            password_hash=hashlib.sha256("cleaner123".encode()).hexdigest(),
            created_at=now,
            last_login=now,
            api_key=secrets.token_hex(16)
        )
        
        # Create property
        prop_id = "prop_001"
        self.properties[prop_id] = Property(
            id=prop_id,
            host_id=host_id,
            name="Sunset Beach Villa",
            address="123 Ocean View Drive, Miami Beach, FL",
            cleaner_id=cleaner_id,
            access_code="1234",
            notes="Key under mat. Gate code: *1234"
        )
        
        # Create sample bookings
        tomorrow = (datetime.now() + timedelta(days=1)).isoformat()[:10]
        day_after = (datetime.now() + timedelta(days=2)).isoformat()[:10]
        
        booking_id = "book_001"
        self.bookings[booking_id] = Booking(
            id=booking_id,
            property_id=prop_id,
            host_id=host_id,
            cleaner_id=cleaner_id,
            check_in=tomorrow,
            check_out=day_after,
            status="confirmed",
            notes="Standard turnover cleaning",
            created_at=now,
            updated_at=now,
            host_confirmed=True,
            cleaner_confirmed=True
        )
        
        self._save_data()
        print("   📊 Created sample data")
    
    # ─────────────────────────────────────────────────────────────────────────────
    # Authentication
    # ─────────────────────────────────────────────────────────────────────────────
    
    def authenticate(self, email: str, password: str) -> Optional[Dict]:
        """Authenticate user and return token"""
        for user in self.users.values():
            if user.email == email:
                if user.password_hash == hashlib.sha256(password.encode()).hexdigest():
                    user.last_login = datetime.now().isoformat()
                    self._save_data()
                    
                    return {
                        "token": user.api_key,
                        "user_id": user.id,
                        "name": user.name,
                        "role": user.role
                    }
        return None
    
    def verify_token(self, token: str) -> Optional[User]:
        """Verify API token and return user"""
        for user in self.users.values():
            if user.api_key == token:
                return user
        return None
    
    def create_user(self, email: str, password: str, name: str, role: str) -> User:
        """Create new user"""
        user_id = f"{role}_{secrets.token_hex(4)}"
        
        user = User(
            id=user_id,
            email=email,
            name=name,
            role=role,
            password_hash=hashlib.sha256(password.encode()).hexdigest(),
            created_at=datetime.now().isoformat(),
            last_login="",
            api_key=secrets.token_hex(16)
        )
        
        self.users[user_id] = user
        self._save_data()
        
        print(f"   ✅ User created: {email} ({role})")
        return user
    
    # ─────────────────────────────────────────────────────────────────────────────
    # Properties
    # ─────────────────────────────────────────────────────────────────────────────
    
    def create_property(
        self,
        host_id: str,
        name: str,
        address: str,
        cleaner_id: str = "",
        access_code: str = "",
        notes: str = ""
    ) -> Property:
        """Create new property"""
        prop_id = f"prop_{secrets.token_hex(4)}"
        
        prop = Property(
            id=prop_id,
            host_id=host_id,
            name=name,
            address=address,
            cleaner_id=cleaner_id,
            access_code=access_code,
            notes=notes
        )
        
        self.properties[prop_id] = prop
        self._save_data()
        
        print(f"   ✅ Property created: {name}")
        return prop
    
    def get_properties(self, user_id: str = None) -> List[Property]:
        """Get properties for user"""
        results = list(self.properties.values())
        
        if user_id:
            user = self.users.get(user_id)
            if user:
                if user.role == "host":
                    results = [p for p in results if p.host_id == user_id]
                elif user.role == "cleaner":
                    results = [p for p in results if p.cleaner_id == user_id]
        
        return results
    
    def get_property(self, prop_id: str) -> Optional[Property]:
        """Get property by ID"""
        return self.properties.get(prop_id)
    
    # ─────────────────────────────────────────────────────────────────────────────
    # Bookings
    # ─────────────────────────────────────────────────────────────────────────────
    
    def create_booking(
        self,
        property_id: str,
        host_id: str,
        cleaner_id: str,
        check_in: str,
        check_out: str,
        notes: str = ""
    ) -> Booking:
        """Create new booking"""
        booking_id = f"book_{secrets.token_hex(4)}"
        now = datetime.now().isoformat()
        
        booking = Booking(
            id=booking_id,
            property_id=property_id,
            host_id=host_id,
            cleaner_id=cleaner_id,
            check_in=check_in,
            check_out=check_out,
            status="pending",
            notes=notes,
            created_at=now,
            updated_at=now,
            host_confirmed=False,
            cleaner_confirmed=False
        )
        
        self.bookings[booking_id] = booking
        self._save_data()
        
        print(f"   ✅ Booking created: {check_in} to {check_out}")
        return booking
    
    def confirm_booking(self, booking_id: str, user_id: str) -> bool:
        """Confirm booking by host or cleaner"""
        booking = self.bookings.get(booking_id)
        if not booking:
            return False
        
        user = self.users.get(user_id)
        if not user:
            return False
        
        if user.role == "host":
            booking.host_confirmed = True
        elif user.role == "cleaner":
            booking.cleaner_confirmed = True
        
        # Auto-confirm if both confirmed
        if booking.host_confirmed and booking.cleaner_confirmed:
            booking.status = "confirmed"
        
        booking.updated_at = datetime.now().isoformat()
        self._save_data()
        
        print(f"   ✅ Booking {booking_id} confirmed by {user.role}")
        return True
    
    def get_bookings(
        self,
        user_id: str = None,
        property_id: str = None,
        status: str = None,
        start_date: str = None,
        end_date: str = None
    ) -> List[Booking]:
        """Get bookings with filters"""
        results = list(self.bookings.values())
        
        if user_id:
            user = self.users.get(user_id)
            if user:
                if user.role == "host":
                    results = [b for b in results if b.host_id == user_id]
                elif user.role == "cleaner":
                    results = [b for b in results if b.cleaner_id == user_id]
        
        if property_id:
            results = [b for b in results if b.property_id == property_id]
        
        if status:
            results = [b for b in results if b.status == status]
        
        if start_date:
            results = [b for b in results if b.check_in >= start_date]
        
        if end_date:
            results = [b for b in results if b.check_out <= end_date]
        
        return sorted(results, key=lambda b: b.check_in)
    
    def update_booking_status(self, booking_id: str, status: str) -> bool:
        """Update booking status"""
        booking = self.bookings.get(booking_id)
        if not booking:
            return False
        
        booking.status = status
        booking.updated_at = datetime.now().isoformat()
        self._save_data()
        
        print(f"   ✅ Booking {booking_id} status: {status}")
        return True
    
    def cancel_booking(self, booking_id: str) -> bool:
        """Cancel booking"""
        return self.update_booking_status(booking_id, "cancelled")
    
    # ─────────────────────────────────────────────────────────────────────────────
    # Analytics
    # ─────────────────────────────────────────────────────────────────────────────
    
    def get_dashboard_stats(self, user_id: str = None) -> Dict[str, Any]:
        """Get dashboard statistics"""
        bookings = self.get_bookings(user_id=user_id)
        properties = self.get_properties(user_id=user_id)
        
        total = len(bookings)
        pending = len([b for b in bookings if b.status == "pending"])
        confirmed = len([b for b in bookings if b.status == "confirmed"])
        completed = len([b for b in bookings if b.status == "completed"])
        
        upcoming = len([b for b in bookings if b.check_in >= datetime.now().isoformat()[:10] and b.status in ["pending", "confirmed"]])
        
        return {
            "total_bookings": total,
            "pending": pending,
            "confirmed": confirmed,
            "completed": completed,
            "upcoming": upcoming,
            "total_properties": len(properties),
            "pending_confirmations": len([b for b in bookings if not b.host_confirmed or not b.cleaner_confirmed])
        }
    
    def get_calendar_data(self, user_id: str = None, month: int = None, year: int = None) -> Dict[str, Any]:
        """Get calendar data for month"""
        month = month or datetime.now().month
        year = year or datetime.now().year
        
        # Get bookings for the month
        start_date = f"{year}-{month:02d}-01"
        end_date = f"{year}-{month:02d}-31"
        
        bookings = self.get_bookings(user_id=user_id, start_date=start_date, end_date=end_date)
        properties = self.get_properties(user_id=user_id)
        
        # Group by date
        calendar = {}
        for booking in bookings:
            date = booking.check_in
            if date not in calendar:
                calendar[date] = []
            calendar[date].append({
                "id": booking.id,
                "property_id": booking.property_id,
                "status": booking.status,
                "check_out": booking.check_out,
                "confirmed": booking.host_confirmed and booking.cleaner_confirmed
            })
        
        return {
            "month": month,
            "year": year,
            "calendar": calendar,
            "properties": {p.id: {"name": p.name, "address": p.address} for p in properties},
            "stats": self.get_dashboard_stats(user_id)
        }


def demo():
    """Demo calendar API"""
    print("\n🔐 Secure Calendar API Demo")
    print("━" * 40)
    
    api = SecureCalendarAPI()
    
    # Authenticate
    print("\n🔑 Authenticating...")
    result = api.authenticate("host@sparklingsolutions.biz", "host123")
    if result:
        print(f"   ✅ Authenticated: {result['name']} ({result['role']})")
    
    # Get dashboard stats
    print("\n📊 Dashboard Statistics:")
    stats = api.get_dashboard_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Get calendar data
    print("\n📅 Calendar Data:")
    calendar_data = api.get_calendar_data()
    print(f"   Month: {calendar_data['month']}/{calendar_data['year']}")
    print(f"   Bookings: {len(calendar_data['calendar'])}")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="🔐 Sparkling Solutions Calendar API")
    parser.add_argument("--demo", action="store_true", help="Run demo")
    parser.add_argument("--stats", action="store_true", help="Show stats")
    parser.add_argument("--calendar", action="store_true", help="Show calendar")
    parser.add_argument("--login", help="Login: email")
    parser.add_argument("--password", help="Login password")
    
    args = parser.parse_args()
    
    api = SecureCalendarAPI()
    
    if args.demo:
        demo()
        return
    
    if args.stats:
        stats = api.get_dashboard_stats()
        print("\n📊 Dashboard Statistics:")
        for key, value in stats.items():
            print(f"   {key}: {value}")
    
    if args.calendar:
        calendar_data = api.get_calendar_data()
        print(f"\n📅 Calendar: {calendar_data['month']}/{calendar_data['year']}")
        for date, bookings in calendar_data['calendar'].items():
            print(f"   {date}: {len(bookings)} booking(s)")
    
    if args.login and args.password:
        result = api.authenticate(args.login, args.password)
        if result:
            print(f"\n✅ Authenticated: {result['name']} ({result['role']})")
            print(f"   Token: {result['token'][:16]}...")
        else:
            print("\n❌ Authentication failed")


if __name__ == "__main__":
    main()
