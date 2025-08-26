import { type User, type InsertUser, type HealthMetrics, type InsertHealthMetrics, type DreamAnalysis, type InsertDreamAnalysis, type AiChat, type InsertAiChat, type UserSettings, type InsertUserSettings } from "@shared/schema";
import { randomUUID } from "crypto";

export interface IStorage {
  getUser(id: string): Promise<User | undefined>;
  getUserByUsername(username: string): Promise<User | undefined>;
  createUser(user: InsertUser): Promise<User>;
  getHealthMetrics(userId: string, limit?: number): Promise<HealthMetrics[]>;
  createHealthMetrics(metrics: InsertHealthMetrics): Promise<HealthMetrics>;
  getDreamAnalyses(userId: string, limit?: number): Promise<DreamAnalysis[]>;
  createDreamAnalysis(analysis: InsertDreamAnalysis): Promise<DreamAnalysis>;
  getAiChats(userId: string, limit?: number): Promise<AiChat[]>;
  createAiChat(chat: InsertAiChat): Promise<AiChat>;
  getUserSettings(userId: string): Promise<UserSettings | undefined>;
  updateUserSettings(userId: string, settings: Partial<InsertUserSettings>): Promise<UserSettings>;
}

export class MemStorage implements IStorage {
  private users: Map<string, User>;
  private healthMetrics: Map<string, HealthMetrics>;
  private dreamAnalyses: Map<string, DreamAnalysis>;
  private aiChats: Map<string, AiChat>;
  private userSettings: Map<string, UserSettings>;

  constructor() {
    this.users = new Map();
    this.healthMetrics = new Map();
    this.dreamAnalyses = new Map();
    this.aiChats = new Map();
    this.userSettings = new Map();
  }

  async getUser(id: string): Promise<User | undefined> {
    return this.users.get(id);
  }

  async getUserByUsername(username: string): Promise<User | undefined> {
    return Array.from(this.users.values()).find(
      (user) => user.username === username,
    );
  }

  async createUser(insertUser: InsertUser): Promise<User> {
    const id = randomUUID();
    const user: User = { ...insertUser, id };
    this.users.set(id, user);
    return user;
  }

  async getHealthMetrics(userId: string, limit = 50): Promise<HealthMetrics[]> {
    return Array.from(this.healthMetrics.values())
      .filter(metric => metric.userId === userId)
      .sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())
      .slice(0, limit);
  }

  async createHealthMetrics(insertMetrics: InsertHealthMetrics): Promise<HealthMetrics> {
    const id = randomUUID();
    const metrics: HealthMetrics = { 
      ...insertMetrics, 
      id, 
      timestamp: new Date(),
      userId: insertMetrics.userId || null,
      dailySteps: insertMetrics.dailySteps || null,
      sleepDuration: insertMetrics.sleepDuration || null
    };
    this.healthMetrics.set(id, metrics);
    return metrics;
  }

  async getDreamAnalyses(userId: string, limit = 20): Promise<DreamAnalysis[]> {
    return Array.from(this.dreamAnalyses.values())
      .filter(analysis => analysis.userId === userId)
      .sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())
      .slice(0, limit);
  }

  async createDreamAnalysis(insertAnalysis: InsertDreamAnalysis): Promise<DreamAnalysis> {
    const id = randomUUID();
    const analysis: DreamAnalysis = { 
      ...insertAnalysis, 
      id, 
      timestamp: new Date(),
      userId: insertAnalysis.userId || null,
      symbols: insertAnalysis.symbols || [],
      emotions: insertAnalysis.emotions || [],
      aiAnalysis: insertAnalysis.aiAnalysis || null
    };
    this.dreamAnalyses.set(id, analysis);
    return analysis;
  }

  async getAiChats(userId: string, limit = 50): Promise<AiChat[]> {
    return Array.from(this.aiChats.values())
      .filter(chat => chat.userId === userId)
      .sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime())
      .slice(-limit);
  }

  async createAiChat(insertChat: InsertAiChat): Promise<AiChat> {
    const id = randomUUID();
    const chat: AiChat = { 
      ...insertChat, 
      id, 
      timestamp: new Date(),
      userId: insertChat.userId || null
    };
    this.aiChats.set(id, chat);
    return chat;
  }

  async getUserSettings(userId: string): Promise<UserSettings | undefined> {
    return Array.from(this.userSettings.values()).find(settings => settings.userId === userId);
  }

  async updateUserSettings(userId: string, partialSettings: Partial<InsertUserSettings>): Promise<UserSettings> {
    const existing = await this.getUserSettings(userId);
    const id = existing?.id || randomUUID();
    const settings: UserSettings = {
      id,
      userId,
      theme: "dark",
      electrodeCount: 64,
      samplingRate: 500,
      alertThresholds: {},
      animationsEnabled: true,
      ...existing,
      ...partialSettings,
    };
    this.userSettings.set(id, settings);
    return settings;
  }
}

export const storage = new MemStorage();
