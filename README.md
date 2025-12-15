# cggtts

Python bindings for the cggtts Rust library (BIPM CGGTTS 2E parser)

## Overview

This package provides Python bindings for the cggtts Rust library, enabling parsing of BIPM CGGTTS 2E format files. CGGTTS (Common-View satellite/GNSS Time-Transfer Format) is a standard format used for precise time transfer between atomic clocks using GNSS satellites.

The original Rust library can be found at: [https://github.com/nav-solutions/cggtts](https://github.com/nav-solutions/cggtts)

## Features

- Parse CGGTTS 2E format files
- Extract complete track information (satellite, epoch, duration, elevation, azimuth, etc.)
- Access to header information (station, version, receiver info, coordinates)
- System delay information
- Support for multiple satellite constellations (GPS, Galileo, Beidou, GLONASS, QZSS, IRNSS, SBAS)
- Ionospheric data support

## Installation

```bash
pip install cggtts
```

## Usage

```python
import cggtts

# Parse a CGGTTS file
result = cggtts.parse_cggtts('path/to/your/file.cggtts')

# Access basic information
print(f"Station: {result['station']}")
print(f"Version: {result['version']}")
print(f"Number of tracks: {result['tracks_count']}")

# Access track information
for track in result['tracks']:
    print(f"Satellite: {track['satellite']}")
    print(f"Epoch: {track['epoch']}")
    print(f"Elevation: {track['elevation_deg']} degrees")
    # ... access other track data
```

## Development

To set up the development environment:

```bash
# Clone the repository
git clone <repository-url>
cd cggtts

# Create virtual environment
make init-venv

# Build and install in development mode
make dev

# Run tests
make test
```

## API

### `parse_cggtts(path: str) -> dict`

Parse a CGGTTS file and return its contents as a dictionary.

**Parameters:**
- `path` (str): Path to the CGGTTS file to parse

**Returns:**
A dictionary containing:
- `station` (str): Station identifier
- `version` (str): CGGTTS format version
- `revision_date` (str): Revision date in ISO format
- `nb_channels` (int): Number of channels
- `reference_time` (str): Reference time
- `reference_frame` (str): Reference frame
- `receiver` (dict): Receiver information (manufacturer, model, serial number, etc.)
- `apc_coordinates` (dict): APC coordinates (x, y, z)
- `delay` (dict): Delay information (antenna cable delay, local ref delay, etc.)
- `ims_hardware` (dict, optional): IMS hardware information
- `tracks_count` (int): Total number of tracks
- `has_ionospheric_data` (bool): Whether ionospheric data is present
- `common_view_class` (str): Common view class
- `follows_bipm_tracking` (bool): Whether it follows BIPM tracking
- `is_gps`, `is_galileo`, `is_beidou`, etc. (bool): Constellation detection flags
- `tracks` (list): List of track dictionaries containing all track information
- `total_duration_seconds` (float, optional): Total duration in seconds
- `first_epoch`, `last_epoch` (str, optional): First and last epochs in ISO format

## License

This project is licensed under the Mozilla Public License 2.0 (MPL-2.0).