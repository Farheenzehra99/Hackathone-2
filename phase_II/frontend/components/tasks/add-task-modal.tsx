// import { useState } from 'react';
// import { Button } from '../../components/ui/button';
// import { Input } from '../../components/ui/input';
// import { Label } from '../../components/ui/label';
// import { Textarea } from '../../components/ui/textarea';
// import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from '../../components/ui/select';
// import { Dialog, DialogContent, DialogHeader, DialogTitle } from '../../components/ui/dialog';
// import { Task } from '../../lib/types';

// interface AddTaskModalProps {
//   isOpen: boolean;
//   onClose: () => void;
//   onAdd?: (taskData: Omit<Task, 'id' | 'userId' | 'createdAt' | 'updatedAt'>) => void | Promise<void>;
// }

// export function AddTaskModal({ isOpen, onClose, onAdd }: AddTaskModalProps) {
//   const [title, setTitle] = useState('');
//   const [description, setDescription] = useState('');
//   const [priority, setPriority] = useState<'low' | 'medium' | 'high'>('medium');
//   const [loading, setLoading] = useState(false);

//   const apiUrl = process.env.NEXT_PUBLIC_API_URL;
//   const token = process.env.NEXT_PUBLIC_API_TOKEN;

//   const handleSubmit = async (e: React.FormEvent) => {
//     e.preventDefault();

//     if (!title) return; // required

//     const taskData: Omit<Task, 'id' | 'userId' | 'createdAt' | 'updatedAt'> = {
//       title,
//       description: description || undefined,
//       priority,
//       completed: false,
//     };

//     setLoading(true);

//     try {
//       const response = await fetch(`${apiUrl}/api/v1/tasks/`, {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//           Authorization: `Bearer ${token}`,
//         },
//         body: JSON.stringify(taskData),
//       });

//       if (!response.ok) {
//         const err = await response.json();
//         console.error('Error adding task:', err);
//         alert('Failed to add task. Check console.');
//       } else {
//         console.log('Task added successfully!');
//         // Pass the task data to the parent callback
//         onAdd?.(taskData);
//         onClose();
//         setTitle('');
//         setDescription('');
//         setPriority('medium');
//       }
//     } catch (error) {
//       console.error('Network error:', error);
//       alert('Network error. Try again.');
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <Dialog open={isOpen} onOpenChange={onClose}>
//       <DialogContent className="sm:max-w-md backdrop-blur-2xl bg-white/10 dark:bg-black/40 border border-white/20 dark:border-gray-700/50 shadow-2xl">
//         <DialogHeader>
//           <DialogTitle className="text-white bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">Add New Task</DialogTitle>
//         </DialogHeader>
//         <form onSubmit={handleSubmit} className="space-y-4">
//           <div className="space-y-2">
//             <Label htmlFor="title" className="text-white">Title *</Label>
//             <Input
//               id="title"
//               value={title}
//               onChange={(e) => setTitle(e.target.value)}
//               required
//               placeholder="Task title"
//               className="bg-white/10 border border-white/20 text-white placeholder:text-gray-400 backdrop-blur-md"
//             />
//           </div>

//           <div className="space-y-2">
//             <Label htmlFor="description" className="text-white">Description</Label>
//             <Textarea
//               id="description"
//               value={description}
//               onChange={(e) => setDescription(e.target.value)}
//               placeholder="Task description (optional)"
//               className="bg-white/10 border border-white/20 text-white placeholder:text-gray-400 backdrop-blur-md"
//             />
//           </div>

//           <div className="space-y-2">
//             <Label htmlFor="priority" className="text-white">Priority</Label>
//             <Select value={priority} onValueChange={(value: 'low' | 'medium' | 'high') => setPriority(value)}>
//               <SelectTrigger className="bg-white/10 border border-white/20 text-white backdrop-blur-md">
//                 <SelectValue placeholder="Select priority" className="text-white" />
//               </SelectTrigger>
//               <SelectContent className="bg-gray-800/80 backdrop-blur-md border border-white/20">
//                 <SelectItem value="low" className="text-white">Low</SelectItem>
//                 <SelectItem value="medium" className="text-white">Medium</SelectItem>
//                 <SelectItem value="high" className="text-white">High</SelectItem>
//               </SelectContent>
//             </Select>
//           </div>

//           <div className="flex justify-end space-x-2 pt-4">
//             <Button
//               type="button"
//               variant="outline"
//               onClick={onClose}
//               disabled={loading}
//               className="bg-transparent backdrop-blur-md border border-white/30 text-white hover:bg-white/10 hover:text-white"
//             >
//               Cancel
//             </Button>
//             <Button
//               type="submit"
//               disabled={loading}
//               className="bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 text-white px-4 py-2 rounded-lg transition-all duration-300 shadow-lg hover:shadow-xl"
//             >
//               {loading ? 'Adding...' : 'Add Task'}
//             </Button>
//           </div>
//         </form>
//       </DialogContent>
//     </Dialog>
//   );
// }



import { useState } from 'react';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Label } from '../../components/ui/label';
import { Textarea } from '../../components/ui/textarea';
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from '../../components/ui/select';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '../../components/ui/dialog';
import { Task } from '../../lib/types'; 

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

interface AddTaskModalProps {
  isOpen: boolean;
  onClose: () => void;
  onAdd?: (taskData: Omit<Task, 'id' | 'userId' | 'createdAt' | 'updatedAt'>) => void | Promise<void>;
}

export function AddTaskModal({ isOpen, onClose, onAdd }: AddTaskModalProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState<'low' | 'medium' | 'high'>('medium');
  const [loading, setLoading] = useState(false);


  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    // ✅ Get token from localStorage (refreshToken)
    const token = localStorage.getItem('accessToken');
    if (!token) {
      alert('No token found! Please login first.');
      setLoading(false);
      return;
    }

    // ✅ Prepare task data correctly
    const taskData: Omit<Task, 'id' | 'userId' | 'createdAt' | 'updatedAt'> = {
      title: title.trim(),
      description: description?.trim() || '',
      priority: priority || 'medium',
      completed: false,
    };

    if (!taskData.title) {
      alert('Title is required.');
      setLoading(false);
      return;
    }

    try {
      const response = await fetch(`${API_BASE}/tasks/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(taskData),
      });

      const data = await response.json();

      if (!response.ok) {
        console.error('Error adding task:', data);
        alert('Failed to add task. Check console.');
      } else {
        console.log('Task added successfully!', data);
        onAdd?.(taskData); // pass data to parent if callback exists
        onClose();
        setTitle('');
        setDescription('');
        setPriority('medium');
      }
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
          <DialogTitle className="text-white bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">Add New Task</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="title" className="text-white">Title *</Label>
            <Input
              id="title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
              placeholder="Task title"
              className="bg-white/10 border border-white/20 text-white placeholder:text-gray-400 backdrop-blur-md"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="description" className="text-white">Description</Label>
            <Textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Task description (optional)"
              className="bg-white/10 border border-white/20 text-white placeholder:text-gray-400 backdrop-blur-md"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="priority" className="text-white">Priority</Label>
            <Select value={priority} onValueChange={(value: 'low' | 'medium' | 'high') => setPriority(value)}>
              <SelectTrigger className="bg-white/10 border border-white/20 text-white backdrop-blur-md">
                <SelectValue placeholder="Select priority" className="text-white" />
              </SelectTrigger>
              <SelectContent className="bg-gray-800/80 backdrop-blur-md border border-white/20">
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
              {loading ? 'Adding...' : 'Add Task'}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}
