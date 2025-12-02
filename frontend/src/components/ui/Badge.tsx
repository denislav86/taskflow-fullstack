import { clsx } from 'clsx';
import type { TaskStatus, TaskPriority } from '@/types';

interface BadgeProps {
  variant: TaskStatus | TaskPriority;
  children: React.ReactNode;
}

const statusLabels: Record<TaskStatus, string> = {
  todo: 'To Do',
  in_progress: 'In Progress',
  done: 'Done',
};

const priorityLabels: Record<TaskPriority, string> = {
  low: 'Low',
  medium: 'Medium',
  high: 'High',
};

export function Badge({ variant, children }: BadgeProps) {
  const variantClasses: Record<string, string> = {
    todo: 'badge-todo',
    in_progress: 'badge-in-progress',
    done: 'badge-done',
    low: 'badge-low',
    medium: 'badge-medium',
    high: 'badge-high',
  };

  return (
    <span className={clsx('badge', variantClasses[variant])}>
      {children}
    </span>
  );
}

export function StatusBadge({ status }: { status: TaskStatus }) {
  return <Badge variant={status}>{statusLabels[status]}</Badge>;
}

export function PriorityBadge({ priority }: { priority: TaskPriority }) {
  return <Badge variant={priority}>{priorityLabels[priority]}</Badge>;
}

export default Badge;

