import xmlrpc.client

class ExitException(Exception):
    pass

def main():
    server = xmlrpc.client.ServerProxy('http://localhost:8000')

    while True:
        print("Seleccione una opción:")
        print("1. Agregar vehículo")
        print("2. Listar vehículos")
        print("3. Agregar cliente")
        print("4. Listar clientes")
        print("5. Realizar una reserva de alquiler")
        print("6. Listar alquileres")
        print("7. Salir")
        opcion = input()

        if opcion == '1':
            marca = input("Ingrese la marca del vehículo: ")
            modelo = input("Ingrese el modelo del vehículo: ")
            year = int(input("Ingrese el año del vehículo: "))
            id_vehiculo = server.add_vehicle(marca, modelo, year)
            print(f"Vehículo agregado con ID: {id_vehiculo}")

        elif opcion == '2':
            vehiculos = server.list_vehicles()
            print("Vehículos disponibles:")
            for v in vehiculos:
                print(v)

        elif opcion == '3':
            nombre = input("Ingrese el nombre del cliente: ")
            email = input("Ingrese el email del cliente: ")
            id_cliente = server.add_client(nombre, email)
            print(f"Cliente agregado con ID: {id_cliente}")

        elif opcion == '4':
            clientes = server.list_clients()
            print("Clientes:")
            for c in clientes:
                print(c)

        elif opcion == '5':
            id_vehiculo = int(input("Ingrese el ID del vehículo: "))
            id_cliente = int(input("Ingrese el ID del cliente: "))
            fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
            fecha_fin = input("Ingrese la fecha de fin (YYYY-MM-DD): ")
            id_reserva = server.rent_vehicle(id_vehiculo, id_cliente, fecha_inicio, fecha_fin)
            print(f"Reserva de alquiler creada con ID: {id_reserva}")

        elif opcion == '6':
            alquileres = server.list_rentals()
            print("Alquileres:")
            for a in alquileres:
                print(a)

        elif opcion == '7':
            print("Saliendo...")
            raise ExitException

        else:
            print("Opción no válida, intente de nuevo.")

