import unittest
from unittest.mock import MagicMock
from domain.models import Cpu
from monitor import MonitorTask
from cpu_service import CpuService

class TestCpuService(unittest.TestCase):

    def test_get_cpu(self):
        # Crée un objet MonitorTask fictif pour les tests
        mock_monitor_task = MagicMock()
        # Définis les valeurs de cpu_percent pour le mock
        mock_monitor_task.cpu_percent = [10.5, 25.3, 50.0]  # Exemple de valeurs

        # Initialise une instance de CpuService
        cpu_service = CpuService()

        # Appelle la méthode get_cpu avec le mock MonitorTask
        cpu_list = cpu_service.get_cpu(mock_monitor_task)

        # Vérifie que la méthode retourne une liste de Cpu
        self.assertIsInstance(cpu_list, list)
        self.assertTrue(all(isinstance(cpu, Cpu) for cpu in cpu_list))

        # Vérifie que la liste retournée correspond aux valeurs attendues
        expected_cpu_list = [
            Cpu(id=0, usage='10.5'),
            Cpu(id=1, usage='25.3'),
            Cpu(id=2, usage='50.0')
        ]
        self.assertEqual(cpu_list, expected_cpu_list)

if __name__ == '__main__':
    unittest.main()
