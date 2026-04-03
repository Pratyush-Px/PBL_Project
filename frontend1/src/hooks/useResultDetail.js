import { useState, useEffect, useRef } from 'react';
import { useApi } from '../context/ApiContext';
import { MOCK_DETAILS } from '../data/mockData';

export const useResultDetail = (id) => {
  const { baseUrl, syncTrigger } = useApi();
  const [detail, setDetail] = useState(null);
  const [loading, setLoading] = useState(false);
  
  const cache = useRef({});

  // Clear cache on sync
  useEffect(() => {
    cache.current = {};
  }, [syncTrigger]);

  useEffect(() => {
    if (!id) {
      setDetail(null);
      return;
    }

    if (cache.current[id]) {
      setDetail(cache.current[id]);
      return;
    }

    let active = true;
    const fetchDetail = async () => {
      setLoading(true);
      try {
        const response = await fetch(`${baseUrl}/results/${id}`);
        if (!response.ok) throw new Error("API not ok");
        const data = await response.json();
        if (active) {
          cache.current[id] = data;
          setDetail(data);
        }
      } catch (err) {
        if (active) {
          const fallback = MOCK_DETAILS[id] || MOCK_DETAILS["1"];
          cache.current[id] = fallback;
          setDetail(fallback);
        }
      } finally {
        if (active) setLoading(false);
      }
    };

    fetchDetail();

    return () => { active = false; };
  }, [id, baseUrl, syncTrigger]);

  return { detail, loading };
};
