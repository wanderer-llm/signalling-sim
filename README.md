# signalling_sim

Railway signaling system with automated train simulation and timetable scheduling, showing trains moving through the network following schedules with realistic timing.

## Overview

This simulation models trains traveling through a railway network, departing at scheduled times and moving between stations according to a timetable. The system includes:

- **Timetable scheduler**: Define routes, services, and departure schedules
- **Train simulator**: Advance time and move trains through the network
- **Visualizer**: Display the network layout, timetables, and train positions

## Running the Demo

```bash
cd ~/signalling-sim
python3 demo.py
```

The demo creates a simple network with three stations (London Euston, Birmingham New Street, Manchester Piccadilly) and runs trains on the West Coast Main Line Express service departing every 30 minutes.

## Structure

- `network.py` - Station and Network classes for representing the railway network
- `train.py` - Train state and movement logic
- `timetable.py` - Route, Service, Schedule dataclasses and TimetableScheduler
- `simulator.py` - Simulator class that advances time and moves trains
- `visualizer.py` - ASCII visualization functions for the network and trains
- `test_*.py` - Tests for each module

## Parts

1. **timetable_scheduler** - Created Route, Service, Schedule dataclasses and TimetableScheduler. Can add services with routes and frequencies, add schedules with departure times, and get departure times for a service.

2. **simulation_loop** - Implemented advance_time() that advances simulation time and moves trains through the network. Trains depart at their scheduled times, move to the next station after the travel time has elapsed, and arrive at their destination.

3. **schedule_visualizer** - Created visualizer module with draw_network, draw_timetable, draw_train_status, and draw_network_with_trains functions. Visual representation of train schedules and network showing trains moving along them according to their schedules.
