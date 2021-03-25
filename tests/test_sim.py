from src.simulator import FEL

def test_FEL():
    event_list = FEL()
    assert len(event_list) == 0

    event_list.append(5)
    assert event_list[0] == 5