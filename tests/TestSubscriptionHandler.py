import unittest
from unittest.mock import AsyncMock
from openUa import SubscriptionHandler
import os
from asyncua import Node

class TestSubscriptionHandler(unittest.TestCase):

    async def setUp(self):
        self.mock_camera_handler = AsyncMock()
        self.handler = SubscriptionHandler(self.mock_camera_handler, AsyncMock())

    async def test_jobfile_change_creates_directories(self):
        val = "/path/to/new_job_file.job"
        self.handler.JobFile_change(val)

        self.assertEqual(self.handler.Job_File, "new_job_file.job")
        self.assertTrue(os.path.exists(self.handler.OutputPath))
        self.assertTrue(os.path.exists(self.handler.Powder_OutputPath))
        self.assertTrue(os.path.exists(self.handler.Layer_OutputPath))

    async def test_layer_change_updates_layer_value(self):
        self.handler.layer_change(42)
        self.assertEqual(self.handler.layer, 42)

    async def test_status_change_stops_cameras_on_status_7(self):
        self.handler.status_change(7)
        self.mock_camera_handler.stop_cameras.assert_called_once()

    async def test_status_change_ignores_repeated_status_7(self):
        self.handler.previous_status = 7
        self.handler.status_change(7)
        self.mock_camera_handler.stop_cameras.assert_not_called()

    async def test_command_change_starts_cameras_on_value_3(self):
        self.handler.command_change(3)
        self.mock_camera_handler.start_cameras.assert_called_once()

    async def test_datachange_notification_triggers_layer_change(self):
        mock_node = AsyncMock()
        mock_node.__str__ = AsyncMock(return_value="current_layer")

        with unittest.mock.patch("openUA.subscription_handler.s.current_layer", "current_layer"):
            self.handler.datachange_notification(mock_node, 5, None)
            self.assertEqual(self.handler.layer, 5)

    async def test_datachange_notification_ignores_unknown_nodes(self):
        mock_node = AsyncMock()
        mock_node.__str__ = AsyncMock(return_value="unknown_node")

        with unittest.mock.patch("openUA.subscription_handler.s.current_layer", "current_layer"):
            self.handler.datachange_notification(mock_node, 999, None)
            self.assertNotEqual(self.handler.layer, 999)  # ensures no change


    async def test_job_file_change(mock_subscription_handler):
        mock_node = AsyncMock(spec=Node)
        mock_subscription_handler.datachange_notification(mock_node, "job1.csv", None)
        
        assert mock_subscription_handler.Job_File == "job1.csv"
        assert mock_subscription_handler.OutputPath.endswith("IMAGE_DIRECTORY/job1.csv")

    async def test_status_change(mock_subscription_handler):
        mock_subscription_handler.status_change(1)
        assert mock_subscription_handler.previous_status == 1

        mock_subscription_handler.status_change(7)
        assert mock_subscription_handler.previous_status == 7
        mock_subscription_handler.camera_handler.stop_cameras.assert_called_once()

if __name__ == "__main__":
    unittest.main()

