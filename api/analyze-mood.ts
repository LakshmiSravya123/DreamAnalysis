import type { VercelRequest, VercelResponse } from '@vercel/node';
import { getOpenAIClient } from './_lib/openai';
import { success, error, methodNotAllowed, badRequest } from './_lib/response';

export default async function handler(req: VercelRequest, res: VercelResponse) {
  if (req.method === 'POST') {
    try {
      const { text, userId } = req.body;

      if (!text) {
        return badRequest(res, 'Missing text to analyze');
      }

      const openai = getOpenAIClient();
      
      // the newest OpenAI model is "gpt-5" which was released August 7, 2025. do not change this unless explicitly requested by the user
      const response = await openai.chat.completions.create({
        model: "gpt-5",
        messages: [
          {
            role: "system",
            content: "Analyze the mood and emotional state from the text. Provide insights about stress levels, emotional patterns, and wellness recommendations. Respond with JSON in this format: { 'mood': string, 'stressLevel': number, 'emotions': string[], 'recommendations': string[] }"
          },
          {
            role: "user",
            content: text
          }
        ],
        response_format: { type: "json_object" }
      });

      const analysis = JSON.parse(response.choices[0].message.content || "{}");
      return success(res, analysis);
    } catch (err) {
      console.error('Error analyzing mood:', err);
      return error(res, 'Failed to analyze mood');
    }
  }

  return methodNotAllowed(res, ['POST']);
}
