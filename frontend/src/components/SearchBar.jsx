import { useState } from 'react';
import { motion } from 'framer-motion';
import { FiSearch, FiX } from 'react-icons/fi';

const SearchBar = ({ onSearch, isLoading }) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim() && !isLoading) {
      onSearch(query.trim());
    }
  };

  const handleClear = () => {
    setQuery('');
  };

  return (
    <motion.form
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      onSubmit={handleSubmit}
      className="w-full max-w-4xl mx-auto"
    >
      <div className={`relative glass-card p-2 ${isLoading ? 'searching' : ''}`}>
        <div className="flex items-center">
          <FiSearch className="absolute left-6 text-magenta-500 text-2xl" />
          
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter a claim to verify... (e.g., 'Plants feel pain')"
            className="w-full bg-transparent text-white pl-16 pr-32 py-4 text-lg focus:outline-none placeholder-gray-500"
            disabled={isLoading}
          />
          
          {query && (
            <button
              type="button"
              onClick={handleClear}
              className="absolute right-32 text-gray-400 hover:text-white transition-colors"
              disabled={isLoading}
            >
              <FiX className="text-xl" />
            </button>
          )}
          
          <motion.button
            type="submit"
            disabled={!query.trim() || isLoading}
            className={`absolute right-2 btn-primary ${
              !query.trim() || isLoading ? 'opacity-50 cursor-not-allowed' : ''
            }`}
            whileHover={query.trim() && !isLoading ? { scale: 1.05 } : {}}
            whileTap={query.trim() && !isLoading ? { scale: 0.95 } : {}}
          >
            {isLoading ? (
              <span className="flex items-center gap-2">
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Searching
              </span>
            ) : (
              'Verify'
            )}
          </motion.button>
        </div>
      </div>
      
      {isLoading && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-center mt-4 text-gray-400 text-sm"
        >
          <p className="flex items-center justify-center gap-2">
            <span className="inline-block w-2 h-2 bg-magenta-500 rounded-full animate-pulse" />
            Searching peer-reviewed journals...
          </p>
        </motion.div>
      )}
    </motion.form>
  );
};

export default SearchBar;
