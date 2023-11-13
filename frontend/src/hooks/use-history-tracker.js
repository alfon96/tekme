import { useState, useEffect } from 'react';

const useHistoryTracker = (currentState, startTracking) => {
    const [history, setHistory] = useState([]);
    const [currentIndex, setCurrentIndex] = useState(-1);

    // Update history only when startTracking is true
    useEffect(() => {
        if (startTracking && history[currentIndex] !== currentState) {
            const newHistory = history.slice(0, currentIndex + 1);
            newHistory.push(currentState);

            if (newHistory.length > 30) {
                newHistory.splice(0, newHistory.length - 30);
            }

            setHistory(newHistory);
            setCurrentIndex(newHistory.length - 1);
        }
    }, [currentState, startTracking]); 

    const undo = () => {
        const newIndex = Math.max(currentIndex - 1, 0);
        setCurrentIndex(newIndex);
        return history[newIndex];
    };

    const redo = () => {
        const newIndex = Math.min(currentIndex + 1, history.length - 1);
        setCurrentIndex(newIndex);
        return history[newIndex];
    };

    // Function to get the current state
    const getCurrentState = () => {
        return history[currentIndex];
    };
    const disableUndo = currentIndex <= 0;
    const disableRedo = currentIndex >= history.length - 1 || history.length === 0;
    return { undo, redo, getCurrentState, disableUndo, disableRedo };
};

export default useHistoryTracker;
