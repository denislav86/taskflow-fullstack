import { useForm } from 'react-hook-form';
import { format } from 'date-fns';
import type { Task, TaskCreate, TaskUpdate } from '@/types';
import { Button, Input, Select } from '@/components/ui';
import { useCreateTask, useUpdateTask } from '@/hooks';

interface TaskFormProps {
  task?: Task;
  onSuccess: () => void;
  onCancel: () => void;
}

interface FormData {
  title: string;
  description: string;
  status: string;
  priority: string;
  due_date: string;
}

const statusOptions = [
  { value: 'todo', label: 'To Do' },
  { value: 'in_progress', label: 'In Progress' },
  { value: 'done', label: 'Done' },
];

const priorityOptions = [
  { value: 'low', label: 'Low' },
  { value: 'medium', label: 'Medium' },
  { value: 'high', label: 'High' },
];

export function TaskForm({ task, onSuccess, onCancel }: TaskFormProps) {
  const isEditing = !!task;
  const createTask = useCreateTask();
  const updateTask = useUpdateTask();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormData>({
    defaultValues: {
      title: task?.title || '',
      description: task?.description || '',
      status: task?.status || 'todo',
      priority: task?.priority || 'medium',
      due_date: task?.due_date
        ? format(new Date(task.due_date), "yyyy-MM-dd'T'HH:mm")
        : '',
    },
  });

  const onSubmit = (data: FormData) => {
    const payload: TaskCreate | TaskUpdate = {
      title: data.title,
      description: data.description || undefined,
      status: data.status as TaskCreate['status'],
      priority: data.priority as TaskCreate['priority'],
      due_date: data.due_date ? new Date(data.due_date).toISOString() : undefined,
    };

    if (isEditing) {
      updateTask.mutate(
        { id: task.id, data: payload },
        { onSuccess }
      );
    } else {
      createTask.mutate(payload as TaskCreate, { onSuccess });
    }
  };

  const isLoading = createTask.isPending || updateTask.isPending;

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <Input
        label="Title"
        placeholder="Enter task title"
        error={errors.title?.message}
        {...register('title', { required: 'Title is required' })}
      />

      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
          Description
        </label>
        <textarea
          className="input min-h-[100px] resize-y"
          placeholder="Enter task description (optional)"
          {...register('description')}
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <Select
          label="Status"
          options={statusOptions}
          {...register('status')}
        />
        <Select
          label="Priority"
          options={priorityOptions}
          {...register('priority')}
        />
      </div>

      <Input
        type="datetime-local"
        label="Due Date"
        {...register('due_date')}
      />

      <div className="flex gap-3 pt-4">
        <Button
          type="button"
          variant="secondary"
          onClick={onCancel}
          disabled={isLoading}
          className="flex-1"
        >
          Cancel
        </Button>
        <Button
          type="submit"
          variant="primary"
          isLoading={isLoading}
          className="flex-1"
        >
          {isEditing ? 'Update Task' : 'Create Task'}
        </Button>
      </div>
    </form>
  );
}

export default TaskForm;

