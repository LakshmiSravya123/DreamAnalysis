import type { VercelRequest, VercelResponse } from '@vercel/node';
import { getDb } from '../_lib/db';
import { getOpenAIClient } from '../_lib/openai';
import { success, error, methodNotAllowed, badRequest } from '../_lib/response';
import { dreamAnalysis } from '../../shared/schema';

export default async function handler(req: VercelRequest, res: VercelResponse) {
  if (req.method === 'POST') {
    try {
      const { dreamText, userId } = req.body;

      if (!dreamText || !userId) {
        return badRequest(res, 'Missing dreamText or userId');
      }

      const openai = getOpenAIClient();
      
      // Analyze dream with OpenAI
      // the newest OpenAI model is "gpt-5" which was released August 7, 2025. do not change this unless explicitly requested by the user
      const response = await openai.chat.completions.create({
        model: "gpt-5",
        messages: [
          {
            role: "system",
            content: "You are a dream analysis expert. Analyze the dream text and provide insights about symbols, emotions, and psychological meanings. Respond with JSON in this format: { 'symbols': string[], 'emotions': { 'emotion': string, 'intensity': number }[], 'analysis': string }"
          },
          {
            role: "user",
            content: `Analyze this dream: ${dreamText}`
          }
        ],
        response_format: { type: "json_object" }
      });

      const analysis = JSON.parse(response.choices[0].message.content || "{}");
      
      const db = getDb();
      const [newAnalysis] = await db
        .insert(dreamAnalysis)
        .values({
          userId,
          dreamText,
          symbols: analysis.symbols || [],
          emotions: analysis.emotions || [],
          aiAnalysis: analysis.analysis || ""
        })
        .returning();

      return success(res, newAnalysis, 201);
    } catch (err) {
      console.error('Error analyzing dream:', err);
      return error(res, 'Failed to analyze dream');
    }
  }

  return methodNotAllowed(res, ['POST']);
}
