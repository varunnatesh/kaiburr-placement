package com.kaiburr.taskmanager.service;

import com.kaiburr.taskmanager.exception.TaskNotFoundException;
import com.kaiburr.taskmanager.model.Task;
import com.kaiburr.taskmanager.model.TaskExecution;
import com.kaiburr.taskmanager.repository.TaskRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Date;
import java.util.List;
import java.util.Optional;

@Service
public class TaskService {
    
    @Autowired
    private TaskRepository taskRepository;
    
    @Autowired
    private CommandValidationService commandValidationService;
    
    @Autowired(required = false)
    private KubernetesExecutionService kubernetesExecutionService;
    
    /**
     * Get all tasks
     */
    public List<Task> getAllTasks() {
        return taskRepository.findAll();
    }
    
    /**
     * Get task by ID
     */
    public Optional<Task> getTaskById(String id) {
        return taskRepository.findById(id);
    }
    
    /**
     * Find tasks by name
     */
    public List<Task> findTasksByName(String name) {
        return taskRepository.findByNameContainingIgnoreCase(name);
    }
    
    /**
     * Find tasks by owner (assignedTo)
     */
    public List<Task> findTasksByOwner(String owner) {
        return taskRepository.findByOwnerContainingIgnoreCase(owner);
    }
    
    /**
     * Create or update a task
     */
    public Task saveTask(Task task) {
        // Validate command
        commandValidationService.validateCommand(task.getCommand());
        return taskRepository.save(task);
    }
    
    /**
     * Delete task by ID
     */
    public void deleteTask(String id) {
        if (!taskRepository.existsById(id)) {
            throw new TaskNotFoundException(id);
        }
        taskRepository.deleteById(id);
    }
    
    /**
     * Execute a task and store execution result
     * Uses Kubernetes API if available, otherwise falls back to local execution
     */
    public TaskExecution executeTask(String taskId) {
        Task task = taskRepository.findById(taskId)
            .orElseThrow(() -> new TaskNotFoundException(taskId));
        
        TaskExecution execution = new TaskExecution();
        execution.setStartTime(new Date());
        
        try {
            String output;
            // Try Kubernetes execution first if available
            if (kubernetesExecutionService != null && kubernetesExecutionService.isKubernetesAvailable()) {
                output = kubernetesExecutionService.executeInKubernetes(task.getCommand());
            } else {
                // Fall back to local execution
                output = executeCommandLocally(task.getCommand());
            }
            execution.setOutput(output);
        } catch (Exception e) {
            execution.setOutput("Error: " + e.getMessage());
        }
        
        execution.setEndTime(new Date());
        
        // Add execution to task
        task.getTaskExecutions().add(execution);
        taskRepository.save(task);
        
        return execution;
    }
    
    /**
     * Execute command locally (placeholder for Task 1)
     */
    private String executeCommandLocally(String command) throws Exception {
        // For Windows
        ProcessBuilder processBuilder;
        String os = System.getProperty("os.name").toLowerCase();
        
        if (os.contains("win")) {
            processBuilder = new ProcessBuilder("cmd.exe", "/c", command);
        } else {
            processBuilder = new ProcessBuilder("sh", "-c", command);
        }
        
        processBuilder.redirectErrorStream(true);
        Process process = processBuilder.start();
        
        StringBuilder output = new StringBuilder();
        try (BufferedReader reader = new BufferedReader(
                new InputStreamReader(process.getInputStream()))) {
            String line;
            while ((line = reader.readLine()) != null) {
                output.append(line).append("\n");
            }
        }
        
        process.waitFor();
        return output.toString();
    }
}
