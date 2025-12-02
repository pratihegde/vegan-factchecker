import { motion } from 'framer-motion';
import { FiCheckCircle, FiXCircle, FiAlertCircle, FiCopy, FiCheck } from 'react-icons/fi';
import { useState } from 'react';

const VerdictCard = ({ claim, evidence }) => {
  const [copiedQuick, setCopiedQuick] = useState(false);

  // Determine verdict
  const getVerdict = () => {
    const score = evidence?.confidence_score || 5;
    const summary = (evidence?.summary || '').toLowerCase();

    if (summary.includes('refutes') || summary.includes('false') || summary.includes('incorrect') || score <= 3) {
      return { text: 'FALSE', color: 'red', icon: FiXCircle, emoji: '❌' };
    } else if (summary.includes('supports') || summary.includes('true') || summary.includes('correct') || score >= 8) {
      return { text: 'TRUE', color: 'green', icon: FiCheckCircle, emoji: '✅' };
    } else {
      return { text: 'PARTIALLY TRUE', color: 'yellow', icon: FiAlertCircle, emoji: '⚠️' };
    }
  };

  const verdict = getVerdict();
  const Icon = verdict.icon;

  // Generate quick response (simplified from backend logic)
  const getQuickResponse = () => {
    const summary = evidence?.summary || '';
    const sentences = summary.split('. ');
    return sentences[0] || 'See details below for full analysis.';
  };

  const quickResponse = getQuickResponse();

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    setCopiedQuick(true);
    setTimeout(() => setCopiedQuick(false), 2000);
  };

  const verdictColors = {
    red: 'border-accent-red bg-accent-red/10',
    green: 'border-accent-green bg-accent-green/10',
    yellow: 'border-accent-yellow bg-accent-yellow/10',
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
      className="w-full max-w-4xl mx-auto mt-8"
    >
      {/* Claim Header */}
      <div className="glass-card p-6 mb-4">
        <h2 className="text-2xl font-display font-bold text-white uppercase tracking-wide">
          {claim}
        </h2>
      </div>

      {/* Verdict */}
      <div className={`glass-card border-2 ${verdictColors[verdict.color]} p-8 mb-4`}>
        <div className="flex items-center justify-center mb-6">
          <div className="flex items-center gap-4">
            <Icon className={`text-5xl text-accent-${verdict.color}`} />
            <div>
              <p className="text-gray-400 text-sm uppercase tracking-wide">Verdict</p>
              <h3 className={`text-4xl font-display font-bold text-accent-${verdict.color}`}>
                {verdict.text}
              </h3>
            </div>
          </div>
        </div>

        {/* Quick Response */}
        <div className="bg-navy-900/50 rounded-lg p-6 border border-navy-700">
          <div className="flex justify-between items-start mb-3">
            <h4 className="text-magenta-500 font-semibold text-lg flex items-center gap-2">
              💬 QUICK RESPONSE
            </h4>
            <button
              onClick={() => copyToClipboard(quickResponse)}
              className="btn-secondary flex items-center gap-2 text-sm py-1 px-3"
            >
              {copiedQuick ? (
                <>
                  <FiCheck className="text-green-400" />
                  Copied!
                </>
              ) : (
                <>
                  <FiCopy />
                  Copy
                </>
              )}
            </button>
          </div>
          <p className="text-white text-lg leading-relaxed">
            "{quickResponse}"
          </p>
        </div>
      </div>
    </motion.div>
  );
};

export default VerdictCard;