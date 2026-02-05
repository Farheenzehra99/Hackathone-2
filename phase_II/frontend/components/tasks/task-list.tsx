'use client';

import { useState, useEffect, useMemo } from 'react';
import { Task } from '../../lib/types';
import { TaskCard } from '../../components/tasks/task-card';
import { AddTaskModal } from '../../components/tasks/add-task-modal';
import { EditTaskModal } from '../../components/tasks/edit-task-modal';
import { DeleteTaskModal } from '../../components/tasks/delete-task-modal';
import { useToast } from '../../hooks/use-toast';
import { Input } from '../../components/ui/input';
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from '../../components/ui/select';

// ---------------- JWT + Neon DB Helper ----------------
const API_BASE = '/api';


const getAuthHeaders = (json: boolean = true): Record<string, string> => {
  if (typeof window === 'undefined') return {}; // safe for server
  const token = localStorage.getItem('accessToken');
  return {
    ...(json ? { 'Content-Type': 'application/json' } : {}),
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
};

const taskApi = {
  getAllTasks: async (): Promise<{ success: boolean; data?: Task[]; message?: string }> => {
    // const token = localStorage.getItem('accessToken');
    // if (!token) {
    //   return { success: false, message: 'User not authenticated' }; // prevent 403
    // }
    const res = await fetch(`${API_BASE}/tasks`, {
      headers: getAuthHeaders(),
    });
    return res.json();
  },

  createTask: async (taskData: Omit<Task, 'id' | 'userId' | 'created_at' | 'updated_at'>) => {
    // const token = localStorage.getItem('accessToken');
    // if (!token) return { success: false, message: 'User not authenticated' };
    const res = await fetch(`${API_BASE}/tasks`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(taskData),
    });
    return res.json();
  },

  updateTask: async (id: string, updatedTask: Partial<Task>) => {
    // const token = localStorage.getItem('accessToken');
    // if (!token) return { success: false, message: 'User not authenticated' };
    const res = await fetch(`${API_BASE}/tasks/${id}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(updatedTask),
    });
    return res.json();
  },

  deleteTask: async (id: string) => {
    // const token = localStorage.getItem('accessToken');
    // if (!token) return { success: false, message: 'User not authenticated' };
    const res = await fetch(`${API_BASE}/tasks/${id}`, {
      method: 'DELETE',
      headers: getAuthHeaders(false),
    });
    return res.json();
  },

  toggleTaskCompletion: async (id: string, completed: boolean) => {
    // const token = localStorage.getItem('accessToken');
    // if (!token) return { success: false, message: 'User not authenticated' };
    const res = await fetch(`${API_BASE}/tasks/${id}/complete`, {
      method: 'PATCH',
      headers: getAuthHeaders(),
      body: JSON.stringify({ completed }),
    });
    return res.json();
  },
};

// ------------------------------------------------------

export function TaskList() {
  const [tasks, setTasks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);
  const [deleteTaskId, setDeleteTaskId] = useState<string | null>(null);
  const [showAddModal, setShowAddModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState<'all' | 'completed' | 'pending'>('all');
  const [filterPriority, setFilterPriority] = useState<'all' | 'low' | 'medium' | 'high'>('all');
  const { toast } = useToast();

  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    setLoading(true);
    try {
      const response = await taskApi.getAllTasks();
      setTasks(Array.isArray(response.data) ? response.data : []);
      // else
      //   toast({
      //     title: 'Error',
      //     description: response.message || 'Failed to load tasks',
      //     variant: 'destructive',
      //   });
    } catch {
      toast({ title: 'Error', description: 'Failed to load tasks', variant: 'destructive' });
    } finally {
      setLoading(false);
    }
  };

  const filteredTasks = useMemo(() => {
    if (!Array.isArray(tasks)) return []; // <<< safe check
    return tasks.filter(task => {
      const matchesSearch =
        task.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (task.description && task.description.toLowerCase().includes(searchTerm.toLowerCase()));

      let matchesStatus = true;
      if (filterStatus === 'completed') matchesStatus = task.completed;
      else if (filterStatus === 'pending') matchesStatus = !task.completed;

      let matchesPriority = true;
      if (filterPriority !== 'all') matchesPriority = task.priority === filterPriority;

      return matchesSearch && matchesStatus && matchesPriority;
    });
  }, [tasks, searchTerm, filterStatus, filterPriority]);

  const handleToggleComplete = async (id: string, completed: boolean) => {
    try {
      const response = await taskApi.toggleTaskCompletion(id, completed);
      if (response.success) {
        setTasks(prev => prev.map(task => (task.id === id ? { ...task, completed, updatedAt: response.data?.updatedAt ? new Date(response.data.updatedAt) : task.updatedAt } : task)));
        toast({
          title: completed ? 'Task completed!' : 'Task marked as incomplete',
          description: completed ? 'Task has been marked as complete' : 'Task has been marked as incomplete',
        });
      } else throw new Error(response.message);
    } catch {
      toast({ title: 'Error', description: 'Failed to update task status', variant: 'destructive' });
    }
  };

  const handleEditTask = (task: Task) => {
    setSelectedTask(task);
    setShowEditModal(true);
  };

  const handleUpdateTask = async (updatedTask: Partial<Task>) => {
    if (!selectedTask) return;
    try {
      const response = await taskApi.updateTask(selectedTask.id, updatedTask);
      if (response.success) {
        setTasks(prev => prev.map(task => (task.id === selectedTask.id ? { ...task, ...response.data } : task)));
        toast({ title: 'Task updated!', description: 'Task has been updated successfully' });
        setShowEditModal(false);
        setSelectedTask(null);
      } else throw new Error(response.message);
    } catch {
      toast({ title: 'Error', description: 'Failed to update task', variant: 'destructive' });
    }
  };

  const handleDeleteTask = (id: string) => {
    setDeleteTaskId(id);
    setShowDeleteModal(true);
  };

  const confirmDeleteTask = async () => {
    if (!deleteTaskId) return;
    const deletedTask = tasks.find(task => task.id === deleteTaskId);
    try {
      const response = await taskApi.deleteTask(deleteTaskId);
      if (response.success) {
        setTasks(prev => prev.filter(task => task.id !== deleteTaskId));
        toast({
          title: 'Task deleted!',
          description: 'Task has been deleted successfully',
          action: deletedTask ? (
        <button
          onClick={() => handleUndoDelete(deletedTask)}
          className="text-blue-500 hover:text-blue-700 font-medium"
        >
          Undo
        </button>
      ) : undefined,

        });
      } else throw new Error(response.message);
    } catch {
      toast({ title: 'Error', description: 'Failed to delete task', variant: 'destructive' });
    } finally {
      setShowDeleteModal(false);
      setDeleteTaskId(null);
    }
  };

  const handleUndoDelete = (task: Task) => {
    setTasks(prev => [...prev, task]);
    toast({ title: 'Task restored!', description: 'Task has been restored' });
  };

  const handleAddTask = async (taskData: Omit<Task, 'id' | 'userId' | 'created_at' | 'updated_at'>) => {
    try {
      const response = await taskApi.createTask(taskData);
      if (response.success) {
        setTasks(prev => [...prev, response.data!]);
        toast({ title: 'Task created!', description: 'Task has been created successfully' });
        setShowAddModal(false);
      } else throw new Error(response.message);
    } catch {
      toast({ title: 'Error', description: 'Failed to create task', variant: 'destructive' });
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <h2 className="text-xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">Your Tasks</h2>
        <div className="flex gap-2">
          <button
            onClick={() => setShowAddModal(true)}
            className="backdrop-blur-md bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 shadow-lg hover:shadow-xl"
          >
            Add Task
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Input
          placeholder="Search tasks..."
          value={searchTerm}
          onChange={e => setSearchTerm(e.target.value)}
          className="backdrop-blur-md bg-white/10 border border-white/20 text-white placeholder:text-gray-400 rounded-lg"
        />
        <Select value={filterStatus} onValueChange={value => setFilterStatus(value as 'all' | 'completed' | 'pending')}>
          <SelectTrigger className="backdrop-blur-md bg-white/10 border border-white/20 text-white rounded-lg">
            <SelectValue placeholder="Filter by status" className="text-white" />
          </SelectTrigger>
          <SelectContent className="bg-gray-800/80 backdrop-blur-md border border-white/20 rounded-lg">
            <SelectItem value="all" className="text-white">All Statuses</SelectItem>
            <SelectItem value="pending" className="text-white">Pending</SelectItem>
            <SelectItem value="completed" className="text-white">Completed</SelectItem>
          </SelectContent>
        </Select>
        <Select value={filterPriority} onValueChange={value => setFilterPriority(value as 'all' | 'low' | 'medium' | 'high')}>
          <SelectTrigger className="backdrop-blur-md bg-white/10 border border-white/20 text-white rounded-lg">
            <SelectValue placeholder="Filter by priority" className="text-white" />
          </SelectTrigger>
          <SelectContent className="bg-gray-800/80 backdrop-blur-md border border-white/20 rounded-lg">
            <SelectItem value="all" className="text-white">All Priorities</SelectItem>
            <SelectItem value="low" className="text-white">Low</SelectItem>
            <SelectItem value="medium" className="text-white">Medium</SelectItem>
            <SelectItem value="high" className="text-white">High</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {filteredTasks.length === 0 ? (
        <div className="text-center py-12 backdrop-blur-xl bg-white/5 rounded-xl border border-white/10 shadow-lg">
          <p className="text-gray-400">{tasks.length === 0 ? 'No tasks yet. Add your first task!' : 'No tasks match your filters.'}</p>
        </div>
      ) : (
        <div className="space-y-3">
          {filteredTasks.map(task => (
            <TaskCard key={task.id} task={task} onToggleComplete={handleToggleComplete} onEdit={handleEditTask} onDelete={handleDeleteTask} />
          ))}
        </div>
      )}

      <AddTaskModal isOpen={showAddModal} onClose={() => setShowAddModal(false)} onAdd={handleAddTask} />
      {showEditModal && selectedTask && (
        <EditTaskModal
          isOpen={showEditModal}
          onClose={() => { setShowEditModal(false); setSelectedTask(null); }}
          task={selectedTask}
          onUpdate={handleUpdateTask}
        />
      )}      
      <DeleteTaskModal isOpen={showDeleteModal} onClose={() => setShowDeleteModal(false)} onConfirm={confirmDeleteTask} taskTitle={tasks.find(t => t.id === deleteTaskId)?.title || ''} />
    </div>
  );
}
