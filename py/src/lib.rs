use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList};
use ::cggtts::prelude::CGGTTS;

#[pyfunction]
fn parse_cggtts(path: &str, py: Python) -> PyResult<Py<PyAny>> {
    // Check if file exists first to avoid Rust panic
    use std::path::Path;
    let path_obj = Path::new(path);
    if !path_obj.exists() {
        return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
            format!("File does not exist: {}", path)
        ));
    }

    let cgg = CGGTTS::from_file(path)
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("Parse error: {}", e)))?;

    let result = PyDict::new(py);

    // Header section
    result.set_item("station", &cgg.header.station)?;
    result.set_item("version", &cgg.header.version.to_string())?;
    result.set_item("revision_date", cgg.header.revision_date.to_isoformat())?;
    result.set_item("nb_channels", cgg.header.nb_channels)?;
    result.set_item("reference_time", &cgg.header.reference_time.to_string())?;
    result.set_item("reference_frame", &cgg.header.reference_frame)?;

    // Receiver hardware info
    let receiver_dict = PyDict::new(py);
    receiver_dict.set_item("manufacturer", &cgg.header.receiver.manufacturer)?;
    receiver_dict.set_item("model", &cgg.header.receiver.model)?;
    receiver_dict.set_item("serial_number", &cgg.header.receiver.serial_number)?;
    receiver_dict.set_item("year", cgg.header.receiver.year)?;
    receiver_dict.set_item("release", &cgg.header.receiver.release)?;
    result.set_item("receiver", receiver_dict)?;

    // APC coordinates
    let coords_dict = PyDict::new(py);
    coords_dict.set_item("x", cgg.header.apc_coordinates.x)?;
    coords_dict.set_item("y", cgg.header.apc_coordinates.y)?;
    coords_dict.set_item("z", cgg.header.apc_coordinates.z)?;
    result.set_item("apc_coordinates", coords_dict)?;

    // Comments if any
    if let Some(comment) = &cgg.header.comments {
        result.set_item("comments", comment)?;
    }

    // System delay info
    let delay_dict = PyDict::new(py);
    delay_dict.set_item("antenna_cable_delay", cgg.header.delay.antenna_cable_delay)?;
    delay_dict.set_item("local_ref_delay", cgg.header.delay.local_ref_delay)?;
    delay_dict.set_item("total_cable_delay_nanos", cgg.header.delay.total_cable_delay_nanos())?;

    if let Some(calibration) = &cgg.header.delay.calibration_id {
        let cal_dict = PyDict::new(py);
        cal_dict.set_item("process_id", calibration.process_id)?;
        cal_dict.set_item("year", calibration.year)?;
        delay_dict.set_item("calibration_id", cal_dict)?;
    }
    result.set_item("delay", delay_dict)?;

    // IMS hardware if available
    if let Some(ims) = &cgg.header.ims_hardware {
        let ims_dict = PyDict::new(py);
        ims_dict.set_item("manufacturer", &ims.manufacturer)?;
        ims_dict.set_item("model", &ims.model)?;
        ims_dict.set_item("serial_number", &ims.serial_number)?;
        ims_dict.set_item("year", ims.year)?;
        ims_dict.set_item("release", &ims.release)?;
        result.set_item("ims_hardware", ims_dict)?;
    }

    result.set_item("tracks_count", cgg.tracks.len())?;
    result.set_item("has_ionospheric_data", cgg.has_ionospheric_data())?;
    result.set_item("common_view_class", &cgg.common_view_class().to_string())?;
    result.set_item("follows_bipm_tracking", cgg.follows_bipm_tracking())?;

    // Add satellite constellation info
    result.set_item("is_gps", cgg.is_gps_cggtts())?;
    result.set_item("is_galileo", cgg.is_galileo_cggtts())?;
    result.set_item("is_beidou", cgg.is_beidou_cggtts())?;
    result.set_item("is_glonass", cgg.is_glonass_cggtts())?;
    result.set_item("is_qzss", cgg.is_qzss_cggtts())?;
    result.set_item("is_irnss", cgg.is_irnss_cggtts())?;
    result.set_item("is_sbas", cgg.is_sbas_cggtts())?;

    // Add all tracks info
    let tracks_list = PyList::empty(py);
    for track in cgg.tracks.iter() {
        let track_dict = PyDict::new(py);
        track_dict.set_item("satellite", &track.sv.to_string())?;
        track_dict.set_item("epoch", track.epoch.to_isoformat())?;
        track_dict.set_item("duration_seconds", track.duration.to_seconds())?;
        track_dict.set_item("class", &track.class.to_string())?;
        track_dict.set_item("elevation_deg", track.elevation_deg)?;
        track_dict.set_item("azimuth_deg", track.azimuth_deg)?;
        track_dict.set_item("frc", &track.frc)?;
        track_dict.set_item("hc", track.hc)?;

        // Track data
        let data_dict = PyDict::new(py);
        data_dict.set_item("refsv", track.data.refsv)?;
        data_dict.set_item("srsv", track.data.srsv)?;
        data_dict.set_item("refsys", track.data.refsys)?;
        data_dict.set_item("srsys", track.data.srsys)?;
        data_dict.set_item("dsg", track.data.dsg)?;
        data_dict.set_item("ioe", track.data.ioe)?;
        data_dict.set_item("mdtr", track.data.mdtr)?;
        data_dict.set_item("smdt", track.data.smdt)?;
        data_dict.set_item("mdio", track.data.mdio)?;
        data_dict.set_item("smdi", track.data.smdi)?;
        track_dict.set_item("data", data_dict)?;

        // FDMA channel for GLONASS
        if let Some(fdma) = track.fdma_channel {
            track_dict.set_item("fdma_channel", fdma)?;
        }

        // Ionospheric data if available
        if let Some(iono) = track.iono {
            let iono_dict = PyDict::new(py);
            iono_dict.set_item("msio", iono.msio)?;
            iono_dict.set_item("smsi", iono.smsi)?;
            iono_dict.set_item("isg", iono.isg)?;
            track_dict.set_item("ionospheric_data", iono_dict)?;
        }

        tracks_list.append(track_dict)?;
    }
    result.set_item("tracks", tracks_list)?;

    // Add total duration if available
    if let Some(first_epoch) = cgg.first_epoch() {
        if let Some(last_epoch) = cgg.last_epoch() {
            result.set_item("total_duration_seconds", (last_epoch - first_epoch).to_seconds())?;
            result.set_item("first_epoch", first_epoch.to_isoformat())?;
            result.set_item("last_epoch", last_epoch.to_isoformat())?;
        }
    }

    Ok(result.into())
}

#[pymodule]
fn cggtts(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(parse_cggtts, m)?)?;
    Ok(())
}
