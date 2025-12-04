from src.core.models import DayPlan, Highlight, RawContent, Route, ScriptSegment


def test_script_segment_defaults_are_independent():
    first = ScriptSegment(text="Hello", order=1)
    second = ScriptSegment(text="World", order=2)

    assert first.text == "Hello"
    assert second.text == "World"
    assert first.order == 1
    assert second.order == 2


def test_route_structure():
    segment = ScriptSegment(text="Intro", order=1, speaker="Host")
    highlight = Highlight(description="Sunset view", order=1)
    day = DayPlan(day_index=1, title="Arrival", segments=[segment], highlights=[highlight])
    route = Route(name="Sample Trip", days=[day], source_text="raw")

    assert route.name == "Sample Trip"
    assert route.days[0].title == "Arrival"
    assert route.days[0].segments[0].text == "Intro"
    assert route.days[0].highlights[0].description == "Sunset view"


def test_raw_content_keeps_text_and_path(tmp_path):
    file_path = tmp_path / "content.md"
    file_path.write_text("sample text", encoding="utf-8")

    content = RawContent(path=str(file_path), text=file_path.read_text(encoding="utf-8"))

    assert content.path == str(file_path)
    assert content.text == "sample text"
