import unittest
from unittest.mock import patch, MagicMock
from app.services.openmrs_service import OpenMRSService

class TestOpenMRSService(unittest.TestCase):
    def setUp(self):
        self.openmrs_service = OpenMRSService()

    @patch('app.services.openmrs_service.requests.Session')
    def test_get_patient_data(self, mock_session):
        # Mock the session and its get method
        mock_get = MagicMock()
        mock_session.return_value.get = mock_get

        # Mock responses for different API calls
        mock_responses = {
            f"{self.openmrs_service.base_url}/patient/test_uuid": MagicMock(
                status_code=200,
                json=lambda: {"person": {"birthdate": "1990-01-01", "gender": "M", "ethnicity": "Caucasian"}}
            ),
            f"{self.openmrs_service.base_url}/obs?patient=test_uuid&concept=Vital Signs": MagicMock(
                status_code=200,
                json=lambda: {"results": []}
            ),
            f"{self.openmrs_service.base_url}/condition?patient=test_uuid": MagicMock(
                status_code=200,
                json=lambda: {"results": []}
            ),
            f"{self.openmrs_service.base_url}/medicationrequest?patient=test_uuid": MagicMock(
                status_code=200,
                json=lambda: {"results": []}
            ),
            f"{self.openmrs_service.base_url}/allergyintolerance?patient=test_uuid": MagicMock(
                status_code=200,
                json=lambda: {"results": []}
            ),
            f"{self.openmrs_service.base_url}/diagnosticreport?patient=test_uuid": MagicMock(
                status_code=200,
                json=lambda: {"results": []}
            ),
            f"{self.openmrs_service.base_url}/careplan?patient=test_uuid": MagicMock(
                status_code=200,
                json=lambda: {"results": []}
            ),
            f"{self.openmrs_service.base_url}/observation?patient=test_uuid&category=social-history": MagicMock(
                status_code=200,
                json=lambda: {"results": []}
            ),
            f"{self.openmrs_service.base_url}/encounter?patient=test_uuid": MagicMock(
                status_code=200,
                json=lambda: {"results": []}
            ),
            f"{self.openmrs_service.base_url}/familymemberhistory?patient=test_uuid": MagicMock(
                status_code=200,
                json=lambda: {"results": []}
            ),
        }

        def side_effect(url, *args, **kwargs):
            return mock_responses.get(url, MagicMock(status_code=404))

        mock_get.side_effect = side_effect

        # Call the method
        patient_data = self.openmrs_service.get_patient_data("test_uuid")

        # Assert the result
        self.assertIsNotNone(patient_data)
        self.assertIn('demographics', patient_data)
        self.assertEqual(patient_data['demographics']['age'], 33)  # Assuming current year is 2023
        self.assertEqual(patient_data['demographics']['gender'], 'M')
        self.assertEqual(patient_data['demographics']['ethnicity'], 'Caucasian')

        # Assert that all expected API calls were made
        expected_calls = list(mock_responses.keys())
        actual_calls = [call.args[0] for call in mock_get.call_args_list]
        self.assertEqual(set(expected_calls), set(actual_calls))

    # Add more tests for other methods in OpenMRSService

if __name__ == '__main__':
    unittest.main()
