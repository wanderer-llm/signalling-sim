"""
Visual representation of railway network and train movements.
"""

from typing import Dict, List, Optional
from datetime import time


def format_time(t: time) -> str:
    """Format a time as HH:MM."""
    return f"{t.hour:02d}:{t.minute:02d}"


def draw_network(network) -> str:
    """Draw a simple ASCII representation of the network."""
    lines = []
    lines.append("Network Layout:")
    lines.append("=" * 60)
    
    # Get all stations sorted by name
    station_names = sorted(network.stations.keys())
    
    # Find the widest station name for alignment
    max_name_len = max(len(name) for name in station_names) if station_names else 0
    
    # Draw each station and its connections
    for station_name in station_names:
        station = network.stations[station_name]
        neighbors = station.connections
        
        # Draw station name
        lines.append(f"[{station_name:<{max_name_len}}]")
        
        # Draw connections
        if neighbors:
            lines.append("  |")
            for neighbor in sorted(neighbors):
                lines.append(f"  +-- [{neighbor:<{max_name_len}}]")
        else:
            lines.append("  (no connections)")
        
        lines.append("")
    
    return '\n'.join(lines)


def draw_timetable(scheduler, service_name: str) -> str:
    """Draw a timetable for a service."""
    if service_name not in scheduler.schedules:
        return f"Service {service_name} not found"
    
    service = scheduler.schedules[service_name].service
    times = scheduler.schedules[service_name].departure_times
    
    lines = []
    lines.append(f"Service: {service.name}")
    lines.append("-" * 60)
    lines.append(f"Route: {' -> '.join(service.route.stations)}")
    lines.append(f"Frequency: Every {service.frequency_minutes} minutes")
    lines.append("Departures:")
    
    for t in times:
        lines.append(f"  {format_time(t)}")
    
    return '\n'.join(lines)


def draw_train_status(simulator) -> str:
    """Draw the status of all trains."""
    lines = []
    lines.append("Train Status:")
    lines.append("=" * 60)
    
    for name, train in sorted(simulator.trains.items()):
        lines.append(f"\n{name}:")
        lines.append(f"  State: {train.state.value}")
        lines.append(f"  Current station: {train.current_station}")
        lines.append(f"  Route: {' -> '.join(train.stations_visited)}")
        
        if train.scheduled_departure:
            lines.append(f"  Scheduled departure: {format_time(train.scheduled_departure)}")
        if train.actual_departure:
            lines.append(f"  Actual departure: {format_time(train.actual_departure)}")
        
        if train.scheduled_arrival:
            lines.append(f"  Scheduled arrival: {format_time(train.scheduled_arrival)}")
        if train.actual_arrival:
            lines.append(f"  Actual arrival: {format_time(train.actual_arrival)}")
    
    return '\n'.join(lines)


def draw_network_with_trains(network, simulator) -> str:
    """Draw the network with train positions overlaid."""
    lines = []
    lines.append("Network with Trains:")
    lines.append("=" * 60)
    
    # Get all stations sorted by name
    station_names = sorted(network.stations.keys())
    
    # Find the widest station name for alignment
    max_name_len = max(len(name) for name in station_names) if station_names else 0
    
    # Build a map of train positions
    train_positions = {}
    for name, train in simulator.trains.items():
        if train.current_station:
            train_positions[train.current_station] = train.name
    
    # Draw each station and its connections
    for station_name in station_names:
        station = network.stations[station_name]
        neighbors = station.connections
        
        # Draw station name
        lines.append(f"[{station_name:<{max_name_len}}]")
        
        # Check if there's a train at this station
        if station_name in train_positions:
            lines.append(f"  |  <- {train_positions[station_name]}")
        elif neighbors:
            lines.append("  |")
        else:
            lines.append("  (no connections)")
        
        # Draw connections
        for neighbor in sorted(neighbors):
            if neighbor in train_positions:
                lines.append(f"  +-- [{neighbor:<{max_name_len}}] <- {train_positions[neighbor]}")
            else:
                lines.append(f"  +-- [{neighbor:<{max_name_len}}]")
        
        lines.append("")
    
    return '\n'.join(lines)
