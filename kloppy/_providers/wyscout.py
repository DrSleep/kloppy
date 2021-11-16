from kloppy.infra.serializers.event.wyscout import (
    WyscoutDeserializer,
    WyscoutInputs,
)
from kloppy.domain import EventDataset, Optional, List
from kloppy.io import open_as_file, FileLike


def load(
    event_data: FileLike,
    event_types: Optional[List[str]] = None,
    coordinates: Optional[str] = None,
) -> EventDataset:
    """
    Load Wyscout event data into a [`EventDataset`][kloppy.domain.models.event.EventDataset]

    Parameters:
        event_data: filename of the XML file containing the events and metadata
        event_types:
        coordinates:
    """
    deserializer = WyscoutDeserializer(
        event_types=event_types, coordinate_system=coordinates
    )
    with open_as_file(event_data) as event_data_fp:
        return deserializer.deserialize(
            inputs=WyscoutInputs(event_data=event_data_fp),
        )
