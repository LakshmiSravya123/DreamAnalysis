import type { VercelRequest, VercelResponse } from '@vercel/node';
import { getDb } from '../_lib/db';
import { getOpenAIClient } from '../_lib/openai';
import { success, error, methodNotAllowed, badRequest } from '../_lib/response';
import { aiChat, healthMetrics } from '../../shared/schema';
import { eq, desc } from 'drizzle-orm';

export default async function handler(req: VercelRequest, res: VercelResponse) {
  if (req.method === 'POST') {
    try {
      const { message, userId } = req.body;

      if (!message || !userId) {
        return badRequest(res, 'Missing message or userId');
      }

      const db = getDb();
      
      // Store user message
      await db.insert(aiChat).values({
        userId,
        message,
        isUser: true
      });

      // Get recent health metrics for context
      const recentMetrics = await db
        .select()
        .from(healthMetrics)
        .where(eq(healthMetrics.userId, userId))
        .orderBy(desc(healthMetrics.timestamp))
        .limit(5);

      const healthContext = recentMetrics.length > 0 ? 
        `Recent health data: Heart rate ${recentMetrics[0].heartRate}, Stress level ${recentMetrics[0].stressLevel}, Sleep quality ${recentMetrics[0].sleepQuality}` : 
        "";

      const openai = getOpenAIClient();
      
      // Generate AI response
      // the newest OpenAI model is "gpt-5" which was released August 7, 2025. do not change this unless explicitly requested by the user
      const response = await openai.chat.completions.create({
        model: "gpt-5",
        messages: [
          {
            role: "system",
            content: `You are an AI wellness companion for a Brain-Computer Interface system. You help users with mood analysis, stress relief, and wellness guidance. ${healthContext} Be supportive, insightful, and provide actionable advice. Keep responses concise but meaningful.`
          },
          {
            role: "user",
            content: message
          }
        ]
      });

      const aiResponse = response.choices[0].message.content || "I'm here to help you with your wellness journey.";
      
      // Store AI response
      const [newChat] = await db
        .insert(aiChat)
        .values({
          userId,
          message: aiResponse,
          isUser: false
        })
        .returning();

      return success(res, newChat, 201);
    } catch (err) {
      console.error('Error processing chat message:', err);
      return error(res, 'Failed to process chat message');
    }
  }

  return methodNotAllowed(res, ['POST']);
}
