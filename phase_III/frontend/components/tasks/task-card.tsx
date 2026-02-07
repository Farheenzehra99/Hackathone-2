import { Task } from '../../lib/types';
import { Button } from '../../components/ui/button';
import { Checkbox } from '../../components/ui/checkbox';
import { Badge } from '../../components/ui/badge';
import { formatDate } from '../../lib/utils';
import { motion } from 'framer-motion';

interface TaskCardProps {
  task: Task;
  onToggleComplete: (id: string, completed: boolean) => void;
  onEdit: (task: Task) => void;
  onDelete: (id: string) => void;
}

export function TaskCard({ task, onToggleComplete, onEdit, onDelete }: TaskCardProps) {
  const handleToggle = () => {
    onToggleComplete(task.id, !task.completed);
  };

  const handleEdit = () => {
    onEdit(task);
  };

  const handleDelete = () => {
    onDelete(task.id);
  };

  // Handle keyboard navigation
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleToggle();
    } else if (e.key === 'e') {
      e.preventDefault();
      handleEdit();
    } else if (e.key === 'd') {
      e.preventDefault();
      handleDelete();
    }
  };

  return (
    <motion.div
      className={`backdrop-blur-xl bg-white/10 dark:bg-black/30 border border-white/20 dark:border-gray-700/50 rounded-xl p-4 shadow-xl cursor-pointer focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all duration-300 ${
        task.completed ? 'opacity-70' : 'hover:shadow-2xl hover:-translate-y-1'
      }`}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, x: -20 }}
      transition={{
        duration: 0.3,
        ease: "easeInOut"
      }}
      whileHover={{ y: -2, boxShadow: "0 12px 48px rgba(31, 38, 135, 0.5)" }}
      whileTap={{ scale: 0.99 }}
      tabIndex={0}
      onKeyDown={handleKeyDown}
    >
      <div className="flex items-start gap-3">
        <Checkbox
          checked={task.completed}
          onCheckedChange={handleToggle}
          aria-label="Toggle task completion"
          className="mt-1"
        />
        <div className="flex-1 min-w-0">
          <h3 className={`font-bold truncate ${task.completed ? 'line-through bg-gradient-to-r from-gray-400 to-gray-500 bg-clip-text text-transparent' : 'bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent'}`}>
            {task.title}
          </h3>
          {task.description && (
            <p className={`text-sm mt-1 ${task.completed ? 'text-gray-400' : 'text-gray-300'}`}>
              {task.description}
            </p>
          )}
          <div className="flex items-center gap-2 mt-2">
            <Badge
              variant={task.priority === 'high' ? 'destructive' : task.priority === 'medium' ? 'default' : 'secondary'}
              className={`text-xs ${
                task.priority === 'high'
                  ? 'bg-red-500/20 border-red-500/30 text-red-300'
                  : task.priority === 'medium'
                    ? 'bg-yellow-500/20 border-yellow-500/30 text-yellow-300'
                    : 'bg-green-500/20 border-green-500/30 text-green-300'
              }`}
            >
              {task.priority}
            </Badge>
            <span className="text-xs text-gray-400">
              {formatDate(task.updated_at)}
            </span>
          </div>
        </div>
        <div className="flex gap-2">
          <Button
            onClick={handleEdit}
            variant="outline"
            size="sm"
            className="bg-transparent backdrop-blur-md border border-blue-500/30 text-blue-300 hover:bg-blue-500/10 hover:text-blue-200"
          >
            Edit
          </Button>
          <Button
            onClick={handleDelete}
            variant="outline"
            size="sm"
            className="bg-transparent backdrop-blur-md border border-red-500/30 text-red-400 hover:bg-red-500/10 hover:text-red-300"
          >
            Delete
          </Button>
        </div>
      </div>
    </motion.div>
  );
}