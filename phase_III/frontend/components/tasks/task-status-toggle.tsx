import { Button } from '../../components/ui/button';
import { Checkbox } from '../../components/ui/checkbox';
interface TaskStatusToggleProps {
  completed: boolean;
  onToggle: (completed: boolean) => void;
  disabled?: boolean;
}

export function TaskStatusToggle({ completed, onToggle, disabled }: TaskStatusToggleProps) {
  return (
    <div className="flex items-center space-x-2">
      <Checkbox
        checked={completed}
        onCheckedChange={onToggle}
        disabled={disabled}
        aria-label={completed ? 'Mark as incomplete' : 'Mark as complete'}
      />
      <span className="text-sm font-medium">
        {completed ? 'Completed' : 'Pending'}
      </span>
    </div>
  );
}