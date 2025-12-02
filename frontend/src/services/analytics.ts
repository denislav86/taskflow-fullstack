import api from './api';
import type { AnalyticsSummary } from '@/types';

export const analyticsService = {
  async getSummary(): Promise<AnalyticsSummary> {
    const response = await api.get<AnalyticsSummary>('/analytics/summary');
    return response.data;
  },
};

export default analyticsService;

