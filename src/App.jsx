import React from 'react';

function App() {
  const [count, setCount] = React.useState(0);

  return React.createElement('div', { className: 'app' },
    React.createElement('div', { className: 'hero-section' },
      React.createElement('h1', { className: 'title' },
        'Projet React Simple'
      ),
      React.createElement('p', { className: 'subtitle' },
        'Un projet React basique sans bundler'
      ),
      React.createElement('div', { className: 'counter-section' },
        React.createElement('button', {
          className: 'counter-btn',
          onClick: () => setCount(count - 1)
        }, '-'),
        React.createElement('span', { className: 'counter-display' }, count),
        React.createElement('button', {
          className: 'counter-btn',
          onClick: () => setCount(count + 1)
        }, '+')
      ),
      React.createElement('div', { className: 'features' },
        React.createElement('div', { className: 'feature-card' },
          React.createElement('h3', null, '⚡ Simple'),
          React.createElement('p', null, 'React sans configuration complexe')
        ),
        React.createElement('div', { className: 'feature-card' },
          React.createElement('h3', null, '🎨 Léger'),
          React.createElement('p', null, 'Pas de bundler, juste React')
        ),
        React.createElement('div', { className: 'feature-card' },
          React.createElement('h3', null, '🚀 Direct'),
          React.createElement('p', null, 'Développement immédiat')
        )
      )
    )
  );
}

export default App;