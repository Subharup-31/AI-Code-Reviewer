import { createGoogleGenerativeAI } from '@ai-sdk/google';
import { createOpenAI } from '@ai-sdk/openai';

// Google Gemini configurations
const google1 = createGoogleGenerativeAI({
    apiKey: process.env.GOOGLE_GENERATIVE_AI_API_KEY || '',
});

const google2 = createGoogleGenerativeAI({
    apiKey: process.env.GOOGLE_GENERATIVE_AI_API_KEY_2 || '',
});

// OpenRouter configuration for the fallback model
const openRouter = createOpenAI({
    baseURL: 'https://openrouter.ai/api/v1',
    apiKey: process.env.OPENROUTER_API_KEY || '',
});

// Log configuration status (only runs once at startup)
if (process.env.NODE_ENV !== 'production') {
    console.log('\n=== LLM Configuration ===');
    console.log('[LLM Config] Primary Gemini key:', process.env.GOOGLE_GENERATIVE_AI_API_KEY ? `✅ Set (${process.env.GOOGLE_GENERATIVE_AI_API_KEY.substring(0, 20)}...)` : '❌ Missing');
    console.log('[LLM Config] Secondary Gemini key:', process.env.GOOGLE_GENERATIVE_AI_API_KEY_2 ? `✅ Set (${process.env.GOOGLE_GENERATIVE_AI_API_KEY_2.substring(0, 20)}...)` : '❌ Missing');
    console.log('[LLM Config] OpenRouter key:', process.env.OPENROUTER_API_KEY ? `✅ Set (${process.env.OPENROUTER_API_KEY.substring(0, 20)}...)` : '❌ Missing');
    console.log('[LLM Config] Keys are identical:', process.env.GOOGLE_GENERATIVE_AI_API_KEY === process.env.GOOGLE_GENERATIVE_AI_API_KEY_2 ? '⚠️ YES (secondary won\'t help)' : '✅ NO (good)');
    console.log('========================\n');
}

// Primary model: Google Gemini 2.5 Flash
export const primaryModel = google1('gemini-2.5-flash');

// Secondary model: Google Gemini 2.5 Flash (with different key)
export const secondaryModel = google2('gemini-2.5-flash');

// Fallback model: OpenRouter with a working free model
export const fallbackModel = openRouter('meta-llama/llama-3.2-3b-instruct:free');
