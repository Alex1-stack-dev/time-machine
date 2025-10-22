import pytest
from unittest.mock import Mock, patch
from timer import TimerPanel
from protocol import TimeMachineG2Protocol

class TestTimerPanel:
    @pytest.fixture
    def timer_panel(self):
        return TimerPanel()
    
    def test_timer_initialization(self, timer_panel):
        assert timer_panel.current_time == "00:00.00"
        assert not timer_panel.is_running
    
    @patch('serial.Serial')
    def test_serial_connection(self, mock_serial, timer_panel):
        timer_panel.handle_connect()
        assert mock_serial.called
    
    def test_protocol_parsing(self, timer_panel):
        protocol = TimeMachineG2Protocol()
        result = protocol.parse_response("TIME:01:23.45")
        assert result["type"] == "time"
        assert result["value"] == "01:23.45"
