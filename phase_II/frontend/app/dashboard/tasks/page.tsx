import { TaskList } from '@/components/tasks/task-list';

export default function TasksPage() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">All Tasks</h1>
      </div>
      <TaskList />
    </div>
  );
}