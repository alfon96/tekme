import { useState, useCallback, useRef, useEffect } from 'react';
import axios from 'axios';

const useApiCall = (uri, applyData, defaultDelay = 300) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const cancelTokenRef = useRef();
  const timeoutRef = useRef();

  const callApi = useCallback(async (config = {}) => {
    setLoading(true);
    setError(null);

    // Annulla la richiesta precedente se ce n'è una
    if (cancelTokenRef.current) {
      cancelTokenRef.current.cancel('Annullata la chiamata API precedente');
    }
    // Annulla il timeout precedente se ce n'è uno
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }

    // Imposta un nuovo timeout
    timeoutRef.current = setTimeout(async () => {
      cancelTokenRef.current = axios.CancelToken.source();

      try {
        const response = await axios({
          method: 'get',
          url: uri,
          cancelToken: cancelTokenRef.current.token,
          ...config
        });
        if (applyData) {
          applyData(response.data);
        }
      } catch (thrown) {
        if (!axios.isCancel(thrown)) {
          setError(thrown.message || 'An error occurred');
        }
      } finally {
        setLoading(false);
      }
    }, defaultDelay);
  }, [uri, applyData, defaultDelay]);

  // Pulizia al componente unmount
  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
      if (cancelTokenRef.current) {
        cancelTokenRef.current.cancel('Cancellazione della chiamata API al componente unmount');
      }
    };
  }, []);

  return { callApi, loading, error };
}

export default useApiCall;
