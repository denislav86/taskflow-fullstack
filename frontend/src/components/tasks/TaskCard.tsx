import { useState } from 'react';
import { format, isPast, isToday } from 'date-fns';
import { Calendar, Edit2, Trash2, Clock } from 'lucide-react';
import { clsx } from 'clsx';
import type { Task } from '@/types';
import { StatusBadge, PriorityBadge, ConfirmDialog } from '@/components/ui';
import { useDeleteTask } from '@/hooks';

interface TaskCardProps {
  task: Task;
  onEdit: (task: Task) => void;
}

export function TaskCard({ task, onEdit }: TaskCardProps) {
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const deleteTask = useDeleteTask();

  const isOverdue =
    task.due_date &&
    task.status !== 'done' &&
    isPast(new Date(task.due_date)) &&
    !isToday(new Date(task.due_date));

  const handleDelete = () => {
    deleteTask.mutate(task.id, {
      onSuccess: () => setShowDeleteConfirm(false),
    });
  };

  return (
    <>
      <div
        className={clsx(
          'card p-4 transition-all duration-200 hover:shadow-md',
          'animate-fade-in',
          task.status === 'done' && 'opacity-75'
        )}
      >
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1 min-w-0">
            <h3
              className={clsx(
                'font-medium text-gray-900 dark:text-gray-100 mb-1',
                task.status === 'done' && 'line-through text-gray-500'
              )}
            >
              {task.title}
            </h3>
            
            {task.description && (
              <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-2 mb-3">
                {task.description}
              </p>
            )}

            <div className="flex flex-wrap items-center gap-2">
              <StatusBadge status={task.status} />
              <PriorityBadge priority={task.priority} />
              
              {task.due_date && (
                <span
                  className={clsx(
                    'inline-flex items-center gap-1 text-xs',
                    isOverdue
                      ? 'text-red-600 dark:text-red-400'
                      : 'text-gray-500 dark:text-gray-400'
                  )}
                >
                  {isOverdue ? (
                    <Clock className="w-3 h-3" />
                  ) : (
                    <Calendar className="w-3 h-3" />
                  )}
                  {format(new Date(task.due_date), 'MMM d, yyyy')}
                </span>
              )}
            </div>
          </div>

          <div className="flex items-center gap-1">
            <button
              onClick={() => onEdit(task)}
              className="p-2 rounded-lg text-gray-400 hover:text-gray-600 hover:bg-gray-100 dark:hover:text-gray-300 dark:hover:bg-gray-800 transition-colors"
              aria-label="Edit task"
            >
              <Edit2 className="w-4 h-4" />
            </button>
            <button
              onClick={() => setShowDeleteConfirm(true)}
              className="p-2 rounded-lg text-gray-400 hover:text-red-600 hover:bg-red-50 dark:hover:text-red-400 dark:hover:bg-red-900/20 transition-colors"
              aria-label="Delete task"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      <ConfirmDialog
        isOpen={showDeleteConfirm}
        onClose={() => setShowDeleteConfirm(false)}
        onConfirm={handleDelete}
        title="Delete Task"
        message={`Are you sure you want to delete "${task.title}"? This action cannot be undone.`}
        confirmText="Delete"
        isLoading={deleteTask.isPending}
      />
    </>
  );
}

export default TaskCard;

