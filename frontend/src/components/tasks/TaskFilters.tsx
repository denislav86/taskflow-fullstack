import { Search, Filter, X } from 'lucide-react';
import { Input, Select, Button } from '@/components/ui';
import type { TaskFilters as TaskFiltersType } from '@/types';

interface TaskFiltersProps {
  filters: TaskFiltersType;
  onChange: (filters: TaskFiltersType) => void;
}

const statusOptions = [
  { value: '', label: 'All Statuses' },
  { value: 'todo', label: 'To Do' },
  { value: 'in_progress', label: 'In Progress' },
  { value: 'done', label: 'Done' },
];

const priorityOptions = [
  { value: '', label: 'All Priorities' },
  { value: 'low', label: 'Low' },
  { value: 'medium', label: 'Medium' },
  { value: 'high', label: 'High' },
];

export function TaskFilters({ filters, onChange }: TaskFiltersProps) {
  const hasActiveFilters = filters.status || filters.priority || filters.search;

  const clearFilters = () => {
    onChange({});
  };

  return (
    <div className="card p-4">
      <div className="flex flex-col sm:flex-row gap-4">
        {/* Search */}
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            type="text"
            placeholder="Search tasks..."
            value={filters.search || ''}
            onChange={(e) => onChange({ ...filters, search: e.target.value || undefined })}
            className="input pl-10"
          />
        </div>

        {/* Status Filter */}
        <Select
          options={statusOptions}
          value={filters.status || ''}
          onChange={(e) =>
            onChange({
              ...filters,
              status: e.target.value as TaskFiltersType['status'] || undefined,
            })
          }
          className="sm:w-40"
        />

        {/* Priority Filter */}
        <Select
          options={priorityOptions}
          value={filters.priority || ''}
          onChange={(e) =>
            onChange({
              ...filters,
              priority: e.target.value as TaskFiltersType['priority'] || undefined,
            })
          }
          className="sm:w-40"
        />

        {/* Clear Filters */}
        {hasActiveFilters && (
          <Button variant="ghost" onClick={clearFilters} size="sm">
            <X className="w-4 h-4" />
            Clear
          </Button>
        )}
      </div>
    </div>
  );
}

export default TaskFilters;

