"""Tests for timetable scheduling."""

import pytest
from timetable import Route, Service, TimetableScheduler
from datetime import time


def test_create_route():
    """Test creating a route."""
    route = Route('Line 1', ['A', 'B', 'C'], 30)
    assert route.name == 'Line 1'
    assert route.stations == ['A', 'B', 'C']
    assert route.duration_minutes == 30


def test_create_service():
    """Test creating a service."""
    route = Route('Line 1', ['A', 'B'], 20)
    service = Service('Line1', route, 15)
    assert service.name == 'Line1'
    assert service.route.stations == ['A', 'B']
    assert service.frequency_minutes == 15


def test_add_service():
    """Test adding a service to scheduler."""
    scheduler = TimetableScheduler()
    route = Route('Line 1', ['A', 'B'], 20)
    scheduler.add_service('Line1', route, 15)
    
    service = scheduler.get_service('Line1')
    assert service is not None
    assert service.name == 'Line1'


def test_add_schedule():
    """Test adding a schedule."""
    scheduler = TimetableScheduler()
    route = Route('Line 1', ['A', 'B'], 20)
    scheduler.add_service('Line1', route, 15)
    
    times = [time(6, 0), time(7, 0), time(8, 0)]
    scheduler.add_schedule('Line1', times)
    
    assert 'Line1' in scheduler.schedules


def test_get_departure_times():
    """Test getting departure times."""
    scheduler = TimetableScheduler()
    route = Route('Line 1', ['A', 'B'], 20)
    scheduler.add_service('Line1', route, 15)
    times = [time(6, 0), time(7, 0), time(8, 0)]
    scheduler.add_schedule('Line1', times)
    
    departures = scheduler.get_departure_times('Line1')
    assert len(departures) == 3
    assert departures[0] == time(6, 0)
    assert departures[1] == time(7, 0)
    assert departures[2] == time(8, 0)


def test_get_service():
    """Test getting service details."""
    scheduler = TimetableScheduler()
    route = Route('Line 1', ['A', 'B'], 20)
    scheduler.add_service('Line1', route, 15)
    
    service = scheduler.get_service('Line1')
    assert service is not None
    assert service.frequency_minutes == 15


def test_next_departure():
    """Test getting next departure after current time."""
    scheduler = TimetableScheduler()
    route = Route('Line 1', ['A', 'B'], 20)
    scheduler.add_service('Line1', route, 15)
    times = [time(6, 0), time(7, 0), time(8, 0)]
    scheduler.add_schedule('Line1', times)
    
    # Next departure after 6:30 should be 7:00
    next_dep = scheduler.get_next_departure('Line1', time(6, 30))
    assert next_dep == time(7, 0)
    
    # Next departure after 8:30 should be None (no more departures)
    next_dep = scheduler.get_next_departure('Line1', time(8, 30))
    assert next_dep is None


def test_format_timetable():
    """Test formatting a timetable."""
    scheduler = TimetableScheduler()
    route = Route('Line 1', ['Station A', 'Station B', 'Station C'], 30)
    scheduler.add_service('Line1', route, 15)
    times = [time(6, 0), time(7, 0), time(8, 0)]
    scheduler.add_schedule('Line1', times)
    
    output = scheduler.format_timetable('Line1')
    lines = output.split('\n')
    assert lines[0] == 'Service: Line1'
    assert 'Station A -> Station B -> Station C' in lines[1]
    assert 'Frequency: Every 15 minutes' in lines[2]


def test_missing_service():
    """Test that missing service returns empty list."""
    scheduler = TimetableScheduler()
    departures = scheduler.get_departure_times('NonExistent')
    assert departures == []
