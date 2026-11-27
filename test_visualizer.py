"""
Tests for the visualizer module.
"""

import sys
sys.path.insert(0, '/home/agent/signalling-sim')

from network import Network
from timetable import TimetableScheduler, Route
from simulator import Simulator
from visualizer import draw_network, draw_timetable, draw_train_status, draw_network_with_trains


def test_draw_network_simple():
    """Test that draw_network produces output for a simple network."""
    net = Network()
    net.add_station('London')
    net.add_station('Birmingham')
    net.connect('London', 'Birmingham')
    
    result = draw_network(net)
    assert len(result) > 0
    assert 'London' in result
    assert 'Birmingham' in result


def test_draw_network_with_multiple_stations():
    """Test that draw_network produces output for a network with multiple stations."""
    net = Network()
    net.add_station('London')
    net.add_station('Birmingham')
    net.add_station('Manchester')
    net.connect('London', 'Birmingham')
    net.connect('Birmingham', 'Manchester')
    
    result = draw_network(net)
    assert len(result) > 0
    assert 'London' in result
    assert 'Birmingham' in result
    assert 'Manchester' in result


def test_draw_timetable():
    """Test that draw_timetable produces output for a service."""
    scheduler = TimetableScheduler()
    route = Route('Test Route', ['Station A', 'Station B'], 60)
    scheduler.add_service('TestService', route, 30)
    
    times = [
        __import__('datetime').time(6, 0),
        __import__('datetime').time(7, 0),
        __import__('datetime').time(8, 0)
    ]
    scheduler.add_schedule('TestService', times)
    
    result = draw_timetable(scheduler, 'TestService')
    assert len(result) > 0
    assert 'TestService' in result
    assert 'Station A' in result
    assert 'Station B' in result


def test_draw_train_status():
    """Test that draw_train_status produces output for a simulator."""
    net = Network()
    net.add_station('London')
    net.add_station('Birmingham')
    net.connect('London', 'Birmingham')
    
    scheduler = TimetableScheduler()
    route = Route('Test Route', ['London', 'Birmingham'], 60)
    scheduler.add_service('TestService', route, 30)
    
    times = [__import__('datetime').time(6, 0)]
    scheduler.add_schedule('TestService', times)
    
    sim = Simulator(net, scheduler)
    sim.current_time = __import__('datetime').time(6, 0)
    sim.create_trains_from_schedule('TestService', times)
    
    result = draw_train_status(sim)
    assert len(result) > 0
    assert 'Train Status' in result
    assert 'stopped' in result
    assert 'London' in result


def test_draw_network_with_trains():
    """Test that draw_network_with_trains produces output showing trains on network."""
    net = Network()
    net.add_station('London')
    net.add_station('Birmingham')
    net.connect('London', 'Birmingham')
    
    sim = Simulator(net, None)
    
    result = draw_network_with_trains(net, sim)
    assert len(result) > 0
    assert 'London' in result
    assert 'Birmingham' in result


def test_draw_network_with_trains_and_train():
    """Test that draw_network_with_trains shows trains on the network."""
    net = Network()
    net.add_station('London')
    net.add_station('Birmingham')
    net.connect('London', 'Birmingham')
    
    scheduler = TimetableScheduler()
    route = Route('Test Route', ['London', 'Birmingham'], 60)
    scheduler.add_service('TestService', route, 30)
    
    times = [__import__('datetime').time(6, 0)]
    scheduler.add_schedule('TestService', times)
    
    sim = Simulator(net, scheduler)
    sim.current_time = __import__('datetime').time(6, 0)
    sim.create_trains_from_schedule('TestService', times)
    sim.advance_time(minutes=30)  # Train should have departed
    
    result = draw_network_with_trains(net, sim)
    assert len(result) > 0
    assert 'London' in result
    assert 'Birmingham' in result
    # Should show at least one train with the service name
    # result is a string, not a list of characters
    assert 'TestService_' in result
