package com.kaiburr.taskmanager.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import jakarta.validation.constraints.NotBlank;
import java.util.ArrayList;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Document(collection = "tasks")
public class Task {
    @Id
    private String id;
    
    @NotBlank(message = "Task name is required")
    private String name;
    
    @NotBlank(message = "Owner is required")
    private String owner;
    
    @NotBlank(message = "Command is required")
    private String command;
    
    private List<TaskExecution> taskExecutions = new ArrayList<>();
}
