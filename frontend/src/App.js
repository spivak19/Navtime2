// frontend/src/App.js
import React, { useState } from 'react';
import CreateDocument from './CreateDocument';
import DocumentList from './DocumentList';
import './App.css';
import logo from './assets/logo.png'; // Ensure you have your logo in src/assets/logo.png

function App() {
  const [refresh, setRefresh] = useState(false);

  const handleDocumentCreated = () => {
    setRefresh(prev => !prev);
  };

  return (
    <div className="app-container">
      <div className="logo-container">
        <img src={logo} alt="Logo" className="logo-image" />
      </div>
      <div className="content-container">
        <h1>NavTime 2.0</h1>
        <div className="glass-card">
          <CreateDocument onDocumentCreated={handleDocumentCreated} />
        </div>
        <div className="glass-card">
          <DocumentList key={refresh} />
        </div>
      </div>
    </div>
  );
}

export default App;
