import logging
import os

from kloppy import SecondSpectrumSerializer
from kloppy.domain import (
    Period,
    AttackingDirection,
    Orientation,
    Provider,
    Point,
    Point3D,
    BallState,
    Team,
    Ground,
)
from kloppy.domain.models.common import DatasetType


class TestSecondSpectrumTracking:
    def test_correct_deserialization(self):
        base_dir = os.path.dirname(__file__)
        serializer = SecondSpectrumSerializer()

        xml_mdfloc = f"{base_dir}/files/second_spectrum_fake_metadata.xml"
        json_mdfloc = f"{base_dir}/files/second_spectrum_fake_metadata.jsonl"
        rawfloc = f"{base_dir}/files/second_spectrum_fake_data.jsonl"

        with open(xml_mdfloc, "rb") as metadata, open(
            json_mdfloc, "rb"
        ) as json_metadata, open(rawfloc, "rb") as raw_data:

            dataset = serializer.deserialize(
                inputs={
                    "xml_metadata": metadata,
                    "raw_data": raw_data,
                    "json_metadata": json_metadata,
                },
                options={
                    "only_alive": False,
                    "coordinate_system": Provider.SECONDSPECTRUM,
                },
            )

        # Check provider, type, shape, etc
        assert dataset.metadata.provider == Provider.SECONDSPECTRUM
        assert dataset.dataset_type == DatasetType.TRACKING
        assert len(dataset.records) == 376
        assert len(dataset.metadata.periods) == 2
        assert dataset.metadata.orientation == Orientation.FIXED_AWAY_HOME

        # Check the Periods
        assert dataset.metadata.periods[0].id == 1
        assert dataset.metadata.periods[0].start_timestamp == 0
        assert dataset.metadata.periods[0].end_timestamp == 2982240
        assert (
            dataset.metadata.periods[0].attacking_direction
            == AttackingDirection.AWAY_HOME
        )

        assert dataset.metadata.periods[1].id == 2
        assert dataset.metadata.periods[1].start_timestamp == 3907360
        assert dataset.metadata.periods[1].end_timestamp == 6927840
        assert (
            dataset.metadata.periods[1].attacking_direction
            == AttackingDirection.HOME_AWAY
        )

        # Check some timestamps
        assert dataset.records[0].timestamp == 0  # First frame
        assert dataset.records[20].timestamp == 320.0  # Later frame

        # Check some players
        home_player = dataset.metadata.teams[0].players[2]
        assert home_player.player_id == "8xwx2"
        assert dataset.records[0].players_coordinates[home_player] == Point(
            x=-8.943903672572427, y=-28.171654132650364
        )

        away_player = dataset.metadata.teams[1].players[3]
        assert away_player.player_id == "2q0uv"
        assert dataset.records[0].players_coordinates[away_player] == Point(
            x=-45.11871334915762, y=-20.06459030559596
        )

        # Check the ball
        assert dataset.records[1].ball_coordinates == Point3D(
            x=-23.147073918432426, y=13.69367399756424, z=0.0
        )

        # Check pitch dimensions
        pitch_dimensions = dataset.metadata.pitch_dimensions
        assert pitch_dimensions.x_dim.min == -52.425
        assert pitch_dimensions.x_dim.max == 52.425
        assert pitch_dimensions.y_dim.min == -33.985
        assert pitch_dimensions.y_dim.max == 33.985

    def test_correct_normalized_deserialization(self):
        base_dir = os.path.dirname(__file__)
        serializer = SecondSpectrumSerializer()

        xml_mdfloc = f"{base_dir}/files/second_spectrum_fake_metadata.xml"
        json_mdfloc = f"{base_dir}/files/second_spectrum_fake_metadata.jsonl"
        rawfloc = f"{base_dir}/files/second_spectrum_fake_data.jsonl"

        with open(xml_mdfloc, "rb") as metadata, open(
            json_mdfloc, "rb"
        ) as json_metadata, open(rawfloc, "rb") as raw_data:

            dataset = serializer.deserialize(
                inputs={
                    "xml_metadata": metadata,
                    "raw_data": raw_data,
                    "json_metadata": json_metadata,
                },
                options={
                    "only_alive": False,
                },
            )

        home_player = dataset.metadata.teams[0].players[2]
        assert dataset.records[0].players_coordinates[home_player] == Point(
            x=0.4146981051733674, y=0.9144718866065965
        )

        # Check normalised pitch dimensions
        pitch_dimensions = dataset.metadata.pitch_dimensions
        assert pitch_dimensions.x_dim.min == 0.0
        assert pitch_dimensions.x_dim.max == 1.0
        assert pitch_dimensions.y_dim.min == 0.0
        assert pitch_dimensions.y_dim.max == 1.0
