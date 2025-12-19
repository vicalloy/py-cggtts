import os
from typing import Any

import pytest

import cggtts


def test_parse_cggtts_basic() -> None:
    """Test basic functionality of parsing CGGTTS files"""
    # Use existing test data file from the project
    test_file = "cggtts/data/CGGTTS/GZGTR560.258"
    if os.path.exists(test_file):
        result: dict[str, Any] = cggtts.parse_cggtts(test_file)
        assert result is not None
        assert "station" in result
        assert "version" in result
        assert "tracks_count" in result
        print(f"Successfully parsed file: {test_file}")
        print(f"Station: {result['station']}")
        print(f"Version: {result['version']}")
        print(f"Number of tracks: {result['tracks_count']}")
    else:
        # Skip test if test data doesn't exist
        pytest.skip("Test data file does not exist")


def test_parse_cggtts_with_nonexistent_file() -> None:
    """Test error handling when parsing non-existent files"""
    with pytest.raises(ValueError):
        cggtts.parse_cggtts("nonexistent_file.cggtts")


def test_parse_cggtts_header_info() -> None:
    """Test parsing header information from CGGTTS files"""
    test_file = "cggtts/data/CGGTTS/GZGTR560.258"
    if os.path.exists(test_file):
        result: dict[str, Any] = cggtts.parse_cggtts(test_file)
        # Check key header fields
        assert "station" in result
        assert "version" in result
        assert "revision_date" in result
        assert "nb_channels" in result
        assert "receiver" in result
        assert "apc_coordinates" in result

        # Check receiver information
        receiver: dict[str, Any] = result["receiver"]
        assert "manufacturer" in receiver
        assert "model" in receiver
        assert "serial_number" in receiver

        # Check APC coordinates
        coords: dict[str, float] = result["apc_coordinates"]
        assert "x" in coords
        assert "y" in coords
        assert "z" in coords

        print("Header information parsing test passed")
    else:
        pytest.skip("Test data file does not exist")


def test_parse_cggtts_track_info() -> None:
    """Test parsing track information from CGGTTS files"""
    test_file = "cggtts/data/CGGTTS/GZGTR560.258"
    if os.path.exists(test_file):
        result: dict[str, Any] = cggtts.parse_cggtts(test_file)
        # Check track information
        assert "tracks_count" in result
        assert "tracks" in result  # Now using 'tracks' key instead of 'first_track'

        tracks: list = result["tracks"]
        assert len(tracks) > 0  # Ensure there is track data

        first_track: dict[str, Any] = tracks[0]  # Get the first track from the list
        assert "satellite" in first_track
        assert "epoch" in first_track
        assert "duration_seconds" in first_track
        assert "elevation_deg" in first_track
        assert "azimuth_deg" in first_track

        # Check track data
        assert "data" in first_track
        track_data: dict[str, Any] = first_track["data"]
        assert "refsv" in track_data
        assert "srsv" in track_data
        assert "refsys" in track_data
        assert "srsys" in track_data
        assert "dsg" in track_data

        print("Track information parsing test passed")
    else:
        pytest.skip("Test data file does not exist")


def test_parse_cggtts_constellation_info() -> None:
    """Test parsing constellation information from CGGTTS files"""
    test_file = "cggtts/data/CGGTTS/GZGTR560.258"
    if os.path.exists(test_file):
        result: dict[str, Any] = cggtts.parse_cggtts(test_file)
        # Check constellation information
        assert "is_gps" in result
        assert "is_galileo" in result
        assert "is_beidou" in result
        assert "is_glonass" in result
        assert "is_qzss" in result
        assert "is_irnss" in result
        assert "is_sbas" in result

        print("Constellation information parsing test passed")
    else:
        pytest.skip("Test data file does not exist")


def test_parse_cggtts_system_delay() -> None:
    """Test parsing system delay information from CGGTTS files"""
    test_file = "cggtts/data/CGGTTS/GZGTR560.258"
    if os.path.exists(test_file):
        result: dict[str, Any] = cggtts.parse_cggtts(test_file)
        # Check system delay information
        assert "delay" in result
        delay_info: dict[str, Any] = result["delay"]
        assert "antenna_cable_delay" in delay_info
        assert "local_ref_delay" in delay_info
        assert "total_cable_delay_nanos" in delay_info

        print("System delay information parsing test passed")
    else:
        pytest.skip("Test data file does not exist")


if __name__ == "__main__":
    # Execute tests if running this file directly
    test_file = "cggtts/data/CGGTTS/GZGTR560.258"
    if os.path.exists(test_file):
        print("Running basic parsing test...")
        test_parse_cggtts_basic()

        print("Running header information test...")
        test_parse_cggtts_header_info()

        print("Running track information test...")
        test_parse_cggtts_track_info()

        print("Running constellation information test...")
        test_parse_cggtts_constellation_info()

        print("Running system delay information test...")
        test_parse_cggtts_system_delay()

        print("All tests passed!")
    else:
        print(f"Test data file {test_file} does not exist, skipping tests")
