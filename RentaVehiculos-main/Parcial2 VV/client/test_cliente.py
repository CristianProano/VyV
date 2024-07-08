import unittest
from unittest.mock import patch, MagicMock
import io
from cliente import main, ExitException

class TestCliente(unittest.TestCase):

    @patch('xmlrpc.client.ServerProxy')
    def test_add_vehicle(self, mock_server):
        mock_server.return_value.add_vehicle.return_value = 1
        with patch('builtins.input', side_effect=['1', 'Toyota', 'Corolla', '2020', '7']), \
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(ExitException):
                main()
            mock_server.return_value.add_vehicle.assert_called_with('Toyota', 'Corolla', 2020)
            output = mock_stdout.getvalue()
            self.assertIn("Vehículo agregado con ID: 1", output)

    @patch('xmlrpc.client.ServerProxy')
    def test_list_vehicles(self, mock_server):
        mock_server.return_value.list_vehicles.return_value = [(1, 'Toyota', 'Corolla', 2020, True)]
        with patch('builtins.input', side_effect=['2', '7']), \
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(ExitException):
                main()
            mock_server.return_value.list_vehicles.assert_called_once()
            output = mock_stdout.getvalue()
            self.assertIn("Vehículos disponibles:", output)

    @patch('xmlrpc.client.ServerProxy')
    def test_add_client(self, mock_server):
        mock_server.return_value.add_client.return_value = 1
        with patch('builtins.input', side_effect=['3', 'John Doe', 'john@example.com', '7']), \
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(ExitException):
                main()
            mock_server.return_value.add_client.assert_called_with('John Doe', 'john@example.com')
            output = mock_stdout.getvalue()
            self.assertIn("Cliente agregado con ID: 1", output)

    @patch('xmlrpc.client.ServerProxy')
    def test_list_clients(self, mock_server):
        mock_server.return_value.list_clients.return_value = [(1, 'John Doe', 'john@example.com')]
        with patch('builtins.input', side_effect=['4', '7']), \
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(ExitException):
                main()
            mock_server.return_value.list_clients.assert_called_once()
            output = mock_stdout.getvalue()
            self.assertIn("Clientes:", output)

    @patch('xmlrpc.client.ServerProxy')
    def test_rent_vehicle(self, mock_server):
        mock_server.return_value.rent_vehicle.return_value = 1
        with patch('builtins.input', side_effect=['5', '1', '1', '2024-06-01', '2024-06-10', '7']), \
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(ExitException):
                main()
            mock_server.return_value.rent_vehicle.assert_called_with(1, 1, '2024-06-01', '2024-06-10')
            output = mock_stdout.getvalue()
            self.assertIn("Reserva de alquiler creada con ID: 1", output)

    @patch('xmlrpc.client.ServerProxy')
    def test_list_rentals(self, mock_server):
        mock_server.return_value.list_rentals.return_value = [
            {
                'id': 1,
                'vehicle_id': 1,
                'client_id': 1,
                'start_date': '2024-06-01',
                'end_date': '2024-06-10',
                'status': 'active'
            }
        ]
        with patch('builtins.input', side_effect=['6', '7']), \
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(ExitException):
                main()
            mock_server.return_value.list_rentals.assert_called_once()
            output = mock_stdout.getvalue()
            self.assertIn("Alquileres:", output)

    @patch('xmlrpc.client.ServerProxy')
    def test_exit(self, mock_server):
        with patch('builtins.input', side_effect=['7']), \
             patch('sys.stdout', new_callable=io.StringIO):
            with self.assertRaises(ExitException):
                main()

if __name__ == '__main__':
    unittest.main()





