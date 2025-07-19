from . import _logic
from .. import csg


def convert(splits: list[bytes]) -> list[bytes]:
    results = []
    for data in splits:
        result = csg.parse(data)
        if not result:
            result = data
        results.append(result)
    return results


def replace(parser: _logic.rbxl_parser, chunk_data: _logic.chunk_data_type) -> _logic.chunk_data_type | None:
    if isinstance(chunk_data, _logic.chunk_data_type_sstr):
        chunk_data.strings = convert(chunk_data.strings)
        return chunk_data

    elif isinstance(chunk_data, _logic.chunk_data_type_prop):
        if not chunk_data.prop_name.startswith(b'MeshData'):
            return

        if chunk_data.prop_type != 0x1C:
            return

        splits = _logic.split_prop_strings(chunk_data.prop_values)
        fixed_splits = convert(splits)
        chunk_data.prop_values = _logic.join_prop_strings(fixed_splits)

        return chunk_data
