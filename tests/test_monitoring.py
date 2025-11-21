import pytest
from unittest.mock import MagicMock, patch
from src.monitoring.metrics import MetricsManager

@pytest.fixture
def metrics_manager():
    return MetricsManager()

def test_singleton_pattern():
    m1 = MetricsManager()
    m2 = MetricsManager()
    assert m1 is m2

def test_log_request(metrics_manager):
    with patch('src.monitoring.metrics.REQUEST_COUNT') as mock_count:
        with patch('src.monitoring.metrics.REQUEST_LATENCY') as mock_latency:
            metrics_manager.log_request("GET", "/api", 200, 0.1)
            
            mock_count.labels.assert_called_with(method="GET", endpoint="/api", status=200)
            mock_count.labels.return_value.inc.assert_called_once()
            
            mock_latency.labels.assert_called_with(method="GET", endpoint="/api")
            mock_latency.labels.return_value.observe.assert_called_with(0.1)

def test_log_workflow(metrics_manager):
    with patch('src.monitoring.metrics.WORKFLOW_COUNT') as mock_count:
        metrics_manager.log_workflow("TEST_TYPE", "COMPLETED")
        
        mock_count.labels.assert_called_with(type="TEST_TYPE", status="COMPLETED")
        mock_count.labels.return_value.inc.assert_called_once()

def test_start_server_error(metrics_manager):
    # Test error handling when starting server fails
    with patch('src.monitoring.metrics.start_http_server', side_effect=Exception("Port in use")):
        metrics_manager.logger = MagicMock()
        metrics_manager.start_server(8000)
        metrics_manager.logger.error.assert_called()
