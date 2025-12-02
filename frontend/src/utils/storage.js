// Local Storage Keys
const STORAGE_KEYS = {
  SEARCH_HISTORY: 'vegan_factchecker_history',
  FAVORITES: 'vegan_factchecker_favorites',
  SETTINGS: 'vegan_factchecker_settings',
};

// Search History Management
export const saveSearch = (claim, result) => {
  try {
    const history = getSearchHistory();
    const newEntry = {
      id: Date.now(),
      claim,
      timestamp: new Date().toISOString(),
      verdict: result.evidence?.confidence_score > 7 ? 'TRUE' : 
               result.evidence?.confidence_score < 4 ? 'FALSE' : 'PARTIAL',
      category: result.analysis?.category || 'general',
      confidence: result.evidence?.confidence_score || 5,
    };
    
    // Add to beginning, limit to 50 entries
    const updatedHistory = [newEntry, ...history.filter(h => h.claim !== claim)].slice(0, 50);
    localStorage.setItem(STORAGE_KEYS.SEARCH_HISTORY, JSON.stringify(updatedHistory));
    
    return updatedHistory;
  } catch (error) {
    console.error('Error saving search:', error);
    return [];
  }
};

export const getSearchHistory = () => {
  try {
    const history = localStorage.getItem(STORAGE_KEYS.SEARCH_HISTORY);
    return history ? JSON.parse(history) : [];
  } catch (error) {
    console.error('Error loading history:', error);
    return [];
  }
};

export const clearSearchHistory = () => {
  try {
    localStorage.removeItem(STORAGE_KEYS.SEARCH_HISTORY);
    return true;
  } catch (error) {
    console.error('Error clearing history:', error);
    return false;
  }
};

export const deleteSearchEntry = (id) => {
  try {
    const history = getSearchHistory();
    const updated = history.filter(entry => entry.id !== id);
    localStorage.setItem(STORAGE_KEYS.SEARCH_HISTORY, JSON.stringify(updated));
    return updated;
  } catch (error) {
    console.error('Error deleting entry:', error);
    return [];
  }
};

// Favorites Management
export const addToFavorites = (claim, result) => {
  try {
    const favorites = getFavorites();
    const newFavorite = {
      id: Date.now(),
      claim,
      timestamp: new Date().toISOString(),
      result,
    };
    
    const updated = [newFavorite, ...favorites].slice(0, 20);
    localStorage.setItem(STORAGE_KEYS.FAVORITES, JSON.stringify(updated));
    return updated;
  } catch (error) {
    console.error('Error adding favorite:', error);
    return [];
  }
};

export const getFavorites = () => {
  try {
    const favorites = localStorage.getItem(STORAGE_KEYS.FAVORITES);
    return favorites ? JSON.parse(favorites) : [];
  } catch (error) {
    console.error('Error loading favorites:', error);
    return [];
  }
};

export const removeFromFavorites = (id) => {
  try {
    const favorites = getFavorites();
    const updated = favorites.filter(fav => fav.id !== id);
    localStorage.setItem(STORAGE_KEYS.FAVORITES, JSON.stringify(updated));
    return updated;
  } catch (error) {
    console.error('Error removing favorite:', error);
    return [];
  }
};

export const isFavorite = (claim) => {
  const favorites = getFavorites();
  return favorites.some(fav => fav.claim.toLowerCase() === claim.toLowerCase());
};

// Settings Management
export const getSettings = () => {
  try {
    const settings = localStorage.getItem(STORAGE_KEYS.SETTINGS);
    return settings ? JSON.parse(settings) : {
      maxSources: 5,
      includeCounterarguments: true,
      autoExpand: false,
      theme: 'dark',
    };
  } catch (error) {
    console.error('Error loading settings:', error);
    return { maxSources: 5, includeCounterarguments: true, autoExpand: false, theme: 'dark' };
  }
};

export const updateSettings = (newSettings) => {
  try {
    const current = getSettings();
    const updated = { ...current, ...newSettings };
    localStorage.setItem(STORAGE_KEYS.SETTINGS, JSON.stringify(updated));
    return updated;
  } catch (error) {
    console.error('Error updating settings:', error);
    return current;
  }
};

// Export statistics
export const getStatistics = () => {
  const history = getSearchHistory();
  const favorites = getFavorites();
  
  const categories = history.reduce((acc, entry) => {
    acc[entry.category] = (acc[entry.category] || 0) + 1;
    return acc;
  }, {});
  
  const verdicts = history.reduce((acc, entry) => {
    acc[entry.verdict] = (acc[entry.verdict] || 0) + 1;
    return acc;
  }, {});
  
  return {
    totalSearches: history.length,
    totalFavorites: favorites.length,
    categories,
    verdicts,
    mostRecentSearch: history[0]?.timestamp,
  };
};
