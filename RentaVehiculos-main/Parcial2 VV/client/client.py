import xmlrpc.client

def main():
    with xmlrpc.client.ServerProxy("http://localhost:8000/RPC2") as proxy:
        while True:
            print("Seleccione una opción:")
            print("1. Agregar vehículo")
            print("2. Listar vehículos")
            print("3. Agregar cliente")
            print("4. Listar clientes")
            print("5. Realizar una reserva de alquiler")
            print("6. Listar alquileres")
            print("7. Salir")

            option = input("Ingrese el número de la opción: ")

            if option == '1':
                make = input("Ingrese la marca del vehículo: ")
                model = input("Ingrese el modelo del vehículo: ")
                year = int(input("Ingrese el año del vehículo: "))
                vehicle_id = proxy.add_vehicle(make, model, year)
                print(f"Vehículo agregado con ID: {vehicle_id}")
            
            elif option == '2':
                vehicles = proxy.list_vehicles()
                print("Vehículos disponibles:")
                for vehicle in vehicles:
                    print(vehicle)

            elif option == '3':
                name = input("Ingrese el nombre del cliente: ")
                email = input("Ingrese el email del cliente: ")
                client_id = proxy.add_client(name, email)
                print(f"Cliente agregado con ID: {client_id}")

            elif option == '4':
                clients = proxy.list_clients()
                print("Clientes:")
                for client in clients:
                    print(client)

            elif option == '5':
                vehicle_id = int(input("Ingrese el ID del vehículo: "))
                client_id = int(input("Ingrese el ID del cliente: "))
                start_date = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
                end_date = input("Ingrese la fecha de fin (YYYY-MM-DD): ")
                rental_id = proxy.rent_vehicle(vehicle_id, client_id, start_date, end_date)
                print(f"Reserva de alquiler creada con ID: {rental_id}")

            elif option == '6':
                rentals = proxy.list_rentals()
                print("Alquileres:")
                for rental in rentals:
                    print(rental)

            elif option == '7':
                print("Saliendo...")
                break

            else:
                print("Opción no válida. Inténtelo de nuevo.")

if __name__ == "__main__":
    main()