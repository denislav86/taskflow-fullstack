import {
  CheckCircle,
  Clock,
  AlertTriangle,
  TrendingUp,
  ListTodo,
  Loader2,
  Target,
  Zap,
} from 'lucide-react';
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
} from 'recharts';
import { clsx } from 'clsx';
import { useAnalytics } from '@/hooks';
import { LoadingScreen } from '@/components/ui';

interface StatCardProps {
  title: string;
  value: number | string;
  icon: React.ElementType;
  color: 'green' | 'blue' | 'yellow' | 'red' | 'purple';
  subtitle?: string;
}

function StatCard({ title, value, icon: Icon, color, subtitle }: StatCardProps) {
  const colorClasses = {
    green: 'bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400',
    blue: 'bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400',
    yellow: 'bg-yellow-100 text-yellow-600 dark:bg-yellow-900/30 dark:text-yellow-400',
    red: 'bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400',
    purple: 'bg-purple-100 text-purple-600 dark:bg-purple-900/30 dark:text-purple-400',
  };

  return (
    <div className="card p-6 animate-fade-in">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
            {title}
          </p>
          <p className="text-3xl font-bold text-gray-900 dark:text-white mt-1">
            {value}
          </p>
          {subtitle && (
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
              {subtitle}
            </p>
          )}
        </div>
        <div className={clsx('p-3 rounded-xl', colorClasses[color])}>
          <Icon className="w-6 h-6" />
        </div>
      </div>
    </div>
  );
}

export function AnalyticsPage() {
  const { data, isLoading } = useAnalytics();

  if (isLoading) {
    return <LoadingScreen />;
  }

  if (!data) {
    return null;
  }

  const statusData = [
    { name: 'To Do', value: data.pending_tasks, color: '#9ca3af' },
    { name: 'In Progress', value: data.in_progress_tasks, color: '#3b82f6' },
    { name: 'Done', value: data.completed_tasks, color: '#22c55e' },
  ];

  const barData = [
    { name: 'Completed', value: data.completed_tasks },
    { name: 'In Progress', value: data.in_progress_tasks },
    { name: 'Pending', value: data.pending_tasks },
    { name: 'Overdue', value: data.overdue_tasks },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          Analytics
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">
          Overview of your task performance
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="Total Tasks"
          value={data.total_tasks}
          icon={ListTodo}
          color="blue"
        />
        <StatCard
          title="Completed"
          value={data.completed_tasks}
          icon={CheckCircle}
          color="green"
          subtitle={`${data.completion_rate}% completion rate`}
        />
        <StatCard
          title="Completed This Week"
          value={data.completed_this_week}
          icon={TrendingUp}
          color="purple"
        />
        <StatCard
          title="Overdue"
          value={data.overdue_tasks}
          icon={AlertTriangle}
          color="red"
        />
      </div>

      {/* Additional Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="In Progress"
          value={data.in_progress_tasks}
          icon={Loader2}
          color="blue"
        />
        <StatCard
          title="Pending"
          value={data.pending_tasks}
          icon={Clock}
          color="yellow"
        />
        <StatCard
          title="High Priority Pending"
          value={data.high_priority_pending}
          icon={Zap}
          color="red"
        />
        <StatCard
          title="Completion Rate"
          value={`${data.completion_rate}%`}
          icon={Target}
          color="green"
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Status Distribution */}
        <div className="card p-6">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">
            Task Status Distribution
          </h2>
          {data.total_tasks > 0 ? (
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={statusData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={2}
                    dataKey="value"
                  >
                    {statusData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      backgroundColor: 'var(--toast-bg)',
                      borderColor: 'transparent',
                      borderRadius: '12px',
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
              <div className="flex justify-center gap-6 mt-4">
                {statusData.map((item) => (
                  <div key={item.name} className="flex items-center gap-2">
                    <div
                      className="w-3 h-3 rounded-full"
                      style={{ backgroundColor: item.color }}
                    />
                    <span className="text-sm text-gray-600 dark:text-gray-400">
                      {item.name} ({item.value})
                    </span>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="h-64 flex items-center justify-center text-gray-500">
              No tasks to display
            </div>
          )}
        </div>

        {/* Task Overview Bar Chart */}
        <div className="card p-6">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">
            Task Overview
          </h2>
          {data.total_tasks > 0 ? (
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={barData}>
                  <XAxis
                    dataKey="name"
                    tick={{ fill: '#9ca3af', fontSize: 12 }}
                    axisLine={false}
                    tickLine={false}
                  />
                  <YAxis
                    tick={{ fill: '#9ca3af', fontSize: 12 }}
                    axisLine={false}
                    tickLine={false}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: 'var(--toast-bg)',
                      borderColor: 'transparent',
                      borderRadius: '12px',
                    }}
                  />
                  <Bar
                    dataKey="value"
                    fill="#22c55e"
                    radius={[6, 6, 0, 0]}
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <div className="h-64 flex items-center justify-center text-gray-500">
              No tasks to display
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default AnalyticsPage;

