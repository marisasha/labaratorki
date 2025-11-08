from models import *
from data_manager import DataManager
from datetime import datetime, date

if __name__ == "__main__":
    system = TransportSystem()
    
    try:
        # Попытка создать автобус с некорректной вместимостью
        bad_bus = Bus(10, "Bad Bus", -5, 60.0, "101")
    except ValueError as e:
        print(f"Ошибка при создании автобуса: {e}")

    # + транспорт
    bus = Bus(1, "Mercedes Citaro", 50, 60.0, "101")
    tram = Tram(2, "Tatra T3", 80, 40.0, "3")
    system.company.transports.extend([bus, tram])
    
    # + водитель
    driver = Driver(1, "Иванов Иван", "AB123456")
    system.company.drivers.append(driver)
    
    # + маршрут
    route = Route(1, "101", 15.5)
    route.stops = ["Центральный вокзал", "Университет", "Стадион"]
    system.routes.append(route)
    
    # + рейс
    trip = Trip(1, date(2024, 1, 15), datetime(2024, 1, 15, 8, 0), datetime(2024, 1, 15, 8, 45))
    system.trips.append(trip)
    
    driver.assigned_trips.append(trip)
    
    # + пассажир с билетом
    passenger = Passenger(1, "Маринушкин Александр", "+79991234567")
    ticket = Ticket(1, 45.5, date(2024, 1, 15))
    passenger.tickets.append(ticket)
    system.passengers.append(passenger)
    
    # Демонстрация работы системы
    print("ДЕМОНСТРАЦИЯ РАБОТЫ СИСТЕМЫ")
    bus.start()
    trip.start_trip()
    print(bus.get_info())
    print(trip.get_info())
    
    print("\nСОХРАНЕНИЕ ДАННЫХ")
    # Сохраняем в JSON
    DataManager.save_to_json(system, "transport_system.json")
    
    # Сохраняем в XML
    DataManager.save_to_xml(system, "transport_system.xml")
    
    print("\n=== ЗАГРУЗКА ДАННЫХ ===")
    # Загружаем из JSON
    new_system = TransportSystem()
    DataManager.load_from_json("transport_system.json", new_system)
    
    print(f"Загружено транспорта: {len(new_system.company.transports)}")
    print(f"Загружено водителей: {len(new_system.company.drivers)}")
    print(f"Загружено маршрутов: {len(new_system.routes)}")
    print(f"Загружено рейсов: {len(new_system.trips)}")
    print(f"Загружено пассажиров: {len(new_system.passengers)}")
    
    if new_system.company.transports:
        print(f"\nПервый транспорт: {new_system.company.transports[0].get_info()}")

