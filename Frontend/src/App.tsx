import { useState, Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { WordCloud } from './components/WordCloud';
import { analyzeUrl, type Topic } from './api';
import './App.css';

function App() {
  const [url, setUrl] = useState('');
  const [words, setWords] = useState<Topic[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sampleUrls = [
    "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "https://en.wikipedia.org/wiki/Space_exploration",
    "https://www.gutenberg.org/files/11/11-h/11-h.htm"
  ];

  const handleAnalyze = async () => {
    if (!url) return;
    setLoading(true);
    setError(null);
    try {
      const data = await analyzeUrl(url);
      setWords(data);
    } catch (err: any) {
      console.error(err);
      setError(err.response?.data?.detail || "Failed to analyze URL");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ width: '100vw', height: '100vh', display: 'flex', flexDirection: 'column', background: '#111', color: 'white' }}>
      <div style={{
        padding: '20px',
        zIndex: 10,
        background: 'rgba(0,0,0,0.8)',
        backdropFilter: 'blur(10px)',
        borderBottom: '1px solid #333',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: '10px'
      }}>
        <h1 style={{ margin: 0, fontSize: '1.5rem', background: '-webkit-linear-gradient(45deg, #FF0099, #493240)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>3D Word Cloud</h1>
        <div style={{ display: 'flex', gap: '10px', width: '100%', maxWidth: '600px' }}>
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Enter article URL..."
            style={{
              flex: 1,
              padding: '10px',
              borderRadius: '5px',
              border: '1px solid #444',
              background: '#222',
              color: 'white'
            }}
          />
          <button
            onClick={handleAnalyze}
            disabled={loading}
            style={{
              padding: '10px 20px',
              borderRadius: '5px',
              border: 'none',
              background: loading ? '#555' : '#FF0099',
              color: 'white',
              cursor: loading ? 'not-allowed' : 'pointer',
              fontWeight: 'bold'
            }}
          >
            {loading ? 'Analyzing...' : 'Visualize'}
          </button>
        </div>

        <div style={{ display: 'flex', gap: '10px', fontSize: '0.8rem', color: '#888' }}>
          <span>Try:</span>
          {sampleUrls.map((s, i) => (
            <button
              key={i}
              onClick={() => setUrl(s)}
              style={{ background: 'none', border: 'none', color: '#00ccff', cursor: 'pointer', textDecoration: 'underline' }}
            >
              Sample {i + 1}
            </button>
          ))}
        </div>

        {error && (
          <div style={{
            color: '#fff',
            background: 'rgba(255, 68, 68, 0.9)',
            padding: '10px 20px',
            borderRadius: '5px',
            marginTop: '10px',
            border: '1px solid #ff0000',
            maxWidth: '600px',
            textAlign: 'center'
          }}>
            <strong>Error:</strong> {error}
          </div>
        )}
      </div>

      <div style={{ flex: 1, position: 'relative' }}>
        <Canvas camera={{ position: [0, 0, 30], fov: 60 }}>
          <color attach="background" args={['#050505']} />
          <Suspense fallback={null}>
            <WordCloud words={words} />
            <OrbitControls autoRotate autoRotateSpeed={0.5} enableZoom={true} />
          </Suspense>
        </Canvas>

        {words.length === 0 && !loading && (
          <div style={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            color: '#444',
            pointerEvents: 'none',
            textAlign: 'center'
          }}>
            <h2>Enter a URL to generate a cloud</h2>
            <p>Explore topics in 3D space</p>
          </div>
        )}
      </div>
    </div>
  );
}
export default App;
