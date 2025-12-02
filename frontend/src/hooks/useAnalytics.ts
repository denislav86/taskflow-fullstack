import { useQuery } from '@tanstack/react-query';
import { analyticsService } from '@/services';

export function useAnalytics() {
  return useQuery({
    queryKey: ['analytics'],
    queryFn: () => analyticsService.getSummary(),
    staleTime: 1000 * 60 * 2, // 2 minutes
  });
}

