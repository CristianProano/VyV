import psycopg2
from psycopg2 import sql
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from datetime import date

# Configuración del servidor RPC
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Clase de servicio de alquiler de carros con conexión a PostgreSQL
class CarRentalService:
    def __init__(self, db_config):
        self.conn = psycopg2.connect(**db_config)
        self.cursor = self.conn.cursor()

    def add_vehicle(self, make, model, year):
        query = sql.SQL("INSERT INTO vehicles (make, model, year, available) VALUES (%s, %s, %s, %s) RETURNING id")
        self.cursor.execute(query, (make, model, year, True))
        vehicle_id = self.cursor.fetchone()[0]
        self.conn.commit()
        return vehicle_id

    def list_vehicles(self):
        query = sql.SQL("SELECT * FROM vehicles")
        self.cursor.execute(query)
        vehicles = self.cursor.fetchall()
        return vehicles

    def add_client(self, name, email):
        query = sql.SQL("INSERT INTO clients (name, email) VALUES (%s, %s) RETURNING id")
        self.cursor.execute(query, (name, email))
        client_id = self.cursor.fetchone()[0]
        self.conn.commit()
        return client_id

    def list_clients(self):
        query = sql.SQL("SELECT * FROM clients")
        self.cursor.execute(query)
        clients = self.cursor.fetchall()
        return clients

    def rent_vehicle(self, vehicle_id, client_id, start_date, end_date):
        query = sql.SQL("SELECT available FROM vehicles WHERE id = %s")
        self.cursor.execute(query, (vehicle_id,))
        available = self.cursor.fetchone()[0]
        
        if available:
            query = sql.SQL("INSERT INTO rentals (vehicle_id, client_id, start_date, end_date, status) VALUES (%s, %s, %s, %s, %s) RETURNING id")
            self.cursor.execute(query, (vehicle_id, client_id, start_date, end_date, 'active'))
            rental_id = self.cursor.fetchone()[0]
            
            query = sql.SQL("UPDATE vehicles SET available = %s WHERE id = %s")
            self.cursor.execute(query, (False, vehicle_id))
            self.conn.commit()
            return rental_id
        else:
            return None

    def list_rentals(self):
        query = sql.SQL("SELECT * FROM rentals")
        self.cursor.execute(query)
        rentals = self.cursor.fetchall()
        rentals_with_str_dates = [
            {
                'id': rental[0],
                'vehicle_id': rental[1],
                'client_id': rental[2],
                'start_date': rental[3].strftime('%Y-%m-%d'),
                'end_date': rental[4].strftime('%Y-%m-%d'),
                'status': rental[5]
            }
            for rental in rentals
        ]
        return rentals_with_str_dates

# Configuración de la base de datos
db_config = {
    'dbname': 'alquilercarros',
    'user': 'postgres',
    'password': '1234',
    'host': 'localhost',
    'port': 5432
}

# Crear el servidor RPC
with SimpleXMLRPCServer(('localhost', 8000), requestHandler=RequestHandler) as server:
    server.register_introspection_functions()
    car_rental_service = CarRentalService(db_config)
    server.register_instance(car_rental_service)
    
    print("Servidor de alquiler de vehículos corriendo en http://localhost:8000")
    server.serve_forever()
