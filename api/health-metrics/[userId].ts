import type { VercelRequest, VercelResponse } from '@vercel/node';
import { getDb } from '../_lib/db';
import { success, error, methodNotAllowed } from '../_lib/response';
import { healthMetrics } from '../../shared/schema';
import { eq, desc } from 'drizzle-orm';

export default async function handler(req: VercelRequest, res: VercelResponse) {
  const { userId } = req.query;

  if (typeof userId !== 'string') {
    return error(res, 'Invalid user ID', 400);
  }

  if (req.method === 'GET') {
    try {
      const db = getDb();
      const metrics = await db
        .select()
        .from(healthMetrics)
        .where(eq(healthMetrics.userId, userId))
        .orderBy(desc(healthMetrics.timestamp))
        .limit(50);
      
      return success(res, metrics);
    } catch (err) {
      console.error('Error fetching health metrics:', err);
      return error(res, 'Failed to fetch health metrics');
    }
  }

  return methodNotAllowed(res, ['GET']);
}
