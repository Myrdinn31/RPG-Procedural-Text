
import React, { useState } from 'react'
import './App.css'

function App() {
  const [resultat, setResultat] = useState([])
  const [isGenerated, setIsGenerated] = useState(false)

  const acheteurs = ["Chantal", "Christian", "Manou", "Mathieu", "Monique", "Sonia", "Vincent", "Benjamin", "Laëtitia"]
  const receveurs = ["Chantal", "Christian", "Manou", "Mathieu", "Monique", "Sonia", "Vincent", "Benjamin", "Laëtitia"]

  const genererTirage = () => {
    let achetursCopy = [...acheteurs]
    let receveursCopy = [...receveurs]
    let nouveauResultat = []
    
    for (let i = 0; i < 9; i++) {
      let resultatTemp = {
        acheteur: "",
        receveur: ""
      }
      
      const tirageAcheteurs = Math.floor(Math.random() * achetursCopy.length)
      resultatTemp.acheteur = achetursCopy[tirageAcheteurs]
      
      let tirageReceveurs
      do {
        tirageReceveurs = Math.floor(Math.random() * receveursCopy.length)
      } while (receveursCopy[tirageReceveurs] === achetursCopy[tirageAcheteurs])
      
      resultatTemp.receveur = receveursCopy[tirageReceveurs]
      
      achetursCopy.splice(tirageAcheteurs, 1)
      receveursCopy.splice(tirageReceveurs, 1)
      
      nouveauResultat.push(resultatTemp)
    }
    
    setResultat(nouveauResultat)
    setIsGenerated(true)
  }

  const recommencer = () => {
    setResultat([])
    setIsGenerated(false)
  }

  return (
    <div className="app">
      <h1>TIRAGE AU SORT NOËL</h1>
      
      {!isGenerated ? (
        <button onClick={genererTirage} className="btn-primary">
          Générer le tirage
        </button>
      ) : (
        <div>
          <div className="resultat">
            {resultat.map((cadeau, index) => (
              <div key={index} className="paire">
                <strong>{cadeau.acheteur}</strong> offre un cadeau à <strong>{cadeau.receveur}</strong>
              </div>
            ))}
          </div>
          <button onClick={recommencer} className="btn-secondary">
            Nouveau tirage
          </button>
        </div>
      )}
    </div>
  )
}

export default App
