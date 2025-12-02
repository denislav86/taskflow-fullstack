import { useState } from 'react';
import { Plus } from 'lucide-react';
import { Button, Modal } from '@/components/ui';
import { TaskFilters, TaskList, TaskForm, Pagination } from '@/components/tasks';
import { useTasks } from '@/hooks';
import type { Task, TaskFilters as TaskFiltersType } from '@/types';

export function DashboardPage() {
  const [filters, setFilters] = useState<TaskFiltersType>({ page: 1, page_size: 10 });
  const [showModal, setShowModal] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | undefined>();

  const { data, isLoading } = useTasks(filters);

  const handleEdit = (task: Task) => {
    setEditingTask(task);
    setShowModal(true);
  };

  const handleCreate = () => {
    setEditingTask(undefined);
    setShowModal(true);
  };

  const handleModalClose = () => {
    setShowModal(false);
    setEditingTask(undefined);
  };

  const handlePageChange = (page: number) => {
    setFilters((prev) => ({ ...prev, page }));
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            My Tasks
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            {data?.total || 0} total tasks
          </p>
        </div>
        <Button onClick={handleCreate}>
          <Plus className="w-5 h-5" />
          New Task
        </Button>
      </div>

      {/* Filters */}
      <div className="mb-6">
        <TaskFilters
          filters={filters}
          onChange={(newFilters) => setFilters({ ...newFilters, page: 1 })}
        />
      </div>

      {/* Task List */}
      <TaskList
        tasks={data?.items || []}
        isLoading={isLoading}
        onEdit={handleEdit}
        onCreateNew={handleCreate}
      />

      {/* Pagination */}
      {data && data.total_pages > 1 && (
        <div className="mt-8">
          <Pagination
            currentPage={data.page}
            totalPages={data.total_pages}
            onPageChange={handlePageChange}
          />
        </div>
      )}

      {/* Create/Edit Modal */}
      <Modal
        isOpen={showModal}
        onClose={handleModalClose}
        title={editingTask ? 'Edit Task' : 'Create New Task'}
      >
        <TaskForm
          task={editingTask}
          onSuccess={handleModalClose}
          onCancel={handleModalClose}
        />
      </Modal>
    </div>
  );
}

export default DashboardPage;

