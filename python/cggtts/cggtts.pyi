from typing import Any

def parse_cggtts(path: str) -> dict[str, Any]:
    """
    Parse a CGGTTS file and return its contents as a dictionary.

    Args:
        path: Path to the CGGTTS file to parse

    Returns:
        A dictionary containing the parsed CGGTTS data with the following structure:
        {
            'station': str,
            'version': str,
            'revision_date': str,
            'nb_channels': int,
            'reference_time': str,
            'reference_frame': str,
            'receiver': {
                'manufacturer': str,
                'model': str,
                'serial_number': str,
                'year': int,
                'release': str
            },
            'apc_coordinates': {
                'x': float,
                'y': float,
                'z': float
            },
            'comments': str | None,
            'delay': {
                'antenna_cable_delay': float,
                'local_ref_delay': float,
                'total_cable_delay_nanos': float,
                'calibration_id': dict[str, str | int] | None
            },
            'ims_hardware': dict[str, str | int] | None,
            'tracks_count': int,
            'has_ionospheric_data': bool,
            'common_view_class': str,
            'follows_bipm_tracking': bool,
            'is_gps': bool,
            'is_galileo': bool,
            'is_beidou': bool,
            'is_glonass': bool,
            'is_qzss': bool,
            'is_irnss': bool,
            'is_sbas': bool,
            'tracks': list[dict[str, Any]],  # List of track data
            'total_duration_seconds': float | None,
            'first_epoch': str | None,
            'last_epoch': str | None
        }

    Raises:
        ValueError: If the file does not exist or if parsing fails
    """
    ...
