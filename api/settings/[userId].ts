import type { VercelRequest, VercelResponse } from '@vercel/node';
import { getDb } from '../_lib/db';
import { success, error, methodNotAllowed, badRequest } from '../_lib/response';
import { userSettings, insertUserSettingsSchema } from '../../shared/schema';
import { eq } from 'drizzle-orm';

export default async function handler(req: VercelRequest, res: VercelResponse) {
  const { userId } = req.query;

  if (typeof userId !== 'string') {
    return error(res, 'Invalid user ID', 400);
  }

  const db = getDb();

  if (req.method === 'GET') {
    try {
      const [settings] = await db
        .select()
        .from(userSettings)
        .where(eq(userSettings.userId, userId))
        .limit(1);
      
      return success(res, settings || null);
    } catch (err) {
      console.error('Error fetching settings:', err);
      return error(res, 'Failed to fetch settings');
    }
  }

  if (req.method === 'POST' || req.method === 'PUT') {
    try {
      const validatedData = insertUserSettingsSchema.parse(req.body);
      
      // Check if settings exist
      const [existing] = await db
        .select()
        .from(userSettings)
        .where(eq(userSettings.userId, userId))
        .limit(1);

      let result;
      if (existing) {
        // Update existing settings
        [result] = await db
          .update(userSettings)
          .set(validatedData)
          .where(eq(userSettings.userId, userId))
          .returning();
      } else {
        // Insert new settings
        [result] = await db
          .insert(userSettings)
          .values({ ...validatedData, userId })
          .returning();
      }
      
      return success(res, result);
    } catch (err: any) {
      console.error('Error updating settings:', err);
      if (err.name === 'ZodError') {
        return badRequest(res, 'Invalid settings data');
      }
      return error(res, 'Failed to update settings');
    }
  }

  return methodNotAllowed(res, ['GET', 'POST', 'PUT']);
}
