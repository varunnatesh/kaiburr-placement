package com.kaiburr.taskmanager.util;

import com.kaiburr.taskmanager.model.Task;
import com.kaiburr.taskmanager.repository.TaskRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.Arrays;
import java.util.List;

@Configuration
public class SampleDataLoader {

    @Bean
    CommandLineRunner loadSampleData(TaskRepository taskRepository) {
        return args -> {
            // Check if data already exists
            long count = taskRepository.count();
            if (count > 0) {
                System.out.println("Sample data already exists. Skipping data load.");
                return;
            }

            System.out.println("Loading sample tasks into database...");

            List<Task> sampleTasks = Arrays.asList(
                new Task("1", "Deploy Application", "John Doe", "echo Deploying application", null),
                new Task("2", "Run Tests", "Jane Smith", "echo Running tests", null),
                new Task("3", "Database Backup", "John Doe", "echo Backing up database", null),
                new Task("4", "Deploy Frontend", "Alice Johnson", "echo Deploying frontend", null),
                new Task("5", "Monitor System", "Bob Wilson", "echo Monitoring system", null)
            );

            taskRepository.saveAll(sampleTasks);
            System.out.println("Sample data loaded successfully! Added " + sampleTasks.size() + " tasks.");
            System.out.println("You can now test search by:");
            System.out.println("  - Name: 'Deploy', 'Test', 'Backup', etc.");
            System.out.println("  - Owner: 'John Doe', 'Jane Smith', 'Alice Johnson', 'Bob Wilson'");
        };
    }
}
