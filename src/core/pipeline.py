from __future__ import annotations

import re
import textwrap
from typing import Iterable

from .models import DayPlan, Route, ScriptSegment


DAY_HEADING_PATTERN = re.compile(r"(?im)^day\s+(\d+)(.*)$")


def _split_on_blank_lines(text: str) -> list[str]:
    sections = [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]
    return sections


def _iter_day_sections(text: str) -> Iterable[tuple[int, str, str]]:
    matches = list(DAY_HEADING_PATTERN.finditer(text))
    if not matches:
        yield (1, "", text)
        return

    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        day_text = text[start:end].strip()
        day_number = int(match.group(1))
        title = match.group(2).lstrip(":：-").strip()
        yield (day_number, title, day_text)


def build_route_from_text(text: str) -> Route:
    """Parse raw itinerary text into a structured :class:`Route` instance.

    The current implementation uses simple heuristics:
    - Detect day headings in the form of "Day X" (case-insensitive).
    - If no headings are found, the entire text is treated as a single day.
    - Within each day, content is split into script segments by blank lines.
    """

    normalized = textwrap.dedent(text).strip()

    days: list[DayPlan] = []
    for day_index, title, body in _iter_day_sections(normalized):
        segments_text = _split_on_blank_lines(body)
        segments = [ScriptSegment(text=segment, order=i + 1) for i, segment in enumerate(segments_text)]
        days.append(DayPlan(day_index=day_index, title=title or None, segments=segments))

    return Route(days=days, source_text=text)
