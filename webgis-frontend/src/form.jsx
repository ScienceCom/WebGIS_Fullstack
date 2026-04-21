import { useState } from "react";
import axios from "axios";

function Form() {
  const [nama, setNama] = useState("");
  const [jenis, setJenis] = useState("");
  const [lat, setLat] = useState("");
  const [lng, setLng] = useState("");

  const handleSubmit = () => {
    axios.post("http://localhost:8000/api/fasilitas", {
      nama,
      jenis,
      latitude: parseFloat(lat),
      longitude: parseFloat(lng)
    });
  };

  axios.post(url, data, {
    headers: {
      Authorization: "Bearer " + localStorage.getItem("token")
    }
  });
  
  return (
    <div>
      <input placeholder="Nama" onChange={e => setNama(e.target.value)} />
      <input placeholder="Jenis" onChange={e => setJenis(e.target.value)} />
      <input placeholder="Latitude" onChange={e => setLat(e.target.value)} />
      <input placeholder="Longitude" onChange={e => setLng(e.target.value)} />
      <button onClick={handleSubmit}>Tambah</button>
    </div>
  );
}

export default Form;