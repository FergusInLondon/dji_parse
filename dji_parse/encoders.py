import csv
from datetime import datetime
import enum
import dataclasses
import json
from typing import List, IO, Type

from .parsing import Position

import gpxpy


class EncoderType(enum.Enum):
    CSV = "csv"
    GPX = "gpx"
    JSON = "json"


class BaseEncoder:
    def __init__(self, output: IO, entries: List[Position] = []):
        self.output = output
        self.entries = entries

    def add(self, obs: Position):
        self.entries.append(obs)

    def write(self):
        if len(self.entries) < 1:
            return

        self._write()

    def _write(self):
        raise NotImplementedError("please use a valid output encoder")


class CSVEncoder(BaseEncoder):
    def _write(self):
        w = csv.DictWriter(
            self.output, fieldnames=list(dataclasses.asdict(self.entries[0]).keys())
        )

        w.writeheader()
        for pos in self.entries:
            w.writerow(dataclasses.asdict(pos))


class GPXEncoder(BaseEncoder):
    def _write(self):
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        for pos in self.entries:
            gpx_segment.points.append(
                gpxpy.gpx.GPXTrackPoint(
                    pos.latitude,
                    pos.longitude,
                    time=datetime.fromisoformat(pos.time),
                    elevation=pos.rel_elevation,
                )
            )

        gpx = gpxpy.gpx.GPX()
        gpx_track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(gpx_track)
        gpx_track.segments.append(gpx_segment)

        self.output.write(gpx.to_xml())


class JSONEncoder(BaseEncoder):
    def _write(self):
        json.dump([dataclasses.asdict(pos) for pos in self.entries], self.output)


_TYPE_CSV_OUTPUT = "csv"
_TYPE_GPX_OUTPUT = "gpx"
_TYPE_JSON_OUTPUT = "json"


def get_encoder(output_type: EncoderType) -> Type[BaseEncoder]:
    try:
        return {
            EncoderType.CSV.value: CSVEncoder,
            EncoderType.GPX.value: GPXEncoder,
            EncoderType.JSON.value: JSONEncoder,
        }[output_type.value]
    except KeyError:
        raise Exception(f"invalid output type specified - '{output_type}")
