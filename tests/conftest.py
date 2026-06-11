import pytest
from pbi_core.state import reset_state


@pytest.fixture(autouse=True)
def clean_state():
    reset_state()
    yield
    reset_state()
