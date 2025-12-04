from src.core.pipeline import build_route_from_text


def test_build_route_with_day_headings():
    text = """
    Day 1: Arrival
    Land and check-in.

    Evening walk.

    Day 2: City Tour
    Morning coffee stop.

    Museum visit.
    """

    route = build_route_from_text(text)

    assert len(route.days) == 2
    assert route.days[0].day_index == 1
    assert route.days[0].title == "Arrival"
    assert [segment.text for segment in route.days[0].segments] == ["Land and check-in.", "Evening walk."]
    assert route.days[1].day_index == 2
    assert route.days[1].title == "City Tour"
    assert route.days[1].segments[0].order == 1


def test_build_route_without_headings():
    text = """
    Welcome to the trip.

    We explore the old town.
    """

    route = build_route_from_text(text)

    assert len(route.days) == 1
    assert route.days[0].day_index == 1
    assert [segment.text for segment in route.days[0].segments] == ["Welcome to the trip.", "We explore the old town."]
