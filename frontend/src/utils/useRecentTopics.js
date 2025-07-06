import { useState, useCallback } from 'react';

export const useRecentTopics = (initialTopics = []) => {
  const [recentTopics, setRecentTopics] = useState(initialTopics);

  const addTopic = useCallback((topic, explanation) => {
    setRecentTopics((prevTopics = []) => {
      const newTopic = {
        topic,
        explanation,
      };
      const updatedTopics = [newTopic, ...prevTopics].slice(0, 5); // Keep only the last 5 topics

      return updatedTopics;
    });
  }, []);

  return {
    recentTopics,
    setRecentTopics,
    addTopic,
  };
};
