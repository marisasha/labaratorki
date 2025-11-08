from datetime import datetime, date, timedelta
from typing import List, Optional

class Company:
    def __init__(self, id: int, name: str, address: str):
        self.id = id
        self.name = name
        self.address = address
        self.transports: List[Transport] = []
        self.drivers: List[Driver] = []
    
    def add_transport(self, t: 'Transport'):
        self.transports.append(t)
        print(f"Транспорт {t.model} добавлен в компанию")
    
    def remove_transport(self, id: int):
        self.transports = [t for t in self.transports if t.id != id]
        print(f"Транспорт с ID {id} удален")
    
    def hire_driver(self, d: 'Driver'):
        self.drivers.append(d)
        print(f"Водитель {d.name} нанят")
    
    def fire_driver(self, id: int):
        self.drivers = [d for d in self.drivers if d.id != id]
        print(f"Водитель с ID {id} уволен")

class Transport:
    def __init__(self, id: int, model: str, capacity: int, speed: float):
        self.id = id
        self.model = model
        self.capacity = capacity
        self.speed = speed
        self.status = "stopped"
    
    def start(self):
        self.status = "running"
        print(f"Транспорт {self.model} запущен")
    
    def stop(self):
        self.status = "stopped"
        print(f"Транспорт {self.model} остановлен")
    
    def update_info(self, model: str, capacity: int):
        self.model = model
        self.capacity = capacity
        print(f"Информация транспорта обновлена: {model}, вместимость {capacity}")
    
    def get_info(self) -> str:
        return f"Транспорт ID: {self.id}, Модель: {self.model}, Вместимость: {self.capacity}, Скорость: {self.speed}, Статус: {self.status}"

class Bus(Transport):
    def __init__(self, id: int, model: str, capacity: int, speed: float, route_number: str):
        if capacity <= 0:
            raise ValueError("Вместимость автобуса должна быть положительной")
        if not model:
            raise ValueError("Модель автобуса не может быть пустой")
        super().__init__(id, model, capacity, speed)
        self.route_number = route_number

class Train(Transport):
    def __init__(self, id: int, model: str, capacity: int, speed: float, wagons: str):
        if capacity <= 0:
            raise ValueError("Вместимость поезда должна быть положительной")
        if not model:
            raise ValueError("Модель поезда не может быть пустой")
        super().__init__(id, model, capacity, speed)
        self.wagons = wagons
    
    def show_type(self) -> str:
        return "Поезд"

class Tram(Transport):
    def __init__(self, id: int, model: str, capacity: int, speed: float, line_number: str):
        if capacity <= 0:
            raise ValueError("Вместимость трамвая должна быть положительной")
        if not model:
            raise ValueError("Модель трамвая не может быть пустой")
        self.line_number = line_number
    
    def show_type(self) -> str:
        return "Трамвай"

class Driver:
    def __init__(self, id: int, name: str, license_number: str):
        self.id = id
        self.name = name
        self.license_number = license_number
        self.assigned_trips: List[Trip] = []
    
    def assign_trip(self, trip: 'Trip'):
        self.assigned_trips.append(trip)
        print(f"Рейс {trip.id} назначен водителю {self.name}")
    
    def remove_trip(self, trip_id: int):
        self.assigned_trips = [t for t in self.assigned_trips if t.id != trip_id]
        print(f"Рейс {trip_id} удален у водителя {self.name}")
    
    def update_license(self, new_license: str):
        self.license_number = new_license
        print(f"Лицензия водителя {self.name} обновлена")

class Route:
    def __init__(self, id: int, number: str, length_km: float):
        self.id = id
        self.number = number
        self.length_km = length_km
        self.stops: List[str] = []
    
    def add_stop(self, stop_name: str):
        self.stops.append(stop_name)
        print(f"Остановка '{stop_name}' добавлена к маршруту {self.number}")
    
    def remove_stop(self, stop_name: str):
        if stop_name in self.stops:
            self.stops.remove(stop_name)
            print(f"Остановка '{stop_name}' удалена из маршруту {self.number}")
        else:
            print(f"Остановка '{stop_name}' не найдена в маршруте {self.number}")
    
    def update_length(self, km: float):
        self.length_km = km
        print(f"Длина маршрута {self.number} обновлена: {km} км")
    
    def get_stops_info(self) -> str:
        return f"Маршрут {self.number}: {', '.join(self.stops)}"

class Trip:
    def __init__(self, id: int, trip_date: date, departure_time: datetime, arrival_time: datetime):
        self.id = id
        self.date = trip_date
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.status = "scheduled"
    
    def start_trip(self):
        self.status = "in_progress"
        print(f"Рейс {self.id} начат")
    
    def finish_trip(self):
        self.status = "completed"
        print(f"Рейс {self.id} завершен")
    
    def update_times(self, new_departure: datetime, new_arrival: datetime):
        self.departure_time = new_departure
        self.arrival_time = new_arrival
        print(f"Время рейса {self.id} обновлено: отправление {new_departure}, прибытие {new_arrival}")
    
    def get_duration(self) -> timedelta:
        return self.arrival_time - self.departure_time
    
    def get_info(self) -> str:
        duration = self.get_duration()
        return f"Рейс ID: {self.id}, Дата: {self.date}, Статус: {self.status}, Отправление: {self.departure_time}, Прибытие: {self.arrival_time}, Длительность: {duration}"

class Passenger:
    def __init__(self, id: int, full_name: str, phone: str):
        self.id = id
        self.full_name = full_name
        self.phone = phone
        self.tickets: List[Ticket] = []
    
    def buy_ticket(self, trip: Trip, price: float) -> 'Ticket':
        ticket = Ticket(len(self.tickets) + 1, price, date.today())
        self.tickets.append(ticket)
        print(f"Билет куплен пассажиром {self.full_name} на рейс {trip.id}")
        return ticket
    
    def cancel_ticket(self, ticket_id: int):
        for ticket in self.tickets:
            if ticket.id == ticket_id:
                ticket.cancel()
                self.tickets.remove(ticket)
                print(f"Билет {ticket_id} отменен пассажиром {self.full_name}")
                return
        print(f"Билет {ticket_id} не найден")
    
    def update_contact(self, phone: str):
        self.phone = phone
        print(f"Контактные данные пассажира {self.full_name} обновлены")

class Ticket:
    def __init__(self, id: int, price: float, issue_date: date):
        if price <= 0:
            raise ValueError("Цена билета должна быть положительной")
        self.id = id
        self.price = price
        self.issue_date = issue_date
        self.status = "active"

    def cancel(self):
        self.status = "cancelled"
        print(f"Билет {self.id} отменен")
    
    def update_price(self, price: float):
        self.price = price
        print(f"Цена билета {self.id} обновлена: {price}")

class TransportSystem:
    """Класс для управления всей транспортной системой"""
    def __init__(self):
        self.company = Company(1, "Городской транспорт", "ул. Центральная, 1")
        self.routes: List[Route] = []
        self.trips: List[Trip] = []
        self.passengers: List[Passenger] = []