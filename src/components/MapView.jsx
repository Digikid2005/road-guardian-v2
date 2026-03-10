import { MapContainer, TileLayer, Marker, Polyline } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { useEffect, useState } from "react";
import L from "leaflet";
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  iconUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png"
});
export default function MapView({ incident }) {
  const [userLocation, setUserLocation] = useState(null);
  const [ambulance, setAmbulance] = useState(
    incident.ambulanceLocation
  );
  useEffect(() => {
    navigator.geolocation.getCurrentPosition(pos => {
      setUserLocation([pos.coords.latitude, pos.coords.longitude]);
    });
    const timer = setInterval(() => {
      setAmbulance(([lat, lng]) => [lat + 0.0001, lng + 0.0001]);
    }, 3000);
    return () => clearInterval(timer);
  }, []);
  return (
    <MapContainer
      center={incident.hospitalLocation}
      zoom={14}
      className="map"
    >
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

      <Marker position={incident.hospitalLocation} />
      <Marker position={incident.accidentLocation} />
      <Marker position={ambulance} />

      {userLocation && <Marker position={userLocation} />}

      <Polyline
        positions={[
          incident.hospitalLocation,
          incident.accidentLocation
        ]}
        color="red"
      />
    </MapContainer>
  );
}
