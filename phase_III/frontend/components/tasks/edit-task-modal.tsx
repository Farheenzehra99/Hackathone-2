// import { useState, useEffect } from 'react';
// import { Task } from '@/lib/types';
// import { Button } from '@/components/ui/button';
// import { Input } from '@/components/ui/input';
// import { Label } from '@/components/ui/label';
// import { Textarea } from '@/components/ui/textarea';
// import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from '@/components/ui/select';
// import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
// import { motion } from 'framer-motion';

// interface EditTaskModalProps {
//   isOpen: boolean;
//   onClose: () => void;
//   task: Task;
//   onUpdate: (taskData: Partial<Task>) => void;
// }

// export function EditTaskModal({ isOpen, onClose, task, onUpdate }: EditTaskModalProps) {
//   const [title, setTitle] = useState('');
//   const [description, setDescription] = useState('');
//   const [priority, setPriority] = useState<'low' | 'medium' | 'high'>('medium');

//   useEffect(() => {
//     if (task) {
//       setTitle(task.title);
//       setDescription(task.description || '');
//       setPriority(task.priority);
//     }
//   }, [task]);

//   const handleSubmit = (e: React.FormEvent) => {
//     e.preventDefault();

//     onUpdate({
//       title,
//       description: description || undefined,
//       priority,
//     });

//     // Reset form
//     setTitle('');
//     setDescription('');
//     setPriority('medium');
//   };

//   return (
//     <Dialog open={isOpen} onOpenChange={onClose}>
//       <DialogContent className="sm:max-w-md">
//         <DialogHeader>
//           <DialogTitle asChild>
//             <motion.h2
//               initial={{ opacity: 0, y: -10 }}
//               animate={{ opacity: 1, y: 0 }}
//               transition={{ duration: 0.2 }}
//             >
//               Edit Task
//             </motion.h2>
//           </DialogTitle>
//         </DialogHeader>
//         <motion.form
//           initial={{ opacity: 0 }}
//           animate={{ opacity: 1 }}
//           transition={{ duration: 0.2, delay: 0.1 }}
//           onSubmit={handleSubmit}
//           className="space-y-4"
//         >
//           <div className="space-y-2">
//             <Label htmlFor="title">Title *</Label>
//             <Input
//               id="title"
//               value={title}
//               onChange={(e) => setTitle(e.target.value)}
//               required
//               placeholder="Task title"
//             />
//           </div>

//           <div className="space-y-2">
//             <Label htmlFor="description">Description</Label>
//             <Textarea
//               id="description"
//               value={description}
//               onChange={(e) => setDescription(e.target.value)}
//               placeholder="Task description (optional)"
//             />
//           </div>

//           <div className="space-y-2">
//             <Label htmlFor="priority">Priority</Label>
//             <Select value={priority} onValueChange={(value: 'low' | 'medium' | 'high') => setPriority(value)}>
//               <SelectTrigger>
//                 <SelectValue placeholder="Select priority" />
//               </SelectTrigger>
//               <SelectContent>
//                 <SelectItem value="low">Low</SelectItem>
//                 <SelectItem value="medium">Medium</SelectItem>
//                 <SelectItem value="high">High</SelectItem>
//               </SelectContent>
//             </Select>
//           </div>

//           <div className="flex justify-end space-x-2 pt-4">
//             <Button type="button" variant="outline" onClick={onClose}>
//               Cancel
//             </Button>
//             <Button type="submit">Update Task</Button>
//           </div>
//         </motion.form>
//       </DialogContent>
//     </Dialog>
//   );
// }


import { useState, useEffect } from 'react';
import { Task } from '../../lib/types';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Label } from '../../components/ui/label';
import { Textarea } from '../../components/ui/textarea';
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from '../../components/ui/select';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '../../components/ui/dialog';
import { motion } from 'framer-motion'
interface EditTaskModalProps {
  isOpen: boolean;
  onClose: () => void;
  task: Task;
  onUpdate: (updatedTask: Partial<Task>) => void | Promise<void>;
}

export function EditTaskModal({
  isOpen,
  onClose,
  task,
  onUpdate,
}: EditTaskModalProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState<'low' | 'medium' | 'high'>('medium');
  const [loading, setLoading] = useState(false);

  const API_BASE = '/api';
  const token = localStorage.getItem("accessToken");

  useEffect(() => {
    if (task) {
      setTitle(task.title);
      setDescription(task.description || '');
      setPriority(task.priority);
    }
  }, [task]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    console.log("TASK ID:", task.id);

    try { 
      console.log("UPDATE URL:", `${API_BASE}/tasks/${task.id}`);

      const response = await fetch(`${API_BASE}/tasks/${task.id}`, {

        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          title,
          description: description || undefined,
          priority,
        }),
      });

      if (!response.ok) {
        const err = await response.json();
        console.error('Error updating task:', err);
        alert('Failed to update task. Check console.');
        return;
      }

      // ✅ parent ko updated data bhejna
      await onUpdate({
        title,
        description: description || undefined,
        priority,
      });

      onClose();
    } catch (error) {
      console.error('Network error:', error);
      alert('Network error. Try again.');
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
              <span className="text-white bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">Edit Task</span>
            </motion.h2>
          </DialogTitle>
        </DialogHeader>

        <motion.form
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.2, delay: 0.1 }}
          onSubmit={handleSubmit}
          className="space-y-4"
        >
          <div className="space-y-2">
            <Label htmlFor="title" className="text-white">Title *</Label>
            <Input
              id="title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
              placeholder="Task title"
              className="bg-white/10 border border-white/20 text-white placeholder:text-gray-400 backdrop-blur-md rounded-lg"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="description" className="text-white">Description</Label>
            <Textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Task description (optional)"
              className="bg-white/10 border border-white/20 text-white placeholder:text-gray-400 backdrop-blur-md rounded-lg"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="priority" className="text-white">Priority</Label>
            <Select
              value={priority}
              onValueChange={(value: 'low' | 'medium' | 'high') =>
                setPriority(value)
              }
            >
              <SelectTrigger className="bg-white/10 border border-white/20 text-white backdrop-blur-md rounded-lg">
                <SelectValue placeholder="Select priority" className="text-white" />
              </SelectTrigger>
              <SelectContent className="bg-gray-800/80 backdrop-blur-md border border-white/20 rounded-lg">
                <SelectItem value="low" className="text-white">Low</SelectItem>
                <SelectItem value="medium" className="text-white">Medium</SelectItem>
                <SelectItem value="high" className="text-white">High</SelectItem>
              </SelectContent>
            </Select>
          </div>

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
              type="submit"
              disabled={loading}
              className="bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 text-white px-4 py-2 rounded-lg transition-all duration-300 shadow-lg hover:shadow-xl"
            >
              {loading ? 'Updating...' : 'Update Task'}
            </Button>
          </div>
        </motion.form>
      </DialogContent>
    </Dialog>
  );
}
