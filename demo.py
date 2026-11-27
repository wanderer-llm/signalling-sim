#!/usr/bin/env python3
"""
Demo of the signalling simulation system.
Shows trains moving through a network following schedules.
"""

import sys
sys.path.insert(0, '/home/agent/signalling-sim')

from datetime import time
from network import Network
from timetable import TimetableScheduler, Route
from simulator import Simulator
from visualizer import draw_network, draw_timetable, draw_train_status, draw_network_with_trains


def main():
    """Run a demo of the signalling simulation."""
    print("=" * 60)
    print("Railway Signalling Simulation Demo")
    print("=" * 60)
    print()
    
    # Create a simple network: London -> Birmingham -> Manchester
    net = Network()
    net.add_station('London Euston')
    net.add_station('Birmingham New Street')
    net.add_station('Manchester Piccadilly')
    net.connect('London Euston', 'Birmingham New Street')
    net.connect('Birmingham New Street', 'Manchester Piccadilly')
    
    print(draw_network(net))
    print()
    
    # Create a timetable with frequent trains
    scheduler = TimetableScheduler()
    route = Route('West Coast Main Line', ['London Euston', 'Birmingham New Street', 'Manchester Piccadilly'], 120)
    scheduler.add_service('WCML_Express', route, 30)  # Every 30 minutes
    
    # Add a schedule with departures every hour starting at 6:00
    departure_times = [
        time(6, 0), time(7, 0), time(8, 0), time(9, 0),
        time(10, 0), time(11, 0), time(12, 0), time(13, 0),
        time(14, 0), time(15, 0), time(16, 0), time(17, 0)
    ]
    scheduler.add_schedule('WCML_Express', departure_times)
    
    print(draw_timetable(scheduler, 'WCML_Express'))
    print()
    
    # Create the simulator
    sim = Simulator(net, scheduler)
    sim.current_time = time(6, 0)
    sim.create_trains_from_schedule('WCML_Express', departure_times)
    
    print(f"Created {len(sim.trains)} trains")
    print()
    
    # Show initial state
    print("Initial State (6:00):")
    print(draw_train_status(sim))
    print()
    
    # Advance time and show changes
    print("Advancing time...")
    print("-" * 60)
    
    # Advance to 6:30 (first train should have departed)
    sim.advance_time(minutes=30)
    print(f"\nTime: {sim.current_time}")
    print(draw_train_status(sim))
    print()
    
    # Advance to 7:00 (second train should depart)
    sim.advance_time(minutes=30)
    print(f"\nTime: {sim.current_time}")
    print(draw_train_status(sim))
    print()
    
    # Advance to 7:30 (first train should be moving, second departed)
    sim.advance_time(minutes=30)
    print(f"\nTime: {sim.current_time}")
    print(draw_train_status(sim))
    print()
    
    # Advance to 8:00 (second train should be moving)
    sim.advance_time(minutes=30)
    print(f"\nTime: {sim.current_time}")
    print(draw_train_status(sim))
    print()
    
    # Advance to 8:30 (first train should arrive at Birmingham)
    sim.advance_time(minutes=30)
    print(f"\nTime: {sim.current_time}")
    print(draw_train_status(sim))
    print()
    
    # Advance to 9:00 (first train should arrive at Manchester)
    sim.advance_time(minutes=60)
    print(f"\nTime: {sim.current_time}")
    print(draw_train_status(sim))
    print()
    
    # Show final state
    print("=" * 60)
    print("Final State:")
    print(draw_train_status(sim))
    print()
    
    # Show network with train positions
    print(draw_network_with_trains(net, sim))
    print()
    
    print("=" * 60)
    print("Demo complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()
