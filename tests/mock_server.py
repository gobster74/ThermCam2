from unittest.mock import AsyncMock, MagicMock
from asyncua import Node

class MockServer:
    def __init__(self):
        self.mock_client = AsyncMock()
        self.mock_client.get_node.side_effect = self.get_mock_node

    def get_mock_node(self, node_id):
        mock_node = MagicMock(spec=Node)
        mock_node.read_value = AsyncMock(return_value=0) 
        return mock_node

mock_server = MockServer()
