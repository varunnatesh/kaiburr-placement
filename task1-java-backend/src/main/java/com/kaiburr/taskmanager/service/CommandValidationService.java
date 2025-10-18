package com.kaiburr.taskmanager.service;

import com.kaiburr.taskmanager.exception.InvalidCommandException;
import org.springframework.stereotype.Service;

import java.util.Arrays;
import java.util.List;
import java.util.regex.Pattern;

@Service
public class CommandValidationService {
    
    // List of dangerous commands and patterns
    private static final List<String> DANGEROUS_COMMANDS = Arrays.asList(
        "rm", "rmdir", "del", "format", "mkfs",
        "dd", "mv", ">", ">>", "curl", "wget",
        "nc", "netcat", "telnet", "ssh", "ftp",
        "chmod", "chown", "sudo", "su", "exec",
        "eval", "source", "systemctl", "service",
        "reboot", "shutdown", "init", "kill", "killall"
    );
    
    // Pattern for command injection attempts
    private static final Pattern COMMAND_INJECTION_PATTERN = 
        Pattern.compile("[;&|`$()<>]");
    
    /**
     * Validates if a command is safe to execute
     * @param command the command to validate
     * @throws InvalidCommandException if the command is deemed unsafe
     */
    public void validateCommand(String command) {
        if (command == null || command.trim().isEmpty()) {
            throw new InvalidCommandException("Command cannot be empty");
        }
        
        String lowerCommand = command.toLowerCase().trim();
        
        // Check for dangerous commands
        for (String dangerous : DANGEROUS_COMMANDS) {
            if (lowerCommand.contains(dangerous)) {
                throw new InvalidCommandException(
                    "Command contains potentially dangerous operation: " + dangerous
                );
            }
        }
        
        // Check for command injection patterns
        if (COMMAND_INJECTION_PATTERN.matcher(command).find()) {
            throw new InvalidCommandException(
                "Command contains potentially malicious characters"
            );
        }
        
        // Additional check for encoded characters
        if (command.contains("%") || command.contains("\\x")) {
            throw new InvalidCommandException(
                "Command contains potentially encoded malicious content"
            );
        }
    }
}
