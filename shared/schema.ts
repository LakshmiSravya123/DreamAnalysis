import { sql } from "drizzle-orm";
import { pgTable, text, varchar, integer, jsonb, timestamp, real, boolean } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

export const users = pgTable("users", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  username: text("username").notNull().unique(),
  password: text("password").notNull(),
});

export const healthMetrics = pgTable("health_metrics", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  userId: varchar("user_id").references(() => users.id),
  heartRate: integer("heart_rate").notNull(),
  stressLevel: integer("stress_level").notNull(),
  sleepQuality: integer("sleep_quality").notNull(),
  neuralActivity: integer("neural_activity").notNull(),
  dailySteps: integer("daily_steps"),
  sleepDuration: real("sleep_duration"),
  timestamp: timestamp("timestamp").defaultNow().notNull(),
});

export const dreamAnalysis = pgTable("dream_analysis", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  userId: varchar("user_id").references(() => users.id),
  dreamText: text("dream_text").notNull(),
  symbols: jsonb("symbols"),
  emotions: jsonb("emotions"),
  aiAnalysis: text("ai_analysis"),
  timestamp: timestamp("timestamp").defaultNow().notNull(),
});

export const aiChats = pgTable("ai_chats", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  userId: varchar("user_id").references(() => users.id),
  message: text("message").notNull(),
  isUser: boolean("is_user").notNull(),
  timestamp: timestamp("timestamp").defaultNow().notNull(),
});

export const userSettings = pgTable("user_settings", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  userId: varchar("user_id").references(() => users.id).unique(),
  theme: text("theme").default("dark"),
  electrodeCount: integer("electrode_count").default(64),
  samplingRate: integer("sampling_rate").default(500),
  alertThresholds: jsonb("alert_thresholds"),
  animationsEnabled: boolean("animations_enabled").default(true),
});

export const insertUserSchema = createInsertSchema(users).pick({
  username: true,
  password: true,
});

export const insertHealthMetricsSchema = createInsertSchema(healthMetrics).omit({
  id: true,
  timestamp: true,
});

export const insertDreamAnalysisSchema = createInsertSchema(dreamAnalysis).omit({
  id: true,
  timestamp: true,
});

export const insertAiChatSchema = createInsertSchema(aiChats).omit({
  id: true,
  timestamp: true,
});

export const insertUserSettingsSchema = createInsertSchema(userSettings).omit({
  id: true,
});

export type InsertUser = z.infer<typeof insertUserSchema>;
export type User = typeof users.$inferSelect;
export type HealthMetrics = typeof healthMetrics.$inferSelect;
export type InsertHealthMetrics = z.infer<typeof insertHealthMetricsSchema>;
export type DreamAnalysis = typeof dreamAnalysis.$inferSelect;
export type InsertDreamAnalysis = z.infer<typeof insertDreamAnalysisSchema>;
export type AiChat = typeof aiChats.$inferSelect;
export type InsertAiChat = z.infer<typeof insertAiChatSchema>;
export type UserSettings = typeof userSettings.$inferSelect;
export type InsertUserSettings = z.infer<typeof insertUserSettingsSchema>;
