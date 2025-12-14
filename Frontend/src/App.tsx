import { useState } from 'react';
import './App.css';

function App() {
  const [url, setUrl] = useState('');
  return (
    <div style={{ color: 'white', padding: 20 }}>
      <h1>3D Word Cloud</h1>
      <input value={url} onChange={e => setUrl(e.target.value)} placeholder="URL..." />
    </div>
  );
}
export default App;
