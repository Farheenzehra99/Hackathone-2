import { Button } from '../../components/ui/button';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '../../components/ui/dialog';
import { motion } from 'framer-motion';
import { useState } from 'react';

interface DeleteTaskModalProps {
  isOpen: boolean;
  onClose: () => void;
  taskTitle: string; // for display
  onConfirm: () => void | Promise<void>; // called when user confirms delete
}

export function DeleteTaskModal({ isOpen, onClose, taskTitle, onConfirm }: DeleteTaskModalProps) {
  const [loading, setLoading] = useState(false);

  const handleDelete = async () => {
    setLoading(true);
    try {
      await onConfirm(); // call parent deletion logic
      onClose();
    } catch (error) {
      console.error('Failed to delete task:', error);
      alert('Failed to delete task. Try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-md backdrop-blur-2xl bg-white/10 dark:bg-black/40 border border-white/20 dark:border-gray-700/50 shadow-2xl">
        <DialogHeader>
          <DialogTitle asChild>
            <motion.h2
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.2 }}
            >
              <span className="text-white bg-gradient-to-r from-red-400 to-orange-400 bg-clip-text text-transparent">Delete Task</span>
            </motion.h2>
          </DialogTitle>
        </DialogHeader>
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.2, delay: 0.1 }}
        >
          <DialogDescription className="mb-4 text-white">
            Are you sure you want to delete <strong className="text-red-400">{taskTitle}</strong>? This action cannot be undone.
          </DialogDescription>
          <div className="flex justify-end space-x-2 pt-4">
            <Button
              type="button"
              variant="outline"
              onClick={onClose}
              disabled={loading}
              className="bg-transparent backdrop-blur-md border border-white/30 text-white hover:bg-white/10 hover:text-white"
            >
              Cancel
            </Button>
            <Button
              type="button"
              variant="destructive"
              onClick={handleDelete}
              disabled={loading}
              className="bg-red-500/20 backdrop-blur-md border border-red-500/30 text-red-300 hover:bg-red-500/30 hover:text-red-200"
            >
              {loading ? 'Deleting...' : 'Delete'}
            </Button>
          </div>
        </motion.div>
      </DialogContent>
    </Dialog>
  );
}