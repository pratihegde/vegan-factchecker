import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FiChevronDown, FiChevronUp } from 'react-icons/fi';

const CollapsibleSection = ({ 
  title, 
  icon, 
  children, 
  defaultOpen = false,
  headerColor = 'magenta-500' 
}) => {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-card mb-4 overflow-hidden"
    >
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between p-6 hover:bg-navy-700/30 transition-colors"
      >
        <div className="flex items-center gap-3">
          <span className="text-2xl">{icon}</span>
          <h3 className={`text-xl font-display font-semibold text-${headerColor}`}>
            {title}
          </h3>
        </div>
        
        <motion.div
          animate={{ rotate: isOpen ? 180 : 0 }}
          transition={{ duration: 0.2 }}
        >
          <FiChevronDown className="text-2xl text-gray-400" />
        </motion.div>
      </button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3 }}
            className="overflow-hidden"
          >
            <div className="px-6 pb-6 pt-2 border-t border-navy-700">
              {children}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};

export default CollapsibleSection;
