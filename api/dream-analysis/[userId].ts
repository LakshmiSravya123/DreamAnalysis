import type { VercelRequest, VercelResponse } from '@vercel/node';
import { getDb } from '../_lib/db';
import { success, error, methodNotAllowed } from '../_lib/response';
import { dreamAnalysis } from '../../shared/schema';
import { eq, desc } from 'drizzle-orm';

export default async function handler(req: VercelRequest, res: VercelResponse) {
  const { userId } = req.query;

  if (typeof userId !== 'string') {
    return error(res, 'Invalid user ID', 400);
  }

  if (req.method === 'GET') {
    try {
      const db = getDb();
      const analyses = await db
        .select()
        .from(dreamAnalysis)
        .where(eq(dreamAnalysis.userId, userId))
        .orderBy(desc(dreamAnalysis.timestamp))
        .limit(20);
      
      return success(res, analyses);
    } catch (err) {
      console.error('Error fetching dream analyses:', err);
      return error(res, 'Failed to fetch dream analyses');
    }
  }

  return methodNotAllowed(res, ['GET']);
}
