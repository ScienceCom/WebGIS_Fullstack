import { useState } from "react";
import axios from "axios";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = () => {
    axios.post("http://localhost:8000/api/user/login", {
      username,
      password
    }).then(res => {
      localStorage.setItem("token", res.data.access_token);
      alert("Login berhasil");
    });
  };

  return (
    <div>
      <input onChange={e => setUsername(e.target.value)} placeholder="username"/>
      <input onChange={e => setPassword(e.target.value)} placeholder="password"/>
      <button onClick={handleLogin}>Login</button>
    </div>
  );
}

export default Login;