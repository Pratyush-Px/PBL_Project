import React, { useState } from 'react';
import Header from './components/Header/Header';
import Sidebar from './components/Sidebar/Sidebar';
import DetailView from './components/DetailView/DetailView';
import EmptyState from './components/EmptyState/EmptyState';
import './App.css';

const App = () => {
  const [selectedId, setSelectedId] = useState(null);

  const showDetail = selectedId != null;

  return (
    <div className="app-shell">
      <Header />
      
      <main className="app-body">
        <Sidebar 
          selectedId={selectedId} 
          onSelectResult={setSelectedId} 
        />
        
        <div style={{ flex: 1, position: 'relative', display: 'flex', flexDirection: 'column' }}>
          {/* We keep EmptyState functionally in DOM but fade it out based on `visible` prop */}
          <EmptyState visible={!showDetail} />
          
          <DetailView selectedId={selectedId} />
        </div>
      </main>
    </div>
  );
}

export default App;
