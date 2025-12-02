import { ClipboardList } from 'lucide-react';
import type { Task } from '@/types';
import { EmptyState, LoadingScreen } from '@/components/ui';
import TaskCard from './TaskCard';

interface TaskListProps {
  tasks: Task[];
  isLoading: boolean;
  onEdit: (task: Task) => void;
  onCreateNew: () => void;
}

export function TaskList({ tasks, isLoading, onEdit, onCreateNew }: TaskListProps) {
  if (isLoading) {
    return <LoadingScreen />;
  }

  if (tasks.length === 0) {
    return (
      <EmptyState
        icon={ClipboardList}
        title="No tasks found"
        description="Get started by creating your first task or adjust your filters."
        action={
          <button
            onClick={onCreateNew}
            className="btn btn-primary"
          >
            Create Task
          </button>
        }
      />
    );
  }

  return (
    <div className="grid gap-4">
      {tasks.map((task) => (
        <TaskCard key={task.id} task={task} onEdit={onEdit} />
      ))}
    </div>
  );
}

export default TaskList;

