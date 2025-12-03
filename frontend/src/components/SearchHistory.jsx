import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FiClock, FiX, FiTrash2, FiChevronDown } from 'react-icons/fi';
import { getSearchHistory, deleteSearchEntry, clearSearchHistory } from '../utils/storage';

const SearchHistory = ({ onSelectSearch, isOpen, onToggle }) => {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = () => {
    const historyData = getSearchHistory();
    setHistory(historyData);
  };

  const handleDelete = (id, e) => {
    e.stopPropagation();
    const updated = deleteSearchEntry(id);
    setHistory(updated);
  };

  const handleClearAll = () => {
    if (window.confirm('Clear all search history?')) {
      clearSearchHistory();
      setHistory([]);
    }
  };

  const getVerdictColor = (verdict) => {
    switch (verdict) {
      case 'TRUE': return 'text-accent-green';
      case 'FALSE': return 'text-accent-red';
      case 'PARTIAL': return 'text-accent-yellow';
      default: return 'text-gray-400';
    }
  };

  const getVerdictEmoji = (verdict) => {
    switch (verdict) {
      case 'TRUE': return '✅';
      case 'FALSE': return '❌';
      case 'PARTIAL': return '⚠️';
      default: return '❓';
    }
  };

  return (
    <>
      {/* Toggle Button - MOBILE OPTIMIZED */}
      <motion.button
        onClick={onToggle}
        className="fixed bottom-6 right-4 sm:top-6 sm:right-6 sm:bottom-auto z-50 btn-secondary flex items-center gap-2 shadow-xl"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        <FiClock className="text-base sm:text-lg" />
        <span className="hidden sm:inline">Past Searches</span>
        <span className="sm:hidden text-xs">History</span>
        <motion.div
          animate={{ rotate: isOpen ? 180 : 0 }}
          transition={{ duration: 0.2 }}
          className="hidden sm:block"
        >
          <FiChevronDown />
        </motion.div>
      </motion.button>

      {/* Sidebar */}
      <AnimatePresence>
        {isOpen && (
          <>
            {/* Overlay */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={onToggle}
              className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
            />

            {/* Sidebar Panel - MOBILE OPTIMIZED */}
            <motion.div
              initial={{ x: '100%' }}
              animate={{ x: 0 }}
              exit={{ x: '100%' }}
              transition={{ type: 'spring', damping: 25, stiffness: 200 }}
              className="fixed right-0 top-0 h-full w-full sm:max-w-md bg-navy-800 shadow-2xl z-50 overflow-hidden flex flex-col"
            >
              {/* Header - MOBILE OPTIMIZED */}
              <div className="p-4 sm:p-6 border-b border-navy-700 flex items-center justify-between">
                <div>
                  <h2 className="text-xl sm:text-2xl font-display font-bold text-white flex items-center gap-2">
                    <FiClock className="text-magenta-500 text-lg sm:text-xl" />
                    <span className="hidden sm:inline">Search History</span>
                    <span className="sm:hidden">History</span>
                  </h2>
                  <p className="text-gray-400 text-xs sm:text-sm mt-1">{history.length} searches</p>
                </div>
                <button
                  onClick={onToggle}
                  className="text-gray-400 hover:text-white transition-colors p-2 touch-manipulation"
                  aria-label="Close history"
                >
                  <FiX className="text-xl sm:text-2xl" />
                </button>
              </div>

              {/* History List - MOBILE OPTIMIZED */}
              <div className="flex-1 overflow-y-auto p-3 sm:p-4 smooth-scroll">
                {history.length === 0 ? (
                  <div className="text-center py-12">
                    <FiClock className="text-4xl sm:text-5xl text-gray-600 mx-auto mb-4" />
                    <p className="text-gray-400 text-sm sm:text-base">No search history yet</p>
                    <p className="text-gray-500 text-xs sm:text-sm mt-2">
                      Your verified claims will appear here
                    </p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {history.map((entry) => (
                      <motion.button
                        key={entry.id}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        onClick={() => {
                          onSelectSearch(entry.claim);
                          onToggle();
                        }}
                        className="w-full glass-card p-3 sm:p-4 text-left hover:border-magenta-500/50 transition-all group touch-manipulation"
                      >
                        <div className="flex items-start justify-between mb-2">
                          <span className="text-xl sm:text-2xl">{getVerdictEmoji(entry.verdict)}</span>
                          <button
                            onClick={(e) => handleDelete(entry.id, e)}
                            className="opacity-100 sm:opacity-0 sm:group-hover:opacity-100 text-gray-400 hover:text-red-400 transition-all p-2 touch-manipulation"
                            aria-label="Delete entry"
                          >
                            <FiTrash2 className="text-base sm:text-lg" />
                          </button>
                        </div>
                        
                        <h3 className="text-white font-semibold mb-2 line-clamp-2 text-sm sm:text-base">
                          {entry.claim}
                        </h3>
                        
                        <div className="flex items-center justify-between text-xs">
                          <span className={`font-semibold ${getVerdictColor(entry.verdict)}`}>
                            {entry.verdict}
                          </span>
                          <span className="text-gray-500">
                            {new Date(entry.timestamp).toLocaleDateString()}
                          </span>
                        </div>
                        
                        <div className="mt-2">
                          <span className="px-2 py-1 bg-navy-900/50 text-gray-400 text-xs rounded capitalize">
                            {entry.category}
                          </span>
                        </div>
                      </motion.button>
                    ))}
                  </div>
                )}
              </div>

              {/* Footer - MOBILE OPTIMIZED */}
              {history.length > 0 && (
                <div className="p-3 sm:p-4 border-t border-navy-700">
                  <button
                    onClick={handleClearAll}
                    className="w-full btn-secondary flex items-center justify-center gap-2 text-red-400 hover:text-red-300 text-sm sm:text-base"
                  >
                    <FiTrash2 />
                    Clear All History
                  </button>
                </div>
              )}
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  );
};

export default SearchHistory;