"""
Train simulation.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import time, timedelta
from enum import Enum


class TrainState(Enum):
    """State of a train."""
    STOPPED = "stopped"
    MOVING = "moving"
    ARRIVED = "arrived"
    DEPARTED = "departed"


@dataclass
class Train:
    """A train moving through the network."""
    name: str
    service_name: str
    current_station: str = None
    next_station: str = None
    state: TrainState = TrainState.STOPPED
    scheduled_departure: Optional[time] = None  # When train should depart first station
    scheduled_arrival: Optional[time] = None  # When train should arrive at last station
    actual_departure: Optional[time] = None  # Actual departure time from origin
    actual_arrival: Optional[time] = None  # Actual arrival time at destination
    last_move_time: Optional[time] = None  # When train last moved (for tracking travel time)
    stations_visited: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        if self.current_station is None:
            self.current_station = self.stations_visited[0] if self.stations_visited else None
    
    def move_to_next(self, network, travel_time_minutes: int):
        """Move train to next station."""
        if self.state != TrainState.MOVING:
            return False
        
        if self.next_station is None:
            return False
        
        # Check if connection exists
        neighbors = network.get_neighbors(self.current_station)
        if self.next_station not in neighbors:
            return False
        
        # Update position
        self.stations_visited.append(self.next_station)
        self.current_station = self.next_station
        
        # Get next station
        if len(self.stations_visited) < 2:
            self.next_station = self.stations_visited[1] if len(self.stations_visited) > 1 else None
        else:
            self.next_station = self.stations_visited[-1]
        
        self.state = TrainState.MOVING
        
        return True
    
    def arrive_at_destination(self):
        """Mark train as arrived at final destination."""
        if self.state == TrainState.ARRIVED:
            return False
        
        self.actual_arrival = self.scheduled_arrival
        self.state = TrainState.ARRIVED
        return True
    
    def depart_from_origin(self):
        """Mark train as departed from origin."""
        if self.state == TrainState.DEPARTED:
            return False
        
        self.actual_departure = self.scheduled_departure
        self.state = TrainState.DEPARTED
        return True
    
    def get_route(self) -> List[str]:
        """Get the route (stations visited) for this train."""
        return self.stations_visited.copy()
