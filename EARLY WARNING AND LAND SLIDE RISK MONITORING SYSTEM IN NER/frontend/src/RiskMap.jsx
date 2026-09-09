import React from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup, ZoomControl } from 'react-leaflet';

const areas = [
  { name: 'East Khasi Hills', state: 'Meghalaya', position: [25.5, 91.4], score: 88, level: 'High' },
  { name: 'Aizawl', state: 'Mizoram', position: [23.7, 92.7], score: 74, level: 'Medium' },
  { name: 'Tawang', state: 'Arunachal Pradesh', position: [27.6, 91.9], score: 43, level: 'Low' },
  { name: 'Darjeeling', state: 'West Bengal', position: [27.0, 88.3], score: 82, level: 'High' },
  { name: 'Kohima', state: 'Nagaland', position: [25.7, 94.1], score: 61, level: 'Medium' },
];
const colors = { High: '#e75b4a', Medium: '#e6a23c', Low: '#35b58a' };

export default function RiskMap() { return <div className="map-wrap"><MapContainer center={[25.4, 92.7]} zoom={5} zoomControl={false} scrollWheelZoom><ZoomControl position="bottomright" /><TileLayer attribution="&copy; OpenStreetMap" url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />{areas.map((area) => <CircleMarker key={area.name} center={area.position} radius={10} pathOptions={{ color: colors[area.level], fillColor: colors[area.level], fillOpacity: .8, weight: 3 }}><Popup><strong>{area.name}</strong><br />{area.state}<br />Risk score: {area.score} ({area.level})</Popup></CircleMarker>)}</MapContainer><div className="map-legend">{Object.entries(colors).map(([name, color]) => <span key={name}><i style={{ background: color }} />{name}</span>)}</div></div>; }
