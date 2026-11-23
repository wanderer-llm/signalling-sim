"""
Timetable scheduling for trains.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import time, timedelta


@dataclass
class Route:
    """A route through the railway network."""
    name: str
    stations: List[str]  # List of station/junction names in order
    duration_minutes: int  # Estimated travel time in minutes


@dataclass
class Service:
    """A service (train type) with a route and frequency."""
    name: str
    route: Route
    frequency_minutes: int  # How often this service runs


@dataclass 
class Schedule:
    """A schedule for a particular service on a specific day."""
    service: Service
    departure_times: List[time]  # Times when trains depart from first station
    date: str = "2026-11-23"  # Default to today


class TimetableScheduler:
    """Manages train schedules and generates timetables."""
    
    def __init__(self):
        self.services: Dict[str, Service] = {}
        self.schedules: Dict[str, Schedule] = {}
    
    def add_service(self, name: str, route: Route, frequency_minutes: int):
        """Add a service to the timetable."""
        self.services[name] = Service(name, route, frequency_minutes)
    
    def add_schedule(self, service_name: str, departure_times: List[time], date: str = "2026-11-23"):
        """Add a schedule for a service."""
        if service_name not in self.services:
            raise ValueError(f"Service {service_name} not found")
        self.schedules[service_name] = Schedule(self.services[service_name], departure_times, date)
    
    def get_departure_times(self, service_name: str) -> List[time]:
        """Get departure times for a service."""
        if service_name not in self.schedules:
            return []
        return self.schedules[service_name].departure_times
    
    def get_service(self, service_name: str) -> Optional[Service]:
        """Get service details."""
        return self.services.get(service_name)
    
    def get_next_departure(self, service_name: str, current_time: time = None) -> Optional[time]:
        """Get the next departure time after current_time."""
        if service_name not in self.schedules:
            return None
        if current_time is None:
            current_time = time(0, 0)
        
        times = sorted(self.schedules[service_name].departure_times)
        for t in times:
            if t > current_time:
                return t
        return None
    
    def format_timetable(self, service_name: str) -> str:
        """Format a timetable for a service."""
        if service_name not in self.schedules:
            return f"Service {service_name} not found"
        
        service = self.schedules[service_name].service
        times = self.schedules[service_name].departure_times
        
        lines = [f"Service: {service.name}",
                 f"Route: {' -> '.join(service.route.stations)}",
                 f"Frequency: Every {service.frequency_minutes} minutes",
                 f"Departures: {', '.join(str(t) for t in times)}"]
        return '\n'.join(lines)
