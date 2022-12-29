import pathlib
from time import perf_counter
from typing import IO

import dji_parse.console
from dji_parse.parsing import video_metadata, parse_subtitles, position_from_subtitle
from dji_parse.encoders import get_encoder, EncoderType

import click


class Timer:
    def __enter__(self):
        self.duration = None
        self.begin = perf_counter()
        return self

    def __exit__(self, t, v, tb):
        self.duration = perf_counter() - self.begin


@click.command()
@click.argument(
    "input_video", type=click.Path(exists=True, readable=True, path_type=pathlib.Path)
)
@click.argument("output", type=click.File("w"))
@click.option(
    "--output-format",
    type=click.Choice(["csv", "gpx", "json"], case_sensitive=False),
    default="gpx",
)
def run(input_video: pathlib.Path, output: IO, output_format: str = "gpx"):
    """Parse INPUT_VIDEO file for embedded DJI telemetry, writing data to OUTPUT.

    Supports writing telemetry data in either CSV, JSON, or GPX format. Defaults to GPX.
    """
    try:
        encoder = get_encoder(EncoderType(output_format))
    except ValueError:
        console.result(message="please select a valid output format", is_success=False)
        exit(-1)

    with Timer() as t:
        metadata = video_metadata(input_video)
        console.print(f"- have input video created on {metadata.creation_time}")

        with console.busy("parsing subtitles from video..."):
            subs = parse_subtitles(input_video)

        console.print(f"- parsed [bold]{len(subs)}[/bold] datapoints")

        with console.busy("writing telemetry to output file..."):
            encoder(
                output,
                entries=[
                    position_from_subtitle(metadata.creation_time, s) for s in subs
                ],
            ).write()

        console.print(
            f"- wrote [bold]{len(subs)}[/bold] datapoints to telemetry output file"
        )

    console.result(
        message="Finished processing DJI telemetry from recording.",
        rows={
            "Input File": str(input_video.name),
            "Recording Duration": "{:.2f} seconds".format(metadata.duration),
            "Recording Creation Date": metadata.creation_time.isoformat(),
            "Output Telemetry File": output.name,
            "Output Telemetry Format": output_format,
            "Number of Observations": f"{len(subs)} datapoints",
            "Processing Duration": "{:.2f} seconds".format(t.duration),
        },
    )


if __name__ == "__main__":
    run()
