from unittest.mock import Mock

from app.engine.ping import PingEngine


def test_ping_engine_calls_router():
    mock_router = Mock()

    mock_router.execute.return_value = """
    SEQ HOST SIZE TTL TIME STATUS
    0 8.8.8.8 56 117 3ms
    """

    ping = PingEngine(mock_router)

    ping.measure(
        destination="8.8.8.8",
        count=5,
    )

    mock_router.execute.assert_called_once()