package com.kaiburr.taskmanager.controller;

import com.kaiburr.taskmanager.exception.InvalidCommandException;
import com.kaiburr.taskmanager.exception.TaskNotFoundException;
import com.kaiburr.taskmanager.model.Task;
import com.kaiburr.taskmanager.model.TaskExecution;
import com.kaiburr.taskmanager.service.TaskService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/tasks")
@CrossOrigin(origins = "*")
public class TaskController {
    
    @Autowired
    private TaskService taskService;
    
    /**
     * GET /api/tasks - Get all tasks
     * GET /api/tasks?id={id} - Get task by ID
     */
    @GetMapping
    public ResponseEntity<?> getTasks(@RequestParam(required = false) String id) {
        if (id != null) {
            return taskService.getTaskById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
        }
        return ResponseEntity.ok(taskService.getAllTasks());
    }
    
    /**
     * GET /api/tasks/search?name={name} - Find tasks by name
     * GET /api/tasks/search?owner={owner} - Find tasks by owner (assignedTo)
     */
    @GetMapping("/search")
    public ResponseEntity<?> searchTasks(
            @RequestParam(required = false) String name,
            @RequestParam(required = false) String owner) {
        
        List<Task> tasks;
        
        if (name != null && !name.trim().isEmpty()) {
            tasks = taskService.findTasksByName(name);
        } else if (owner != null && !owner.trim().isEmpty()) {
            tasks = taskService.findTasksByOwner(owner);
        } else {
            return ResponseEntity.badRequest()
                .body(Map.of("error", "Please provide 'name' or 'owner' parameter"));
        }
        
        if (tasks.isEmpty()) {
            return ResponseEntity.ok(tasks); // Return empty list instead of 404
        }
        return ResponseEntity.ok(tasks);
    }
    
    /**
     * POST /api/tasks - Create a new task
     */
    @PostMapping
    public ResponseEntity<?> createTask(@Valid @RequestBody Task task) {
        try {
            Task savedTask = taskService.saveTask(task);
            return ResponseEntity.status(HttpStatus.CREATED).body(savedTask);
        } catch (InvalidCommandException e) {
            Map<String, String> error = new HashMap<>();
            error.put("error", e.getMessage());
            return ResponseEntity.badRequest().body(error);
        }
    }

    /**
     * PUT /api/tasks - Create or update a task
     */
    @PutMapping
    public ResponseEntity<?> createOrUpdateTask(@Valid @RequestBody Task task) {
        try {
            Task savedTask = taskService.saveTask(task);
            return ResponseEntity.ok(savedTask);
        } catch (InvalidCommandException e) {
            return ResponseEntity.badRequest()
                .body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * DELETE /api/tasks/{id} - Delete a task
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<?> deleteTask(@PathVariable String id) {
        try {
            taskService.deleteTask(id);
            return ResponseEntity.ok(Map.of("message", "Task deleted successfully"));
        } catch (TaskNotFoundException e) {
            return ResponseEntity.notFound().build();
        }
    }
    
    /**
     * PUT /api/tasks/{id}/execute - Execute a task
     */
    @PutMapping("/{id}/execute")
    public ResponseEntity<?> executeTask(@PathVariable String id) {
        try {
            TaskExecution execution = taskService.executeTask(id);
            return ResponseEntity.ok(execution);
        } catch (TaskNotFoundException e) {
            return ResponseEntity.notFound().build();
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * Exception handler for validation errors
     */
    @ExceptionHandler(Exception.class)
    public ResponseEntity<?> handleException(Exception e) {
        Map<String, String> error = new HashMap<>();
        error.put("error", e.getMessage());
        return ResponseEntity.badRequest().body(error);
    }
}
