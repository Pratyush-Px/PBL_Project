import React, { createContext, useContext, useState, useRef } from 'react';

const ApiContext = createContext();

export const ApiProvider = ({ children }) => {
  const [baseUrl, setBaseUrl] = useState("http://localhost:8000");
  const [syncTrigger, setSyncTrigger] = useState(0);
  
  const handleSync = () => {
    setSyncTrigger(prev => prev + 1);
  };

  return (
    <ApiContext.Provider value={{ baseUrl, setBaseUrl, syncTrigger, handleSync }}>
      {children}
    </ApiContext.Provider>
  );
};

export const useApi = () => useContext(ApiContext);
