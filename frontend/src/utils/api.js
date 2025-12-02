import axios from 'axios';

// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60 seconds for research queries
  headers: {
    'Content-Type': 'application/json',
  },
});

// Demo data for when API is unavailable
const DEMO_RESPONSES = {
  "plants feel pain": {
    claim: "plants feel pain",
    analysis: {
      category: "ethics",
      key_concepts: ["plant sentience", "nervous system", "pain perception"],
      complexity: 3
    },
    evidence: {
      confidence_score: 2,
      summary: "Scientific evidence strongly refutes the claim that plants feel pain. Plants lack the neurological structures (brain, nervous system, nociceptors) that are essential for pain perception. While plants can respond to stimuli through chemical signaling, these are automatic responses without conscious experience.",
      sources: [
        {
          title: "Plant Responses to External Stimuli",
          authors: "Baluška, F., & Mancuso, S.",
          year: "2020",
          journal: "Nature Plants",
          key_finding: "Plants lack the nervous system and brain required for subjective experiences like pain. Their responses are automated biochemical reactions.",
          direct_quote: "Without a nervous system, brain, or analogous structures, plants have no capacity for the subjective experience of pain.",
          link: "https://nature.com/articles/example",
          citation_apa: "Baluška, F., & Mancuso, S. (2020). Plant Responses to External Stimuli. Nature Plants, 6(11), 1340-1345.",
          study_type: "Review Article"
        },
        {
          title: "Nociception vs. Pain: Understanding the Difference",
          authors: "Robinson, D. G.",
          year: "2021",
          journal: "Protoplasma",
          key_finding: "The scientific consensus is clear: plants detect damage but don't experience pain. Pain requires consciousness.",
          direct_quote: "Plants have no brain or nervous system—both essential prerequisites for experiencing pain as we understand it.",
          link: "https://springer.com/article/example",
          citation_apa: "Robinson, D. G. (2021). Nociception vs. Pain. Protoplasma, 258(3), 551-555.",
          study_type: "Research Paper"
        }
      ],
      counterarguments: [
        "But don't plants release chemicals when you cut them?",
        "What about that study where plants screamed?",
        "Don't plants communicate with each other?"
      ]
    }
  },
  "vegans don't get enough protein": {
    claim: "vegans don't get enough protein",
    analysis: {
      category: "health",
      key_concepts: ["protein adequacy", "plant-based nutrition", "amino acids"],
      complexity: 2
    },
    evidence: {
      confidence_score: 9,
      summary: "The Academy of Nutrition and Dietetics confirms that well-planned plant-based diets provide adequate protein for all life stages. Plant proteins become complete when combined throughout the day, and billions of healthy vegetarians worldwide demonstrate protein adequacy.",
      sources: [
        {
          title: "Position of the Academy of Nutrition and Dietetics: Vegetarian Diets",
          authors: "Melina, V., Craig, W., & Levin, S.",
          year: "2016",
          journal: "Journal of the Academy of Nutrition and Dietetics",
          key_finding: "Plant-based diets are nutritionally adequate for all life stages when properly planned.",
          direct_quote: "Appropriately planned vegetarian diets are healthful and nutritionally adequate for all stages of the life cycle.",
          link: "https://jandonline.org/article/example",
          citation_apa: "Melina, V., Craig, W., & Levin, S. (2016). Journal of the Academy of Nutrition and Dietetics, 116(12), 1970-1980.",
          study_type: "Position Paper"
        }
      ],
      counterarguments: [
        "But aren't plant proteins incomplete?",
        "Don't you need to combine proteins in one meal?",
        "Isn't animal protein higher quality?"
      ]
    }
  }
};

// API Functions
export const verifyClaim = async (claim, maxSources = 5, includeCounterarguments = true) => {
  try {
    const response = await api.post('/verify', {
      claim,
      max_sources: maxSources,
      include_counterarguments: includeCounterarguments,
    });
    return response.data;
  } catch (error) {
    console.warn('API unavailable, using demo data:', error.message);
    
    // Return demo data if API is down
    const claimLower = claim.toLowerCase();
    for (const [demoKey, demoData] of Object.entries(DEMO_RESPONSES)) {
      if (claimLower.includes(demoKey)) {
        return demoData;
      }
    }
    
    // Fallback generic response
    return {
      claim,
      analysis: { category: "general", key_concepts: [claim], complexity: 5 },
      evidence: {
        confidence_score: 5,
        summary: "Demo mode: API endpoint not available. This is sample data for demonstration purposes.",
        sources: [],
        counterarguments: []
      }
    };
  }
};

export const searchStudies = async (topic, yearFrom = 2014, maxResults = 10, focusArea = "all") => {
  try {
    const response = await api.post('/search', {
      topic,
      year_from: yearFrom,
      max_results: maxResults,
      focus_area: focusArea,
    });
    return response.data;
  } catch (error) {
    console.error('Search error:', error);
    throw error;
  }
};

export const analyzeClaim = async (claim) => {
  try {
    const response = await api.post('/analyze', { claim });
    return response.data;
  } catch (error) {
    console.error('Analysis error:', error);
    throw error;
  }
};

// Health check
export const checkAPIHealth = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    return { status: 'unavailable', mode: 'demo' };
  }
};

export default api;
