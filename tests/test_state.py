from pbi_core.state import get_state, reset_state, McpState

def test_initial_state_is_empty():
    reset_state()
    s = get_state()
    assert s.session is None
    assert s.report_path is None

def test_state_mutation_persists():
    reset_state()
    s = get_state()
    s.session = "mock_session"
    s.report_path = "C:/test.pbip"
    s2 = get_state()
    assert s2.session == "mock_session"
    assert s2.report_path == "C:/test.pbip"

def test_reset_clears_state():
    s = get_state()
    s.session = "mock_session"
    reset_state()
    assert get_state().session is None
