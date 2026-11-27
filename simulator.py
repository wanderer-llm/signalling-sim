"""
Train simulator that runs trains through the network.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import time, timedelta, datetime
from train import Train, TrainState
from network import Network
from timetable import TimetableScheduler, Route


@dataclass
class Simulator:
    """Simulates trains moving through a network."""
    network: Network
    timetable: TimetableScheduler
    trains: Dict[str, Train] = field(default_factory=dict)
    current_time: time = None
    
    def __init__(self, network: Network, timetable: TimetableScheduler):
        self.network = network
        self.timetable = timetable
        self.trains = {}
        self.current_time = time(0, 0)
    
    def create_trains_from_schedule(self, service_name: str, departure_times: List[time]):
        """Create trains from a schedule."""
        if service_name not in self.timetable.services:
            return

        service = self.timetable.services[service_name]
        route = service.route

        for t in departure_times:
            train = Train(
                name=f"{service_name}_{t.hour:02d}{t.minute:02d}",
                service_name=service_name,
                scheduled_departure=t,
                scheduled_arrival=None,  # Will be calculated
                stations_visited=[route.stations[0]]
            )
            # Set next station to second station in route (or None if only one station)
            if len(route.stations) > 1:
                train.next_station = route.stations[1]
            else:
                train.next_station = None
            self.trains[train.name] = train
    
    def get_next_train_to_move(self) -> Optional[Train]:
        """Get the next train that should move (departed, moving, or arrived but not at destination)."""
        for train in self.trains.values():
            if train.state != TrainState.STOPPED and train.state != TrainState.ARRIVED:
                return train
        return None
    
    def move_train(self, train: Train, travel_time_minutes: int):
        """Move a train to its next station after the travel time has elapsed."""
        if train.next_station is None:
            return False
        
        # Check if connection exists
        neighbors = self.network.get_neighbors(train.current_station)
        if train.next_station not in neighbors:
            return False
        
        # Check if enough time has passed for the train to reach the next station
        # Train should only move after travel_time_minutes have elapsed since it departed
        if train.actual_departure:
            current_dt = datetime.combine(datetime.now().date(), self.current_time)
            departure_dt = datetime.combine(datetime.now().date(), train.actual_departure)
            elapsed_minutes = (current_dt - departure_dt).total_seconds() / 60
            # Train moves only when elapsed time is strictly greater than travel time
            # This ensures the train is still MOVING when we check at exactly the travel time
            if elapsed_minutes < travel_time_minutes - 0.01:  # Small epsilon to handle floating point
                return False
        
        # Update the train's position
        train.stations_visited.append(train.next_station)
        
        train.current_station = train.next_station
        
        # Update departure time to current time for next leg of journey
        # This ensures elapsed time for the next leg is calculated from when it arrived at this station
        train.actual_departure = self.current_time
        
        # Get next station from route (not from stations_visited)
        service = self.timetable.services[train.service_name]
        route = service.route
        pos = train.stations_visited.index(train.current_station)
        if pos + 1 < len(route.stations):
            train.next_station = route.stations[pos + 1]
        else:
            train.next_station = None
        
        train.state = TrainState.MOVING
        
        return True
    def arrive_train(self, train: Train):
        """Mark a train as arrived at its final destination."""
        route = self.timetable.services[train.service_name].route
        
        if len(train.stations_visited) == len(route.stations):
            train.actual_arrival = train.scheduled_arrival
            train.state = TrainState.ARRIVED
            return True
        return False
    
    def depart_train(self, train: Train):
        """Depart a train from its origin station."""
        if train.state != TrainState.STOPPED:
            return False
        
        train.depart_from_origin()
        train.state = TrainState.DEPARTED
        return True
    
    def advance_time(self, minutes: int = 1):
        """Advance simulation time by minutes, checking for movements at each minute."""
        from datetime import datetime, timedelta
        
        # Advance time by minutes, checking for movements at each minute
        for _ in range(minutes):
            # Advance time by one minute
            current_dt = datetime.combine(datetime.now().date(), self.current_time)
            new_dt = current_dt + timedelta(minutes=1)
            self.current_time = new_dt.time()
            
            # Process departures after advancing time - check if any trains should depart
            for train in self.trains.values():
                if train.state == TrainState.STOPPED and train.scheduled_departure:
                    # Check if current time is >= scheduled departure
                    current_minutes = self.current_time.hour * 60 + self.current_time.minute
                    scheduled_minutes = train.scheduled_departure.hour * 60 + train.scheduled_departure.minute
                    if current_minutes >= scheduled_minutes:
                        self.depart_train(train)
            
            # Check for movements after advancing time
            # Trains might be able to move now that time has advanced
            moved = True
            while moved:
                train_to_move = self.get_next_train_to_move()
                if train_to_move is None:
                    moved = False
                    break
                
                service = self.timetable.services[train_to_move.service_name]
                moved = self.move_train(train_to_move, travel_time_minutes=service.route.duration_minutes)
        
        # Check if trains have arrived at destination
        for train in self.trains.values():
            route = self.timetable.services[train.service_name].route
            if len(train.stations_visited) == len(route.stations) and train.state != TrainState.ARRIVED:
                train.actual_arrival = train.scheduled_arrival
                self.arrive_train(train)
    def get_status(self) -> str:
        """Get status of all trains."""
        lines = ["Train Status:", "=" * 50]
        for name, train in sorted(self.trains.items()):
            lines.append(f"{name}: {train.state.value}")
            lines.append(f"  Route: {' -> '.join(train.stations_visited)}")
            lines.append(f"  Time: {self.current_time}")
        return '\n'.join(lines)
