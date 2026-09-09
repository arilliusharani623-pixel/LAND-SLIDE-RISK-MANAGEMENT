import React, { useState } from 'react';
import axios from 'axios';
import { ArrowPathIcon, BoltIcon } from '@heroicons/react/24/outline';

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const initial = { rainfall: 450, slope: 35, soil_moisture: 78, elevation: 1200 };

export default function PredictionForm({ onResult }) {
  const [values, setValues] = useState(initial);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const submit = async (event) => {
    event.preventDefault(); setLoading(true); setError('');
    try { const { data } = await axios.post(`${API}/predict`, values); onResult(data); }
    catch (err) { setError(err.response?.data?.detail || 'Prediction service is unavailable.'); }
    finally { setLoading(false); }
  };
  const fields = [['rainfall', 'Rainfall', 'mm', 0, 2000], ['slope', 'Slope angle', 'deg', 0, 90], ['soil_moisture', 'Soil moisture', '%', 0, 100], ['elevation', 'Elevation', 'm', -500, 9000]];
  return <form className="panel prediction-form" onSubmit={submit}>
    <div className="panel-heading"><div><p className="eyebrow">LIVE INFERENCE</p><h2>Assess a zone</h2></div><BoltIcon className="heading-icon" /></div>
    <div className="form-grid">{fields.map(([key, label, unit, min, max]) => <label key={key}><span>{label}<small>{unit}</small></span><input type="number" min={min} max={max} step="any" value={values[key]} onChange={(e) => setValues({ ...values, [key]: Number(e.target.value) })} required /></label>)}</div>
    <button className="primary-button" disabled={loading}>{loading ? <ArrowPathIcon className="spin" /> : <BoltIcon />} {loading ? 'Running model' : 'Run risk assessment'}</button>
    {error && <p className="form-error">{error}</p>}
  </form>;
}
