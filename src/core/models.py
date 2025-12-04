from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RawContent:
    """Container for raw input text before parsing."""

    path: str
    text: str


@dataclass
class ScriptSegment:
    """Smallest unit of a script, representing a paragraph or beat."""

    text: str
    order: Optional[int] = None
    speaker: Optional[str] = None
    notes: Optional[str] = None


@dataclass
class Highlight:
    """Notable moment to emphasize in a video cut or thumbnail."""

    description: str
    order: Optional[int] = None
    segment_order: Optional[int] = None


@dataclass
class DayPlan:
    """A day in the route containing a sequence of script segments."""

    day_index: int
    title: Optional[str] = None
    segments: list[ScriptSegment] = field(default_factory=list)
    highlights: list[Highlight] = field(default_factory=list)


@dataclass
class Route:
    """Structured itinerary script for a full tour video."""

    name: Optional[str] = None
    days: list[DayPlan] = field(default_factory=list)
    source_text: Optional[str] = None
