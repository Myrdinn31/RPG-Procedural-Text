import React, { useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="app">
      <div className="hero-section">
        <h1 className="title">
          Bienvenue dans votre nouveau projet React
        </h1>
        <p className="subtitle">
          Un projet moderne avec un design élégant
        </p>

        <div className="counter-section">
          <button 
            className="counter-btn"
            onClick={() => setCount(count - 1)}
          >
            -
          </button>
          <span className="counter-display">{count}</span>
          <button 
            className="counter-btn"
            onClick={() => setCount(count + 1)}
          >
            +
          </button>
        </div>

        <div className="features">
          <div className="feature-card">
            <h3>⚡ Rapide</h3>
            <p>Développement ultra-rapide avec Vite</p>
          </div>
          <div className="feature-card">
            <h3>🎨 Moderne</h3>
            <p>Design contemporain et responsive</p>
          </div>
          <div className="feature-card">
            <h3>🚀 Optimisé</h3>
            <p>Performance et expérience utilisateur optimales</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App