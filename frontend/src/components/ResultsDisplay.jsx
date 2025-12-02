import { useState } from 'react';
import { motion } from 'framer-motion';
import { FiCopy, FiCheck, FiExternalLink, FiBook, FiAward } from 'react-icons/fi';
import CollapsibleSection from './CollapsibleSection';

const ResultsDisplay = ({ result }) => {
  const [copiedItems, setCopiedItems] = useState({});

  if (!result || !result.evidence) return null;

  const { evidence, analysis } = result;
  const sources = evidence.sources || [];

  const copyToClipboard = (text, key) => {
    navigator.clipboard.writeText(text);
    setCopiedItems({ ...copiedItems, [key]: true });
    setTimeout(() => {
      setCopiedItems({ ...copiedItems, [key]: false });
    }, 2000);
  };

  // Check if a journal/source is prestigious
  const isPrestigious = (journal) => {
    if (!journal) return false;
    
    const journalLower = journal.toLowerCase();
    const prestigious = [
      'harvard', 'oxford', 'stanford', 'cambridge', 'mit',
      'yale', 'johns hopkins', 'mayo clinic',
      'nature', 'science', 'cell', 'lancet', 'jama', 'nejm',
      'new england journal of medicine',
      'bmj', 'plos medicine', 'cochrane',
      'who', 'nih', 'cdc', 'fda',
      'american journal of clinical nutrition',
      'journal of nutrition', 'nutrients'
    ];
    
    return prestigious.some(p => journalLower.includes(p));
  };

  // Get prestigious badge text
  const getPrestigiousBadge = (journal) => {
    if (!journal) return null;
    
    const journalLower = journal.toLowerCase();
    
    // Top tier journals
    if (journalLower.includes('nature')) return '🏆 Nature';
    if (journalLower.includes('science')) return '🏆 Science';
    if (journalLower.includes('lancet')) return '🏆 The Lancet';
    if (journalLower.includes('nejm') || journalLower.includes('new england journal')) return '🏆 NEJM';
    if (journalLower.includes('jama')) return '🏆 JAMA';
    if (journalLower.includes('cell')) return '🏆 Cell';
    
    // Top institutions
    if (journalLower.includes('harvard')) return '🏆 Harvard';
    if (journalLower.includes('oxford')) return '🏆 Oxford';
    if (journalLower.includes('stanford')) return '🏆 Stanford';
    if (journalLower.includes('cambridge')) return '🏆 Cambridge';
    if (journalLower.includes('mit')) return '🏆 MIT';
    if (journalLower.includes('yale')) return '🏆 Yale';
    if (journalLower.includes('johns hopkins')) return '🏆 Johns Hopkins';
    if (journalLower.includes('mayo clinic')) return '🏆 Mayo Clinic';
    
    // Organizations
    if (journalLower.includes('who')) return '🏆 WHO';
    if (journalLower.includes('nih')) return '🏆 NIH';
    
    // High-quality nutrition journals
    if (journalLower.includes('american journal of clinical nutrition')) return '⭐ AJCN';
    if (journalLower.includes('journal of nutrition')) return '⭐ J. Nutrition';
    if (journalLower.includes('nutrients')) return '⭐ Nutrients';
    if (journalLower.includes('bmj')) return '⭐ BMJ';
    
    return null;
  };

  const extractKeyFacts = () => {
    const facts = [];
    
    sources.slice(0, 3).forEach(source => {
      if (source.key_finding && source.key_finding.length > 10) {
        facts.push(source.key_finding);
      }
    });

    if (facts.length === 0 && evidence.summary) {
      const sentences = evidence.summary.split('. ');
      facts.push(...sentences.slice(0, 3));
    }

    return facts.slice(0, 3);
  };

  const extractPrestigiousSources = () => {
    return sources
      .filter(s => isPrestigious(s.journal))
      .map(s => getPrestigiousBadge(s.journal) || s.journal)
      .slice(0, 3);
  };

const generateCounterResponse = (question) => {
  if (!question) return "See the sources above for detailed information.";
  
  const q = question.toLowerCase();
  
  // PLANT PAIN RESPONSES - Specific matching
  if (q.includes('feel pain') || q.includes('really feel') || q.includes('like animals')) {
    return "Plants lack brains, nervous systems, and pain receptors - all required for feeling pain. They respond to stimuli through automatic chemical processes, not conscious experience.";
  }
  
  if (q.includes('chemical') || q.includes('release') || q.includes('when you cut')) {
    return "Yes, plants release chemicals when damaged - but that's automatic signaling, not pain. A smoke detector beeps when there's fire, but it's not scared. Chemical responses ≠ consciousness.";
  }
  
  if (q.includes('scream') || q.includes('sound') || q.includes('noise') || q.includes('study')) {
    return "That was ultrasonic vibrations from air bubbles in damaged stems - like wood creaking. No evidence of consciousness, distress, or suffering. Plants lack the neurological hardware for that.";
  }
  
  if (q.includes('respond') || q.includes('react') || q.includes('just reacting') || q.includes("aren't just")) {
    return "Response doesn't equal pain. Your thermostat responds to temperature changes - it doesn't feel hot or cold. Plants lack the brain structures necessary for conscious experience.";
  }
  
  if (q.includes('survival') && q.includes('mechanism')) {
    return "Survival mechanisms are automatic processes, not evidence of consciousness. Single-celled bacteria have survival mechanisms too - they're not sentient. Pain requires a nervous system and brain.";
  }
  
  if (q.includes('communication') || q.includes('signal') || q.includes('talk')) {
    return "Plants use chemical signals, but that's not communication like animals. It's automatic chemistry with no consciousness required - like how your liver responds to toxins automatically.";
  }
  
  // PROTEIN RESPONSES
  if (q.includes('protein')) {
    if (q.includes('incomplete') || q.includes('complete')) {
      return "Plant proteins become complete when combined throughout the day. The Academy of Nutrition and Dietetics confirms plant-based diets meet all protein needs. Beans + rice, hummus + pita - all complete protein.";
    }
    if (q.includes('enough') || q.includes('adequate')) {
      return "Yes! The Academy of Nutrition and Dietetics (100,000+ professionals) confirms plant-based diets provide adequate protein for all life stages. Billions of healthy vegans prove it works.";
    }
    return "Plant proteins combined throughout the day provide all essential amino acids. Major health organizations confirm plant-based diets are nutritionally adequate.";
  }
  
  // B12 RESPONSES
  if (q.includes('b12') || q.includes('b-12')) {
    return "B12 comes from bacteria, not animals. Factory-farmed animals get B12 supplements in their feed - vegans just skip the middleman. It's the same bacteria-produced B12.";
  }
  
  // OMEGA-3 RESPONSES  
  if (q.includes('omega') || q.includes('dha') || q.includes('epa')) {
    return "ALA from flax, chia, and walnuts converts to DHA/EPA. Or take algae oil for direct DHA/EPA - that's where fish get their omega-3s anyway!";
  }
  
  // IRON RESPONSES
  if (q.includes('iron')) {
    return "Plant foods are high in iron (lentils, spinach, fortified cereals). Pair with vitamin C for 3-4x better absorption. Many omnivores are iron-deficient too.";
  }
  
  // CALCIUM RESPONSES
  if (q.includes('calcium')) {
    return "Calcium is abundant in fortified plant milk, tofu, leafy greens, and tahini. Countries with highest dairy consumption have highest osteoporosis rates!";
  }
  
  // SOY RESPONSES
  if (q.includes('soy') && (q.includes('estrogen') || q.includes('hormone'))) {
    return "Soy contains phytoestrogens (plant compounds), not human estrogen. Studies show soy is safe and may reduce cancer risk. Dairy has actual mammalian estrogen though.";
  }
  
  // COST RESPONSES
  if (q.includes('expensive') || q.includes('afford') || q.includes('cost')) {
    return "Beans, rice, lentils, oats - the cheapest foods in any store. Meat is expensive and heavily subsidized. Vegan specialty products are optional.";
  }
  
  // Generic fallback
  return "The peer-reviewed research addresses this question. Check the sources above for detailed scientific evidence.";
};



  const keyFacts = extractKeyFacts();
  const prestigiousSources = extractPrestigiousSources();

  return (
    <div className="w-full max-w-4xl mx-auto space-y-4">
      {/* Key Facts */}
      <CollapsibleSection title="KEY FACTS" icon="📊" defaultOpen={true}>
        <div className="space-y-4">
          {keyFacts.map((fact, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: idx * 0.1 }}
              className="bg-navy-900/50 p-4 rounded-lg border-l-4 border-magenta-500"
            >
              <p className="text-white leading-relaxed">{fact}</p>
            </motion.div>
          ))}
        </div>
      </CollapsibleSection>

      {/* Sources */}
      <CollapsibleSection title="SOURCES" icon="🏆" defaultOpen={true}>
        <div className="space-y-3 mb-4">
          {prestigiousSources.length > 0 && (
            <div className="flex flex-wrap gap-2 mb-4">
              {prestigiousSources.map((source, idx) => (
                <span key={idx} className="px-3 py-1 bg-magenta-500/20 text-magenta-400 rounded-full text-sm border border-magenta-500/30">
                  {source}
                </span>
              ))}
            </div>
          )}
        </div>

        <div className="space-y-4">
          {sources.slice(0, 5).map((source, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.1 }}
              className="bg-navy-900/50 p-5 rounded-lg border border-navy-700 hover:border-magenta-500/30 transition-colors"
            >
              <div className="flex justify-between items-start mb-3">
                <h4 className="text-white font-semibold text-lg leading-tight flex-1">
                  {source.title}
                </h4>
                {source.link && (
                  <a
                    href={source.link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-magenta-500 hover:text-magenta-400 ml-3"
                  >
                    <FiExternalLink className="text-xl" />
                  </a>
                )}
              </div>

              <div className="flex gap-3 text-sm text-gray-400 mb-3">
                <span>{source.authors || 'Unknown'}</span>
                <span>•</span>
                <span>{source.year || 'N/A'}</span>
                <span>•</span>
                <span className="text-magenta-400">{source.journal || 'Unknown Journal'}</span>
              </div>

              {source.key_finding && (
                <div className="mb-3">
                  <p className="text-sm text-gray-400 mb-1">Key Finding:</p>
                  <p className="text-white">{source.key_finding}</p>
                </div>
              )}

              {source.direct_quote && (
                <div className="bg-navy-800/50 p-3 rounded border-l-2 border-magenta-500 mb-3">
                  <p className="text-gray-300 italic">"{source.direct_quote}"</p>
                </div>
              )}

              <div className="flex gap-2">
                {source.citation_apa && (
                  <button
                    onClick={() => copyToClipboard(source.citation_apa, `apa-${idx}`)}
                    className="btn-secondary text-xs flex items-center gap-1"
                  >
                    {copiedItems[`apa-${idx}`] ? <FiCheck /> : <FiCopy />}
                    {copiedItems[`apa-${idx}`] ? 'Copied APA' : 'Copy APA'}
                  </button>
                )}
                {source.citation_mla && (
                  <button
                    onClick={() => copyToClipboard(source.citation_mla, `mla-${idx}`)}
                    className="btn-secondary text-xs flex items-center gap-1"
                  >
                    {copiedItems[`mla-${idx}`] ? <FiCheck /> : <FiCopy />}
                    {copiedItems[`mla-${idx}`] ? 'Copied MLA' : 'Copy MLA'}
                  </button>
                )}
              </div>
            </motion.div>
          ))}
        </div>
      </CollapsibleSection>

      {/* Simple Explanation */}
      <CollapsibleSection title="SIMPLE EXPLANATION" icon="💡">
        <div className="prose prose-invert max-w-none">
          <p className="text-white leading-relaxed text-lg">
            {evidence.summary}
          </p>
        </div>
      </CollapsibleSection>

      {/* Common Questions */}
      {evidence.counterarguments && evidence.counterarguments.length > 0 && (
        <CollapsibleSection title="COMMON QUESTIONS" icon="❓">
          <div className="space-y-6">
            {evidence.counterarguments.map((counter, idx) => (
              <div key={idx} className="bg-navy-900/50 p-4 rounded-lg border-l-2 border-magenta-500/30">
                <p className="text-magenta-400 font-semibold mb-3 text-lg">Q: {counter}</p>
                <p className="text-white leading-relaxed">
                  <span className="font-semibold text-gray-300">A:</span> {generateCounterResponse(counter, sources)}
                </p>
              </div>
            ))}
          </div>
        </CollapsibleSection>
      )}

      {/* Full Academic Details */}
      <CollapsibleSection title="FULL ACADEMIC DETAILS" icon="📖">
        <div className="space-y-6">
          <div className="grid grid-cols-2 gap-4 mb-6">
            <div className="bg-navy-900/50 p-4 rounded-lg">
              <p className="text-gray-400 text-sm mb-1">Category</p>
              <p className="text-white font-semibold capitalize">{analysis?.category || 'General'}</p>
            </div>
            <div className="bg-navy-900/50 p-4 rounded-lg">
              <p className="text-gray-400 text-sm mb-1">Sources Found</p>
              <p className="text-white font-semibold">{sources.length} peer-reviewed</p>
            </div>
          </div>

          {sources.map((source, idx) => {
            const badge = getPrestigiousBadge(source.journal);
            const isPrest = isPrestigious(source.journal);
            
            return (
              <div 
                key={idx} 
                className={`bg-navy-900/50 p-5 rounded-lg border ${
                  isPrest ? 'border-magenta-500/40' : 'border-navy-700'
                } ${isPrest ? 'shadow-lg shadow-magenta-500/10' : ''}`}
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <h4 className="text-white font-semibold">{idx + 1}. {source.title}</h4>
                    </div>
                    
                    <div className="flex items-center gap-2 mb-2">
                      {badge && (
                        <span className="px-3 py-1 bg-gradient-to-r from-magenta-500/20 to-magenta-600/20 text-magenta-400 text-sm rounded-full border border-magenta-500/30 font-semibold flex items-center gap-1">
                          {badge}
                        </span>
                      )}
                      {!badge && (
                        <span className="text-magenta-400 text-sm font-medium">{source.journal}</span>
                      )}
                    </div>
                    
                    <p className="text-gray-400 text-sm">
                      {source.authors} ({source.year})
                    </p>
                  </div>
                </div>

                {source.abstract && (
                  <div className="mb-3">
                    <p className="text-gray-300 text-sm line-clamp-3">{source.abstract}</p>
                  </div>
                )}

                <div className="flex gap-2 flex-wrap">
                  <span className="px-2 py-1 bg-navy-800 text-gray-400 text-xs rounded">
                    {source.study_type || 'Research'}
                  </span>
                  {source.access_type && (
                    <span className="px-2 py-1 bg-navy-800 text-gray-400 text-xs rounded">
                      {source.access_type}
                    </span>
                  )}
                  {source.link && (
                    <a
                      href={source.link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="px-2 py-1 bg-magenta-500/20 text-magenta-400 text-xs rounded hover:bg-magenta-500/30 transition-colors flex items-center gap-1"
                    >
                      <FiExternalLink />
                      View Paper
                    </a>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </CollapsibleSection>
    </div>
  );
};

export default ResultsDisplay;