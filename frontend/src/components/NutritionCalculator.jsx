import { useState } from 'react';
import { motion } from 'framer-motion';
import { FiCheck, FiCopy, FiInfo } from 'react-icons/fi';

const NutritionCalculator = () => {
  const [age, setAge] = useState('');
  const [gender, setGender] = useState('female');
  const [weight, setWeight] = useState('');
  const [nutrient, setNutrient] = useState('');
  const [customNutrient, setCustomNutrient] = useState('');
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [copiedResponse, setCopiedResponse] = useState(false);

  // Organized nutrient categories
  const nutrientCategories = {
    "Popular": [
      { id: 'omega-3', label: 'Omega-3', icon: '🐟' },
      { id: 'iron', label: 'Iron', icon: '🔴' },
      { id: 'protein', label: 'Protein', icon: '💪' },
      { id: 'vitamin-b12', label: 'B12', icon: '💊' },
      { id: 'calcium', label: 'Calcium', icon: '🦴' },
      { id: 'zinc', label: 'Zinc', icon: '⚡' },
    ],
    "Vitamins": [
      { id: 'vitamin-d', label: 'Vitamin D', icon: '☀️' },
      { id: 'vitamin-c', label: 'Vitamin C', icon: '🍊' },
      { id: 'vitamin-a', label: 'Vitamin A', icon: '🥕' },
      { id: 'vitamin-e', label: 'Vitamin E', icon: '🌰' },
      { id: 'vitamin-k', label: 'Vitamin K', icon: '🥬' },
      { id: 'folate', label: 'Folate (B9)', icon: '🍃' },
    ],
    "Minerals": [
      { id: 'magnesium', label: 'Magnesium', icon: '✨' },
      { id: 'selenium', label: 'Selenium', icon: '🌟' },
      { id: 'potassium', label: 'Potassium', icon: '🍌' },
      { id: 'iodine', label: 'Iodine', icon: '🧂' },
    ]
  };

  const handleCalculate = async () => {
    if (!age || !weight) {
      alert('Please enter your age and weight');
      return;
    }

    const selectedNutrient = customNutrient || nutrient;
    if (!selectedNutrient) {
      alert('Please select or enter a nutrient');
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/nutrition-calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          age: parseInt(age),
          gender,
          weight: parseFloat(weight),
          nutrient: selectedNutrient
        })
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error:', error);
      alert('Error calculating nutrition. Make sure backend is running.');
    } finally {
      setIsLoading(false);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    setCopiedResponse(true);
    setTimeout(() => setCopiedResponse(false), 2000);
  };

  const handleQuickSelect = (nutrientId) => {
    setNutrient(nutrientId);
    setCustomNutrient('');
  };

  const getPracticalContext = (food, dailyNeed) => {
    const percentage = (food.amount / dailyNeed) * 100;
    
    if (percentage >= 100) {
      return `One serving exceeds your daily need!`;
    } else if (percentage >= 80) {
      return `One serving covers most of your daily ${result.nutrient}!`;
    } else if (percentage >= 50) {
      return `Two servings cover your full daily need`;
    } else if (percentage >= 33) {
      return `Three servings throughout the day = full daily need`;
    } else if (percentage >= 25) {
      return `Four servings spread throughout the day = full daily need`;
    } else {
      return `Great addition to boost your ${result.nutrient} intake`;
    }
  };

  const getPercentage = (amount, dailyNeed) => {
    return Math.min(Math.round((amount / dailyNeed) * 100), 100);
  };

  return (
    <div className="w-full max-w-4xl mx-auto">
      {/* Calculator Card */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-card p-8 mb-6"
      >
        <div className="flex items-center gap-3 mb-6">
          <span className="text-4xl">🥗</span>
          <div>
            <h2 className="text-3xl font-display font-bold gradient-text">
              VEGAN NUTRITION CALCULATOR
            </h2>
            <p className="text-gray-400 mt-1">Get personalized daily nutrition needs</p>
          </div>
        </div>

        {/* User Info Input */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div>
            <label className="block text-gray-400 text-sm mb-2">Age</label>
            <input
              type="number"
              value={age}
              onChange={(e) => setAge(e.target.value)}
              placeholder="27"
              className="w-full bg-navy-900 border border-navy-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-magenta-500"
              min="18"
              max="100"
            />
          </div>

          <div>
            <label className="block text-gray-400 text-sm mb-2">Gender</label>
            <select
              value={gender}
              onChange={(e) => setGender(e.target.value)}
              className="w-full bg-navy-900 border border-navy-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-magenta-500"
            >
              <option value="female">Female</option>
              <option value="male">Male</option>
            </select>
          </div>

          <div>
            <label className="block text-gray-400 text-sm mb-2">Weight (kg)</label>
            <input
              type="number"
              value={weight}
              onChange={(e) => setWeight(e.target.value)}
              placeholder="50"
              className="w-full bg-navy-900 border border-navy-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-magenta-500"
              min="30"
              max="200"
              step="0.1"
            />
          </div>
        </div>

        {/* Quick Pick Nutrients - Organized by Category */}
        {Object.entries(nutrientCategories).map(([category, nutrients]) => (
          <div key={category} className="mb-4">
            <label className="block text-gray-400 text-sm mb-2">{category}:</label>
            <div className="flex flex-wrap gap-2">
              {nutrients.map((n) => (
                <button
                  key={n.id}
                  onClick={() => handleQuickSelect(n.id)}
                  className={`px-4 py-2 rounded-lg transition-all ${
                    nutrient === n.id && !customNutrient
                      ? 'bg-magenta-500 text-white'
                      : 'bg-navy-800 text-gray-300 hover:bg-navy-700'
                  }`}
                >
                  {n.icon} {n.label}
                </button>
              ))}
            </div>
          </div>
        ))}

        {/* Custom Nutrient Input */}
        <div className="mb-6">
          <label className="block text-gray-400 text-sm mb-2">Or enter any nutrient:</label>
          <input
            type="text"
            value={customNutrient}
            onChange={(e) => {
              setCustomNutrient(e.target.value);
              setNutrient('');
            }}
            placeholder="e.g., Vitamin B6, Niacin, Thiamin, Riboflavin..."
            className="w-full bg-navy-900 border border-navy-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-magenta-500"
          />
        </div>

        {/* Calculate Button */}
        <button
          onClick={handleCalculate}
          disabled={isLoading}
          className="w-full btn-primary text-lg py-4"
        >
          {isLoading ? 'Calculating...' : '🔍 Calculate My Needs'}
        </button>

        {/* Disclaimer */}
        <div className="mt-4 flex items-start gap-2 text-xs text-gray-500">
          <FiInfo className="mt-0.5 flex-shrink-0" />
          <p>For educational purposes. Consult healthcare provider for personalized advice.</p>
        </div>
      </motion.div>

      {/* Results */}
      {result && !result.error && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-4"
        >
          {/* Daily Need Card */}
          <div className="glass-card p-6 border-2 border-magenta-500/30">
            <h3 className="text-2xl font-display font-bold text-white mb-4 flex items-center gap-2">
              🎯 Your Daily Need
            </h3>
            <div className="bg-navy-900/50 p-6 rounded-lg">
              <p className="text-gray-400 mb-2">
                {result.profile.age} year old {result.profile.gender}, {result.profile.weight}kg
              </p>
              <p className="text-4xl font-bold text-magenta-500 mb-2">
                {result.daily_need} {result.unit}
              </p>
              <p className="text-gray-300 capitalize">{result.nutrient} per day</p>
              {result.notes && (
                <p className="text-sm text-gray-400 mt-3 italic">
                  💡 {result.notes}
                </p>
              )}
            </div>
          </div>

          {/* Food Options */}
          <div className="glass-card p-6">
            <h3 className="text-2xl font-display font-bold text-white mb-4 flex items-center gap-2">
              🥄 Easy Ways to Get It
            </h3>
            <div className="space-y-4">
              {result.food_options.map((food, idx) => {
                const percentage = getPercentage(food.amount, result.daily_need);
                
                return (
                  <div
                    key={idx}
                    className="bg-navy-900/50 p-5 rounded-lg border-l-4 border-magenta-500 hover:bg-navy-800/50 transition-colors"
                  >
                    {/* Food name and progress bar row */}
                    <div className="flex items-center justify-between gap-4 mb-2">
                      <div className="flex-1">
                        <h4 className="text-white font-semibold text-lg">
                          {food.name}
                        </h4>
                        <p className="text-gray-400 text-sm">{food.serving}</p>
                      </div>
                      
                      {/* Amount and progress bar */}
                      <div className="flex items-center gap-3 min-w-[200px]">
                        <span className="text-magenta-400 font-bold text-lg">
                          {food.amount}{result.unit}
                        </span>
                        
                        {/* Progress bar */}
                        <div className="flex-1 min-w-[100px]">
                          <div className="w-full bg-navy-800 rounded-full h-3 overflow-hidden">
                            <div
                              className="h-full bg-gradient-to-r from-magenta-500 to-accent-pink transition-all duration-500"
                              style={{ width: `${percentage}%` }}
                            />
                          </div>
                        </div>
                        
                        <span className="text-gray-400 font-bold text-lg min-w-[60px]">
                          {result.daily_need}{result.unit}
                        </span>
                      </div>
                    </div>

                    {/* Percentage */}
                    <div className="text-right mb-3">
                      <span className="text-magenta-400 font-semibold text-sm">
                        {percentage}%
                      </span>
                    </div>

                    {/* Practical context */}
                    <p className="text-green-400 font-semibold mb-3 flex items-center gap-2">
                      <span>✅</span>
                      <span>{getPracticalContext(food, result.daily_need)}</span>
                    </p>

                    {/* Tips */}
                    {food.tips && (
                      <p className="text-gray-300 text-sm mb-2 flex items-start gap-2">
                        <span>💡</span>
                        <span>{food.tips}</span>
                      </p>
                    )}

                    {/* Versatility */}
                    {food.versatility && (
                      <p className="text-gray-400 text-xs flex items-start gap-2">
                        <span>📌</span>
                        <span>Use in: {food.versatility}</span>
                      </p>
                    )}
                  </div>
                );
              })}
            </div>

            {/* Combination tip */}
            {result.food_options.length > 1 && (
              <div className="mt-4 bg-navy-800/50 p-4 rounded-lg border border-magenta-500/30">
                <p className="text-magenta-400 font-semibold mb-2">💡 Mix & Match Tip:</p>
                <p className="text-gray-300 text-sm">
                  You don't need to get all your {result.nutrient} from one food! 
                  Combine different sources throughout the day for variety and better nutrition.
                </p>
              </div>
            )}
          </div>

          {/* Additional Tips */}
          {result.tips && Object.keys(result.tips).length > 0 && (
            <div className="glass-card p-6">
              <h3 className="text-xl font-display font-bold text-white mb-4 flex items-center gap-2">
                💡 Pro Tips
              </h3>
              <div className="space-y-3 text-gray-300">
                {result.tips.tip && (
                  <p className="bg-navy-900/50 p-3 rounded-lg">{result.tips.tip}</p>
                )}
                {result.tips.enhancers && (
                  <p className="text-sm text-gray-400">
                    ✅ Better absorption with: {result.tips.enhancers.join(', ')}
                  </p>
                )}
                {result.tips.inhibitors && (
                  <p className="text-sm text-gray-400">
                    ⚠️ Reduce absorption: {result.tips.inhibitors.join(', ')}
                  </p>
                )}
              </div>
            </div>
          )}

          {/* Sources */}
          <div className="glass-card p-4">
            <p className="text-gray-400 text-sm">
              📚 RDA sources: {result.official_sources.join(', ')}
            </p>
          </div>
        </motion.div>
      )}

      {/* Error Message */}
      {result && result.error && (
        <div className="glass-card p-6 border-2 border-accent-red bg-accent-red/10">
          <p className="text-white mb-2">⚠️ {result.error}</p>
          {result.available_nutrients && (
            <div className="mt-3">
              <p className="text-gray-400 text-sm mb-2">Available nutrients:</p>
              <div className="flex flex-wrap gap-2">
                {result.available_nutrients.map((n) => (
                  <span key={n} className="px-2 py-1 bg-navy-800 text-gray-300 text-xs rounded">
                    {n}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default NutritionCalculator;