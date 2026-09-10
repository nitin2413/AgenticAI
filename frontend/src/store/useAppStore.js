import { create } from 'zustand';

const DEMO_EMAIL = 'admin@nass.ai';
const DEMO_PASSWORD = 'nass2024';

// Helper to get api keys from localStorage
const getStoredKey = (provider) => {
  return localStorage.getItem(`ai_agent_key_${provider}`) || '';
};

// Helper to save api keys to localStorage
const storeKey = (provider, key) => {
  localStorage.setItem(`ai_agent_key_${provider}`, key);
};

const getStoredUser = () => {
  try {
    const raw = localStorage.getItem('nass_auth_user');
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
};

const storeUser = (user) => {
  if (user) {
    localStorage.setItem('nass_auth_user', JSON.stringify(user));
  } else {
    localStorage.removeItem('nass_auth_user');
  }
};

export const useAppStore = create((set, get) => ({
  user: getStoredUser(),
  isAuthenticated: !!getStoredUser(),

  activeSection: 'chat', // 'rag', 'chat', 'gmail', 'coding'
  activeProvider: 'openai', // 'openai', 'anthropic', 'google', 'groq', 'openrouter', 'ollama'
  modelName: 'gpt-4o-mini',
  apiKey: getStoredKey('openai'),
  ollamaBaseUrl: 'http://localhost:11434',
  gmailConnected: false,
  agentMode: false,
  systemPrompt: 'You are an advanced Orchestrator Agent. You have dynamic access to sub-agents (RAG, Gmail) to retrieve knowledge and execute tasks. Be direct, helpful, and concise.',
  
  // Auth
  login: async (email, password, remember = true) => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email.trim(), password })
      });
      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Invalid email or password.');
      }
      const user = await response.json();
      if (remember) {
        storeUser(user);
      }
      set({ user, isAuthenticated: true });
      return { success: true };
    } catch (err) {
      return { success: false, error: err.message };
    }
  },

  signup: async (name, email, password) => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/auth/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: name.trim(), email: email.trim().toLowerCase(), password })
      });
      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Sign up failed.');
      }
      const user = await response.json();
      storeUser(user);
      set({ user, isAuthenticated: true });
      return { success: true };
    } catch (err) {
      return { success: false, error: err.message };
    }
  },

  loginWithGoogle: async (googleUser) => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/auth/google', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: googleUser.email,
          name: googleUser.name,
          picture: googleUser.picture
        })
      });
      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Google authentication sync failed.');
      }
      const user = await response.json();
      storeUser(user);
      set({ user, isAuthenticated: true });
      return { success: true };
    } catch (err) {
      console.error("Google login backend sync error:", err);
      // Fallback: authenticates locally on frontend anyway so the user is not locked out
      storeUser(googleUser);
      set({ user: googleUser, isAuthenticated: true });
      return { success: true };
    }
  },

  logout: () => {
    storeUser(null);
    set({ user: null, isAuthenticated: false });
  },

  // Navigation
  setActiveSection: (section) => set({ activeSection: section }),
  
  // LLM Config
  setActiveProvider: (provider) => {
    let defaultModel = 'gpt-4o-mini';
    if (provider === 'anthropic') defaultModel = 'claude-3-5-sonnet-20240620';
    if (provider === 'google') defaultModel = 'gemini-1.5-pro';
    if (provider === 'groq') defaultModel = 'llama3-8b-8192';
    if (provider === 'openrouter') defaultModel = 'meta-llama/llama-3-8b-instruct:free';
    if (provider === 'ollama') defaultModel = 'llama3';

    set({ 
      activeProvider: provider,
      apiKey: getStoredKey(provider),
      modelName: defaultModel
    });
  },
  
  setModelName: (modelName) => set({ modelName }),
  
  setApiKey: (key) => {
    const provider = get().activeProvider;
    storeKey(provider, key);
    set({ apiKey: key });
  },
  
  setOllamaBaseUrl: (url) => set({ ollamaBaseUrl: url }),
  setGmailConnected: (connected) => set({ gmailConnected: connected }),
  setAgentMode: (mode) => set({ agentMode: mode }),
  setSystemPrompt: (prompt) => set({ systemPrompt: prompt }),
}));
