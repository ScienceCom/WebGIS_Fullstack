import { MapContainer, TileLayer, GeoJSON } from "react-leaflet";
import { useEffect, useState } from "react";
import axios from "axios";
import L from "leaflet";

function App() {
  const [data, setData] = useState(null);
  const url = "http://localhost:8000/api/fasilitas/geojson";

  useEffect(() => {
    axios.get("http://localhost:8000/api/fasilitas/geojson")
      .then(res => setData(res.data))
      .catch(err => console.log(err));
  }, []);

  axios.post(url, data, {
    headers: {
      Authorization: "Bearer " + localStorage.getItem("token")
    }
  });

  const getColor = (jenis) => {
    if (jenis === "Puskesmas") return "red";
    if (jenis === "Masjid") return "green";
    if (jenis === "Rumah Makan") return "orange";
    if (jenis === "Fitness Center") return "purple";
    return "blue";
  };

  const pointToLayer = (feature, latlng) => {
    return L.circleMarker(latlng, {
      radius: 8,
      fillColor: getColor(feature.properties.jenis),
      color: "black",
      weight: 1,
      fillOpacity: 0.8
    });
  };

  const onEachFeature = (feature, layer) => {
    layer.bindPopup(`
      <b>${feature.properties.nama}</b><br/>
      <button onclick="edit(${feature.properties.id})">Edit</button>
      <button onclick="hapus(${feature.properties.id})">Delete</button>
    `);
  };

  window.hapus = (id) => {
    axios.delete(`http://localhost:8000/api/fasilitas/${id}`)
      .then(() => window.location.reload());
  };

  return (
    <div style={{ height: "100vh", width: "100%" }}>
      <MapContainer center={[-5.397, 105.256]} zoom={15} style={{ height: "100%", width: "100%" }}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

        {data && (
          <GeoJSON
            data={data}
            pointToLayer={pointToLayer}
            onEachFeature={onEachFeature}
          />
        )}
      </MapContainer>
    </div>
  );
}

export default App;