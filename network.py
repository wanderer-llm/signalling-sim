"""
Railway network representation.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from collections import defaultdict


@dataclass
class Station:
    """A station or junction in the network."""
    name: str
    connections: List[str] = field(default_factory=list)  # Names of connected stations


@dataclass
class Network:
    """A railway network with stations and connections."""
    stations: Dict[str, Station] = field(default_factory=dict)
    
    def add_station(self, name: str):
        """Add a station to the network."""
        if name not in self.stations:
            self.stations[name] = Station(name)
        return self.stations[name]
    
    def connect(self, station_a: str, station_b: str):
        """Connect two stations."""
        if station_a not in self.stations:
            self.add_station(station_a)
        if station_b not in self.stations:
            self.add_station(station_b)
        
        self.stations[station_a].connections.append(station_b)
        self.stations[station_b].connections.append(station_a)
    
    def get_neighbors(self, station: str) -> List[str]:
        """Get neighboring stations for a given station."""
        if station not in self.stations:
            return []
        return self.stations[station].connections.copy()
    
    def get_distance(self, station_a: str, station_b: str) -> int:
        """Get distance (number of connections) between two stations using BFS."""
        if station_a not in self.stations or station_b not in self.stations:
            return float('inf')
        
        if station_a == station_b:
            return 0
        
        visited = {station_a}
        queue = [(station_a, 0)]
        
        while queue:
            current, dist = queue.pop(0)
            for neighbor in self.get_neighbors(current):
                if neighbor == station_b:
                    return dist + 1
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        
        return float('inf')
