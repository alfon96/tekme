import { useState, useCallback } from 'react';
import axios from 'axios';

const useHttp = () => {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    const sendRequest = useCallback(async ({ url, method = 'GET', body = null, headers = {} }) => {
        setIsLoading(true);
        setError(null);
        try {
            const response = await axios({
                url,
                method,
                data: body,
                headers
            });
            setIsLoading(false);
            return response.data;
        } catch (err) {
            setError(err.message || 'Something went wrong!');
            setIsLoading(false);
            throw err;
        }
    }, []);

    return { isLoading, error, sendRequest };
};

export default useHttp;
