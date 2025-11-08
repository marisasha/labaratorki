import json
import xml.etree.ElementTree as ET
from datetime import datetime, date
from typing import Dict, Any
from models import *


class DataManager:
    @staticmethod
    def to_dict(system: 'TransportSystem') -> Dict[str, Any]:
        """Конвертирует всю систему в словарь для JSON"""
        return {
            "company": {
                "id": system.company.id,
                "name": system.company.name,
                "address": system.company.address,
                "transports": [DataManager._transport_to_dict(t) for t in system.company.transports],
                "drivers": [DataManager._driver_to_dict(d) for d in system.company.drivers]
            },
            "routes": [DataManager._route_to_dict(r) for r in system.routes],
            "trips": [DataManager._trip_to_dict(t) for t in system.trips],
            "passengers": [DataManager._passenger_to_dict(p) for p in system.passengers]
        }
    
    @staticmethod
    def _transport_to_dict(transport: 'Transport') -> Dict[str, Any]:
        base = {
            "id": transport.id,
            "model": transport.model,
            "capacity": transport.capacity,
            "speed": transport.speed,
            "status": transport.status
        }
        if isinstance(transport, Bus):
            base.update({"type": "bus", "route_number": transport.route_number})
        elif isinstance(transport, Train):
            base.update({"type": "train", "wagons": transport.wagons})
        elif isinstance(transport, Tram):
            base.update({"type": "tram", "line_number": transport.line_number})
        return base
    
    @staticmethod
    def _driver_to_dict(driver: 'Driver') -> Dict[str, Any]:
        return {
            "id": driver.id,
            "name": driver.name,
            "license_number": driver.license_number,
            "assigned_trips": [t.id for t in driver.assigned_trips]
        }
    
    @staticmethod
    def _route_to_dict(route: 'Route') -> Dict[str, Any]:
        return {
            "id": route.id,
            "number": route.number,
            "length_km": route.length_km,
            "stops": route.stops
        }
    
    @staticmethod
    def _trip_to_dict(trip: 'Trip') -> Dict[str, Any]:
        return {
            "id": trip.id,
            "date": trip.date.isoformat(),
            "departure_time": trip.departure_time.isoformat(),
            "arrival_time": trip.arrival_time.isoformat(),
            "status": trip.status
        }
    
    @staticmethod
    def _passenger_to_dict(passenger: 'Passenger') -> Dict[str, Any]:
        return {
            "id": passenger.id,
            "full_name": passenger.full_name,
            "phone": passenger.phone,
            "tickets": [{
                "id": t.id,
                "price": t.price,
                "issue_date": t.issue_date.isoformat(),
                "status": t.status
            } for t in passenger.tickets]
        }
    
    @staticmethod
    def save_to_json(system: 'TransportSystem', filename: str):
        """Сохраняет систему в JSON файл"""
        data = DataManager.to_dict(system)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        print(f"Данные сохранены в {filename}")
    
    @staticmethod
    def load_from_json(filename: str, system: 'TransportSystem'):
        """Загружает систему из JSON файла"""
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        DataManager._load_from_dict(data, system)
        print(f"Данные загружены из {filename}")
    
    @staticmethod
    def save_to_xml(system: 'TransportSystem', filename: str):
        """Сохраняет систему в XML файл"""
        root = ET.Element("transport_system")
        
        # Company
        company_elem = ET.SubElement(root, "company")
        company_elem.set("id", str(system.company.id))
        company_elem.set("name", system.company.name)
        company_elem.set("address", system.company.address)
        
        # Transports
        transports_elem = ET.SubElement(company_elem, "transports")
        for transport in system.company.transports:
            transport_elem = ET.SubElement(transports_elem, "transport")
            transport_elem.set("id", str(transport.id))
            transport_elem.set("model", transport.model)
            transport_elem.set("capacity", str(transport.capacity))
            transport_elem.set("speed", str(transport.speed))
            transport_elem.set("status", transport.status)
            
            if isinstance(transport, Bus):
                transport_elem.set("type", "bus")
                transport_elem.set("route_number", transport.route_number)
            elif isinstance(transport, Train):
                transport_elem.set("type", "train")
                transport_elem.set("wagons", str(transport.wagons))
            elif isinstance(transport, Tram):
                transport_elem.set("type", "tram")
                transport_elem.set("line_number", transport.line_number)
        
        # Drivers
        drivers_elem = ET.SubElement(company_elem, "drivers")
        for driver in system.company.drivers:
            driver_elem = ET.SubElement(drivers_elem, "driver")
            driver_elem.set("id", str(driver.id))
            driver_elem.set("name", driver.name)
            driver_elem.set("license_number", driver.license_number)
            
            trips_elem = ET.SubElement(driver_elem, "assigned_trips")
            for trip in driver.assigned_trips:
                ET.SubElement(trips_elem, "trip_id").text = str(trip.id)
        
        # Routes
        routes_elem = ET.SubElement(root, "routes")
        for route in system.routes:
            route_elem = ET.SubElement(routes_elem, "route")
            route_elem.set("id", str(route.id))
            route_elem.set("number", route.number)
            route_elem.set("length_km", str(route.length_km))
            
            stops_elem = ET.SubElement(route_elem, "stops")
            for stop in route.stops:
                ET.SubElement(stops_elem, "stop").text = stop
        
        # Trips
        trips_elem = ET.SubElement(root, "trips")
        for trip in system.trips:
            trip_elem = ET.SubElement(trips_elem, "trip")
            trip_elem.set("id", str(trip.id))
            trip_elem.set("date", trip.date.isoformat())
            trip_elem.set("status", trip.status)
            
            ET.SubElement(trip_elem, "departure_time").text = trip.departure_time.isoformat()
            ET.SubElement(trip_elem, "arrival_time").text = trip.arrival_time.isoformat()
        
        # Passengers
        passengers_elem = ET.SubElement(root, "passengers")
        for passenger in system.passengers:
            passenger_elem = ET.SubElement(passengers_elem, "passenger")
            passenger_elem.set("id", str(passenger.id))
            passenger_elem.set("full_name", passenger.full_name)
            passenger_elem.set("phone", passenger.phone)
            
            tickets_elem = ET.SubElement(passenger_elem, "tickets")
            for ticket in passenger.tickets:
                ticket_elem = ET.SubElement(tickets_elem, "ticket")
                ticket_elem.set("id", str(ticket.id))
                ticket_elem.set("price", str(ticket.price))
                ticket_elem.set("issue_date", ticket.issue_date.isoformat())
                ticket_elem.set("status", ticket.status)
        
        tree = ET.ElementTree(root)
        tree.write(filename, encoding='utf-8', xml_declaration=True)
        print(f"Данные сохранены в {filename}")
    
    @staticmethod
    def load_from_xml(filename: str, system: 'TransportSystem'):
        """Загружает систему из XML файла"""
        tree = ET.parse(filename)
        root = tree.getroot()
        
        # Clear existing data
        system.company.transports.clear()
        system.company.drivers.clear()
        system.routes.clear()
        system.trips.clear()
        system.passengers.clear()
        
        # Load company
        company_elem = root.find("company")
        system.company.id = int(company_elem.get("id"))
        system.company.name = company_elem.get("name")
        system.company.address = company_elem.get("address")
        
        # Load transports
        for transport_elem in company_elem.find("transports"):
            transport_type = transport_elem.get("type")
            transport_id = int(transport_elem.get("id"))
            model = transport_elem.get("model")
            capacity = int(transport_elem.get("capacity"))
            speed = float(transport_elem.get("speed"))
            
            if transport_type == "bus":
                route_number = transport_elem.get("route_number")
                transport = Bus(transport_id, model, capacity, speed, route_number)
            elif transport_type == "train":
                wagons = int(transport_elem.get("wagons"))
                transport = Train(transport_id, model, capacity, speed, wagons)
            elif transport_type == "tram":
                line_number = transport_elem.get("line_number")
                transport = Tram(transport_id, model, capacity, speed, line_number)
            
            transport.status = transport_elem.get("status")
            system.company.transports.append(transport)
        
        # Load drivers and trips first (need trips for assignment)
        temp_trips = {}
        for trip_elem in root.find("trips"):
            trip_id = int(trip_elem.get("id"))
            trip_date = date.fromisoformat(trip_elem.get("date"))
            departure_time = datetime.fromisoformat(trip_elem.find("departure_time").text)
            arrival_time = datetime.fromisoformat(trip_elem.find("arrival_time").text)
            
            trip = Trip(trip_id, trip_date, departure_time, arrival_time)
            trip.status = trip_elem.get("status")
            system.trips.append(trip)
            temp_trips[trip_id] = trip
        
        # Load drivers
        for driver_elem in company_elem.find("drivers"):
            driver_id = int(driver_elem.get("id"))
            name = driver_elem.get("name")
            license_number = driver_elem.get("license_number")
            
            driver = Driver(driver_id, name, license_number)
            
            # Assign trips
            for trip_id_elem in driver_elem.find("assigned_trips"):
                trip_id = int(trip_id_elem.text)
                if trip_id in temp_trips:
                    driver.assigned_trips.append(temp_trips[trip_id])
            
            system.company.drivers.append(driver)
        
        # Load routes
        for route_elem in root.find("routes"):
            route_id = int(route_elem.get("id"))
            number = route_elem.get("number")
            length_km = float(route_elem.get("length_km"))
            
            route = Route(route_id, number, length_km)
            for stop_elem in route_elem.find("stops"):
                route.stops.append(stop_elem.text)
            
            system.routes.append(route)
        
        # Load passengers
        for passenger_elem in root.find("passengers"):
            passenger_id = int(passenger_elem.get("id"))
            full_name = passenger_elem.get("full_name")
            phone = passenger_elem.get("phone")
            
            passenger = Passenger(passenger_id, full_name, phone)
            
            for ticket_elem in passenger_elem.find("tickets"):
                ticket_id = int(ticket_elem.get("id"))
                price = float(ticket_elem.get("price"))
                issue_date = date.fromisoformat(ticket_elem.get("issue_date"))
                
                ticket = Ticket(ticket_id, price, issue_date)
                ticket.status = ticket_elem.get("status")
                passenger.tickets.append(ticket)
            
            system.passengers.append(passenger)
        
        print(f"Данные загружены из {filename}")
    
    @staticmethod
    def _load_from_dict(data: Dict[str, Any], system: 'TransportSystem'):
        """Загружает данные из словаря в систему"""
        # Clear existing data
        system.company.transports.clear()
        system.company.drivers.clear()
        system.routes.clear()
        system.trips.clear()
        system.passengers.clear()
        
        # Load company info
        company_data = data["company"]
        system.company.id = company_data["id"]
        system.company.name = company_data["name"]
        system.company.address = company_data["address"]
        
        # Load transports
        for transport_data in company_data["transports"]:
            transport_type = transport_data["type"]
            if transport_type == "bus":
                transport = Bus(
                    transport_data["id"],
                    transport_data["model"],
                    transport_data["capacity"],
                    transport_data["speed"],
                    transport_data["route_number"]
                )
            elif transport_type == "train":
                transport = Train(
                    transport_data["id"],
                    transport_data["model"],
                    transport_data["capacity"],
                    transport_data["speed"],
                    transport_data["wagons"]
                )
            elif transport_type == "tram":
                transport = Tram(
                    transport_data["id"],
                    transport_data["model"],
                    transport_data["capacity"],
                    transport_data["speed"],
                    transport_data["line_number"]
                )
            
            transport.status = transport_data["status"]
            system.company.transports.append(transport)
        
        # Load trips first (need them for driver assignment)
        temp_trips = {}
        for trip_data in data["trips"]:
            trip = Trip(
                trip_data["id"],
                date.fromisoformat(trip_data["date"]),
                datetime.fromisoformat(trip_data["departure_time"]),
                datetime.fromisoformat(trip_data["arrival_time"])
            )
            trip.status = trip_data["status"]
            system.trips.append(trip)
            temp_trips[trip.id] = trip
        
        # Load drivers
        for driver_data in company_data["drivers"]:
            driver = Driver(
                driver_data["id"],
                driver_data["name"],
                driver_data["license_number"]
            )
            
            # Assign trips to driver
            for trip_id in driver_data["assigned_trips"]:
                if trip_id in temp_trips:
                    driver.assigned_trips.append(temp_trips[trip_id])
            
            system.company.drivers.append(driver)
        
        # Load routes
        for route_data in data["routes"]:
            route = Route(
                route_data["id"],
                route_data["number"],
                route_data["length_km"]
            )
            route.stops = route_data["stops"]
            system.routes.append(route)
        
        # Load passengers
        for passenger_data in data["passengers"]:
            passenger = Passenger(
                passenger_data["id"],
                passenger_data["full_name"],
                passenger_data["phone"]
            )
            
            for ticket_data in passenger_data["tickets"]:
                ticket = Ticket(
                    ticket_data["id"],
                    ticket_data["price"],
                    date.fromisoformat(ticket_data["issue_date"])
                )
                ticket.status = ticket_data["status"]
                passenger.tickets.append(ticket)
            
            system.passengers.append(passenger)