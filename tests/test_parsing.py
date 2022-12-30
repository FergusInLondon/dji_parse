import dataclasses

import pysrt

from tests import fixtures
from dji_parse import parsing


class TestingParsing:

    @staticmethod
    def _verify_dataclass(expected: dataclasses.dataclass, actual: dataclasses.dataclass):
        expected_dict = dataclasses.asdict(expected)
        actual_dict = dataclasses.asdict(actual)

        for k in list(expected_dict.keys()):
            assert expected_dict[k] == actual_dict[k]

    def test_metadata_from_ffmpeg_probe(self):
        metadata = parsing.parse_metadata_from_probe({
            "format": {
                "duration": "23.3",
                "tags": {
                    "creation_time": fixtures.TEST_DATETIME.isoformat(),
                    "location": "England, UK"
                }
            }
        })

        self._verify_dataclass(parsing.Metadata(
            creation_time=fixtures.TEST_DATETIME,
            duration=23.3,
            location="England, UK"
        ), metadata)

    def test_position_from_subtitle(self):
        subs = pysrt.open(fixtures.SUBTITLES_FILE)
        assert len(subs) == len(fixtures.EXPECTED_POSITIONS)

        for i in range(len(subs)):
            self._verify_dataclass(
                fixtures.EXPECTED_POSITIONS[i],
                parsing.position_from_subtitle(fixtures.TEST_DATETIME, subs[i])
            )
