import axios from 'axios';
import { Task, TaskFormData, TaskExecution } from '../types/Task';

const API_BASE_URL = '/api/tasks';

export const taskService = {
  // Get all tasks
  getAllTasks: async (): Promise<Task[]> => {
    const response = await axios.get(API_BASE_URL);
    return response.data;
  },

  // Get task by ID
  getTaskById: async (id: string): Promise<Task> => {
    const response = await axios.get(`${API_BASE_URL}?id=${id}`);
    return response.data;
  },

  // Search tasks by name
  searchTasks: async (name: string): Promise<Task[]> => {
    const response = await axios.get(`${API_BASE_URL}/search?name=${name}`);
    return response.data;
  },

  // Search tasks by name or owner
  searchTasksBy: async (params: { name?: string; owner?: string }): Promise<Task[]> => {
    const queryParams = new URLSearchParams();
    if (params.name) queryParams.append('name', params.name);
    if (params.owner) queryParams.append('owner', params.owner);
    const response = await axios.get(`${API_BASE_URL}/search?${queryParams.toString()}`);
    return response.data;
  },

  // Create or update task
  saveTask: async (task: TaskFormData): Promise<Task> => {
    const response = await axios.put(API_BASE_URL, task);
    return response.data;
  },

  // Delete task
  deleteTask: async (id: string): Promise<void> => {
    await axios.delete(`${API_BASE_URL}/${id}`);
  },

  // Execute task
  executeTask: async (id: string): Promise<TaskExecution> => {
    const response = await axios.put(`${API_BASE_URL}/${id}/execute`);
    return response.data;
  },
};
