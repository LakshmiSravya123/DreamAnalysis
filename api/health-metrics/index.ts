import type { VercelRequest, VercelResponse } from '@vercel/node';
import { getDb } from '../_lib/db';
import { success, error, methodNotAllowed, badRequest } from '../_lib/response';
import { healthMetrics, insertHealthMetricsSchema } from '../../shared/schema';

export default async function handler(req: VercelRequest, res: VercelResponse) {
  if (req.method === 'POST') {
    try {
      const validatedData = insertHealthMetricsSchema.parse(req.body);
      const db = getDb();
      
      const [newMetrics] = await db
        .insert(healthMetrics)
        .values(validatedData)
        .returning();
      
      return success(res, newMetrics, 201);
    } catch (err: any) {
      console.error('Error creating health metrics:', err);
      if (err.name === 'ZodError') {
        return badRequest(res, 'Invalid health metrics data');
      }
      return error(res, 'Failed to create health metrics');
    }
  }

  return methodNotAllowed(res, ['POST']);
}
