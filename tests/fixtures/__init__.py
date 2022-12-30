from datetime import datetime, timedelta

from dji_parse.parsing import Position


def _add_seconds(secs: int) -> datetime:
    return TEST_DATETIME + timedelta(seconds=secs)


TEST_DATETIME = datetime(2022, 12, 25)


SUBTITLES_FILE = "tests/fixtures/test.data.srt"


EXPECTED_POSITIONS = [
    Position(
        time=_add_seconds(1).isoformat(),
        timestamp="00:00:01",
        latitude=52.3734,
        longitude=0.2054,
        distance=5.9,
        rel_elevation=20.0,
        horizontal_velocity=0.0,
        vertical_velocity=0.0,
    ),
    Position(
        time=_add_seconds(2).isoformat(),
        timestamp="00:00:02",
        latitude=52.3734,
        longitude=0.2054,
        distance=5.9,
        rel_elevation=20.1,
        horizontal_velocity=0.0,
        vertical_velocity=0.1,
    ),
    Position(
        time=_add_seconds(3).isoformat(),
        timestamp="00:00:03",
        latitude=52.3734,
        longitude=0.2051,
        distance=5.74,
        rel_elevation=20.4,
        horizontal_velocity=0.0,
        vertical_velocity=0.0,
    ),
    Position(
        time=_add_seconds(4).isoformat(),
        timestamp="00:00:04",
        latitude=52.3734,
        longitude=0.2052,
        distance=5.73,
        rel_elevation=19.9,
        horizontal_velocity=0.28,
        vertical_velocity=-0.2,
    ),
    Position(
        time=_add_seconds(5).isoformat(),
        timestamp="00:00:05",
        latitude=52.3734,
        longitude=0.2056,
        distance=5.73,
        rel_elevation=19.7,
        horizontal_velocity=0.0,
        vertical_velocity=0.2,
    ),
]
