import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import SearchBar from './components/SearchBar';
import VerdictCard from './components/VerdictCard';
import ResultsDisplay from './components/ResultsDisplay';
import SearchHistory from './components/SearchHistory';
import NutritionCalculator from './components/NutritionCalculator';
import { verifyClaim, checkAPIHealth } from './utils/api';
import { saveSearch } from './utils/storage';
import { FiGithub, FiLinkedin, FiMail, FiAlertCircle } from 'react-icons/fi';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [currentClaim, setCurrentClaim] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [historyOpen, setHistoryOpen] = useState(false);
  const [apiStatus, setApiStatus] = useState('checking');

  useEffect(() => {
    checkAPI();
  }, []);

  const checkAPI = async () => {
    try {
      const status = await checkAPIHealth();
      setApiStatus(status.status === 'unavailable' ? 'demo' : 'online');
    } catch (error) {
      setApiStatus('demo');
    }
  };

  const handleSearch = async (claim) => {
    setIsLoading(true);
    setError(null);
    setCurrentClaim(claim);
    setResult(null);

    try {
      const data = await verifyClaim(claim, 5, true);
      setResult(data);
      
      // Save to history
      saveSearch(claim, data);
    } catch (err) {
      setError(err.message || 'Failed to verify claim. Please try again.');
      console.error('Search error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectFromHistory = (claim) => {
    handleSearch(claim);
  };

  return (
    <div className="min-h-screen bg-navy-900 relative overflow-hidden">
      {/* Background gradient effects */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-magenta-500/10 rounded-full blur-3xl animate-pulse-slow" />
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse-slow" style={{ animationDelay: '1s' }} />
      </div>

      {/* Main Content */}
      <div className="relative z-10">
        {/* Header */}
        <header className="py-8 px-6">
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="max-w-6xl mx-auto"
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <span className="text-5xl">🌱</span>
                <div>
                  <h1 className="text-4xl font-display font-bold gradient-text">
                    VEGAN FACT CHECKER
                  </h1>
                  <p className="text-gray-400 mt-1">
                    Evidence-based activism with peer-reviewed sources
                  </p>
                </div>
              </div>

              {/* API Status Badge */}
              <div className="flex items-center gap-3">
                {apiStatus === 'demo' && (
                  <div className="flex items-center gap-2 px-3 py-2 bg-accent-yellow/20 text-accent-yellow rounded-lg text-sm border border-accent-yellow/30">
                    <FiAlertCircle />
                    Demo Mode
                  </div>
                )}
                {apiStatus === 'online' && (
                  <div className="flex items-center gap-2 px-3 py-2 bg-accent-green/20 text-accent-green rounded-lg text-sm border border-accent-green/30">
                    <span className="w-2 h-2 bg-accent-green rounded-full animate-pulse" />
                    API Online
                  </div>
                )}
              </div>
            </div>

            {/* Example claims */}
            <div className="mt-6 flex flex-wrap gap-2">
              <span className="text-gray-400 text-sm">Try:</span>
              {['Plants have feelings', 'Do vegans get enough protein?', 'How do vegans get omega-3?'].map((example) => (
                <button
                  key={example}
                  onClick={() => !isLoading && handleSearch(example)}
                  className="px-3 py-1 bg-navy-800 hover:bg-navy-700 text-magenta-400 text-sm rounded-full transition-colors border border-navy-700 hover:border-magenta-500/50"
                  disabled={isLoading}
                >
                  {example}
                </button>
              ))}
            </div>
          </motion.div>
        </header>

        {/* Fact Checker Section */}
        <main className="px-6 pb-12">
          <SearchBar onSearch={handleSearch} isLoading={isLoading} />

          {/* Error Display */}
          {error && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="max-w-4xl mx-auto mt-6 glass-card p-4 border-2 border-accent-red bg-accent-red/10"
            >
              <div className="flex items-center gap-3">
                <FiAlertCircle className="text-accent-red text-2xl" />
                <div>
                  <p className="text-white font-semibold">Error</p>
                  <p className="text-gray-300">{error}</p>
                </div>
              </div>
            </motion.div>
          )}

          {/* Results */}
          {result && !isLoading && (
            <div className="mt-8 animate-fade-in">
              <VerdictCard claim={currentClaim} evidence={result.evidence} />
              <div className="mt-6">
                <ResultsDisplay result={result} />
              </div>
            </div>
          )}

          {/* Empty State */}
          {!result && !isLoading && !error && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
              className="max-w-4xl mx-auto mt-16 text-center"
            >
              <div className="glass-card p-12">
                <span className="text-7xl mb-6 block">🔍</span>
                <h2 className="text-3xl font-display font-bold text-white mb-4">
                  Enter a claim to verify
                </h2>
                <p className="text-gray-400 max-w-2xl mx-auto leading-relaxed">
                  Search peer-reviewed journals and credible sources to find evidence-based
                  responses for your activism. Get direct quotes, citations, and confidence
                  scores.
                </p>

                <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="p-6 bg-navy-900/50 rounded-lg border border-navy-700">
                    <span className="text-3xl mb-3 block">🏆</span>
                    <h3 className="text-white font-semibold mb-2">Peer-Reviewed</h3>
                    <p className="text-gray-400 text-sm">
                      Sources from Nature, Harvard, and top journals
                    </p>
                  </div>
                  <div className="p-6 bg-navy-900/50 rounded-lg border border-navy-700">
                    <span className="text-3xl mb-3 block">📋</span>
                    <h3 className="text-white font-semibold mb-2">Quick Responses</h3>
                    <p className="text-gray-400 text-sm">
                      Copy-paste talking points for debates
                    </p>
                  </div>
                  <div className="p-6 bg-navy-900/50 rounded-lg border border-navy-700">
                    <span className="text-3xl mb-3 block">📖</span>
                    <h3 className="text-white font-semibold mb-2">Full Citations</h3>
                    <p className="text-gray-400 text-sm">
                      APA and MLA format citations ready to use
                    </p>
                  </div>
                </div>
              </div>
            </motion.div>
          )}
        </main>

        {/* Divider */}
        <div className="max-w-6xl mx-auto px-6 py-12">
          <div className="border-t border-navy-700"></div>
        </div>

        {/* Nutrition Calculator Section */}
        <section className="px-6 pb-12">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="max-w-6xl mx-auto"
          >
            {/* Section Header */}
            <div className="text-center mb-8">
              <h2 className="text-3xl font-display font-bold gradient-text mb-2">
                NUTRITION CALCULATOR
              </h2>
              <p className="text-gray-400">
                Calculate your personalized daily nutrient needs
              </p>
            </div>

            {/* Calculator Component */}
            <NutritionCalculator />
          </motion.div>
        </section>

        {/* Footer */}
        <footer className="py-8 px-6 border-t border-navy-800 mt-12">
          <div className="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="text-gray-400 text-sm">
              <p>Built for vegan activists • Powered by peer-reviewed research</p>
              <p className="text-xs mt-1">
                Sources: Semantic Scholar, PubMed, Tavily Search • RDA: NIH, USDA, WHO
              </p>
            </div>
            
            <div className="flex items-center gap-4">
              <a
                href="https://github.com/yourusername"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-magenta-500 transition-colors"
              >
                <FiGithub className="text-xl" />
              </a>
              <a
                href="https://linkedin.com/in/yourprofile"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-magenta-500 transition-colors"
              >
                <FiLinkedin className="text-xl" />
              </a>
              <a
                href="mailto:your.email@example.com"
                className="text-gray-400 hover:text-magenta-500 transition-colors"
              >
                <FiMail className="text-xl" />
              </a>
            </div>
          </div>
        </footer>
      </div>

      {/* Search History Sidebar */}
      <SearchHistory
        isOpen={historyOpen}
        onToggle={() => setHistoryOpen(!historyOpen)}
        onSelectSearch={handleSelectFromHistory}
      />
    </div>
  );
}

export default App;