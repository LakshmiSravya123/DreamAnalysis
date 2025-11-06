import type { VercelRequest, VercelResponse } from '@vercel/node';
import { getDb } from '../_lib/db';
import { error, methodNotAllowed } from '../_lib/response';
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
        .orderBy(desc(healthMetrics.timestamp));
      
      // Convert to CSV format
      const csvData = metrics.map(m => ({
        timestamp: m.timestamp,
        heartRate: m.heartRate,
        stressLevel: m.stressLevel,
        sleepQuality: m.sleepQuality,
        neuralActivity: m.neuralActivity,
        dailySteps: m.dailySteps,
        sleepDuration: m.sleepDuration
      }));

      res.setHeader('Content-Type', 'text/csv');
      res.setHeader('Content-Disposition', 'attachment; filename=neural_data.csv');
      
      // Simple CSV conversion
      if (csvData.length === 0) {
        return res.send('No data available');
      }

      const csvHeader = Object.keys(csvData[0]).join(',');
      const csvRows = csvData.map(row => Object.values(row).join(','));
      const csvContent = [csvHeader, ...csvRows].join('\n');
      
      return res.send(csvContent);
    } catch (err) {
      console.error('Error exporting data:', err);
      return error(res, 'Failed to export data');
    }
  }

  return methodNotAllowed(res, ['GET']);
}
