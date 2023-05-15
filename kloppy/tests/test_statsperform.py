import pytest
import os

from kloppy.domain import (
    AttackingDirection,
    Orientation,
    Provider,
    Point,
    Point3D,
    DatasetType,
)

from kloppy import statsperform


class TestStatsperformTracking:
    @pytest.fixture
    def meta_data(self) -> str:
        base_dir = os.path.dirname(__file__)
        return f"{base_dir}/files/statsperform_MA1_metadata.xml"

    @pytest.fixture
    def raw_data(self) -> str:
        base_dir = os.path.dirname(__file__)
        return f"{base_dir}/files/statsperform_MA25_tracking.txt"

    def test_correct_deserialization(self, meta_data: str, raw_data: str):
        dataset = statsperform.load(
            meta_data=meta_data,
            raw_data=raw_data,
            only_alive=False,
            coordinates="statsperform",
        )

        # Check provider, type, shape, etc
        assert dataset.metadata.provider == Provider.STATSPERFORM
        assert dataset.dataset_type == DatasetType.TRACKING
        assert len(dataset.records) == 92
        assert len(dataset.metadata.periods) == 2
        assert dataset.metadata.orientation == Orientation.FIXED_HOME_AWAY

        # Check the Periods
        assert dataset.metadata.periods[0].id == 1
        assert dataset.metadata.periods[0].start_timestamp == 0
        assert dataset.metadata.periods[0].end_timestamp == 2500
        assert (
            dataset.metadata.periods[0].attacking_direction
            == AttackingDirection.HOME_AWAY
        )

        assert dataset.metadata.periods[1].id == 2
        assert dataset.metadata.periods[1].start_timestamp == 0
        assert dataset.metadata.periods[1].end_timestamp == 6500
        assert (
            dataset.metadata.periods[1].attacking_direction
            == AttackingDirection.HOME_AWAY
        )

        # Check some timestamps
        assert dataset.records[0].timestamp == 0  # First frame
        assert dataset.records[20].timestamp == 2.0  # Later frame

        # Check some players
        home_player = dataset.metadata.teams[0].players[2]
        assert home_player.player_id == "5g5wwp5luxo1rz1kp6chvz0x6"
        assert dataset.records[0].players_coordinates[home_player] == Point(
            x=68.689, y=39.75
        )

        away_player = dataset.metadata.teams[1].players[3]
        assert away_player.player_id == "72d5uxwcmvhd6mzthxuvev1sl"
        assert dataset.records[0].players_coordinates[away_player] == Point(
            x=30.595, y=44.022
        )

        # Check the ball
        assert dataset.records[1].ball_coordinates == Point3D(
            x=50.615, y=35.325, z=0.0
        )

        # Check pitch dimensions
        pitch_dimensions = dataset.metadata.pitch_dimensions
        assert pitch_dimensions.x_dim.min == 0
        assert pitch_dimensions.x_dim.max == 100
        assert pitch_dimensions.y_dim.min == 0
        assert pitch_dimensions.y_dim.max == 100

    def test_correct_normalized_deserialization(
        self, meta_data: str, raw_data: str
    ):
        dataset = statsperform.load(
            meta_data=meta_data,
            raw_data=raw_data,
            only_alive=False,
        )

        home_player = dataset.metadata.teams[0].players[2]
        assert dataset.records[0].players_coordinates[home_player] == Point(
            x=0.6868899999999999, y=0.6025
        )

        # Check normalised pitch dimensions
        pitch_dimensions = dataset.metadata.pitch_dimensions
        assert pitch_dimensions.x_dim.min == 0.0
        assert pitch_dimensions.x_dim.max == 1.0
        assert pitch_dimensions.y_dim.min == 0.0
        assert pitch_dimensions.y_dim.max == 1.0
