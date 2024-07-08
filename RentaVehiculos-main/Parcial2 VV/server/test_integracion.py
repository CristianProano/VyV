import unittest
from xmlrpc.client import ServerProxy
from datetime import date
import xmlrunner
import os

class TestIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Conectar al servidor RPC
        cls.client_service = ServerProxy('http://localhost:8000')

    def test_add_and_list_client(self):
        # Añadir un cliente
        client_id = self.client_service.add_client('John Doe', 'john@example.com')
        
        # Listar clientes y verificar que el cliente agregado está presente
        clients = self.client_service.list_clients()
        self.assertTrue(any(client == [client_id, 'John Doe', 'john@example.com'] for client in clients))

    def test_add_and_list_vehicle(self):
        # Añadir un vehículo
        vehicle_id = self.client_service.add_vehicle('Toyota', 'Corolla', 2020)
        
        # Listar vehículos y verificar el estado de disponibilidad
        vehicles = self.client_service.list_vehicles()
        added_vehicle = next(vehicle for vehicle in vehicles if vehicle[0] == vehicle_id)
        self.assertTrue(added_vehicle[4])  # Verifica que el vehículo esté disponible

    def test_rent_vehicle(self):
        # Añadir un cliente y un vehículo
        client_id = self.client_service.add_client('John Doe', 'john@example.com')
        vehicle_id = self.client_service.add_vehicle('Toyota', 'Corolla', 2020)
        
        # Realizar una reserva de alquiler
        start_date = date.today().isoformat()
        end_date = (date.today()).isoformat()
        rental_id = self.client_service.rent_vehicle(vehicle_id, client_id, start_date, end_date)
        
        # Verificar que la reserva se realizó correctamente
        self.assertIsNotNone(rental_id)

        # Verificar que el vehículo no esté disponible después de la reserva
        vehicles = self.client_service.list_vehicles()
        rented_vehicle = next(vehicle for vehicle in vehicles if vehicle[0] == vehicle_id)
        self.assertFalse(rented_vehicle[4])  # Verifica que el vehículo esté no disponible

        # Listar alquileres y verificar que haya exactamente uno
        rentals = self.client_service.list_rentals()
        self.assertTrue(any(rental['id'] == rental_id for rental in rentals))

if __name__ == '__main__':
    # Crear el directorio test-reports si no existe
    os.makedirs('test-reports', exist_ok=True)
    
    with open('test-reports/results.xml', 'wb') as output:
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output=output), failfast=False, buffer=False, catchbreak=False)

