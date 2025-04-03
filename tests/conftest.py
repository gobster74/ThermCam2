import pytest
from unittest.mock import AsyncMock, MagicMock
from openUa import SubscriptionHandler
from tests.mock_server import mock_server

@pytest.fixture
def mock_camera_handler():
    return MagicMock()

@pytest.fixture
def mock_subscription_handler(mock_camera_handler):
    return SubscriptionHandler(mock_camera_handler, mock_server.mock_client)
