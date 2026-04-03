import { useState, useEffect } from 'react';
import { useApi } from '../context/ApiContext';
import { MOCK_RESULTS } from '../data/mockData';

export const useResults = () => {
  const { baseUrl, syncTrigger } = useApi();
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isMockMode, setIsMockMode] = useState(false);

  useEffect(() => {
    let active = true;
    const fetchResults = async () => {
      setLoading(true);
      try {
        const response = await fetch(`${baseUrl}/results`);
        if (!response.ok) throw new Error("API not ok");
        const data = await response.json();
        if (active) {
          setResults(data);
          setIsMockMode(false);
        }
      } catch (err) {
        if (active) {
          setResults(MOCK_RESULTS);
          setIsMockMode(true);
        }
      } finally {
        if (active) setLoading(false);
      }
    };
    
    fetchResults();
    
    return () => { active = false; };
  }, [baseUrl, syncTrigger]);

  return { results, loading, isMockMode };
};
