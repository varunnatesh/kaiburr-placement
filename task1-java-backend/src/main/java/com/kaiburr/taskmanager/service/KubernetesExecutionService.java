package com.kaiburr.taskmanager.service;

import io.kubernetes.client.openapi.ApiClient;
import io.kubernetes.client.openapi.ApiException;
import io.kubernetes.client.openapi.Configuration;
import io.kubernetes.client.openapi.apis.CoreV1Api;
import io.kubernetes.client.openapi.models.*;
import io.kubernetes.client.util.Config;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Collections;

@Service
public class KubernetesExecutionService {
    
    private static final Logger logger = LoggerFactory.getLogger(KubernetesExecutionService.class);
    private CoreV1Api api;
    private String namespace;
    private boolean enabled;
    
    public KubernetesExecutionService() {
        // Gate Kubernetes usage behind an env flag (disabled by default for Task 1)
        this.enabled = "true".equalsIgnoreCase(System.getenv().getOrDefault("ENABLE_K8S", "false"));
        this.namespace = System.getenv().getOrDefault("KUBERNETES_NAMESPACE", "default");

        if (!this.enabled) {
            this.api = null;
            logger.info("Kubernetes execution disabled (ENABLE_K8S=false). Falling back to local execution.");
            return;
        }

        try {
            // Initialize Kubernetes client (best-effort; non-fatal for Task 1)
            ApiClient client = Config.defaultClient();
            Configuration.setDefaultApiClient(client);
            this.api = new CoreV1Api();
            logger.info("Kubernetes client initialized. Namespace={}", this.namespace);
        } catch (Exception e) {
            // Do NOT fail application startup; just disable K8s execution
            this.api = null;
            this.enabled = false;
            logger.warn("Kubernetes not available. Continuing without K8s execution. Reason: {}", e.getMessage());
        }
    }
    
    /**
     * Execute a command in a Kubernetes pod
     */
    public String executeInKubernetes(String command) throws Exception {
        if (api == null) {
            throw new IllegalStateException("Kubernetes API client is not available");
        }
        String podName = "task-execution-" + System.currentTimeMillis();
        
        try {
            // Create pod
            V1Pod pod = createPod(podName, command);
            api.createNamespacedPod(namespace, pod, null, null, null, null);
            
            logger.info("Created pod: " + podName);
            
            // Wait for pod to complete
            String phase = waitForPodCompletion(podName, 60);
            
            // Get pod logs
            String logs = getPodLogs(podName);
            
            // Clean up pod
            deletePod(podName);
            
            return logs;
            
        } catch (ApiException e) {
            logger.error("Kubernetes API error: " + e.getResponseBody());
            throw new Exception("Failed to execute in Kubernetes: " + e.getMessage());
        }
    }
    
    /**
     * Create a pod specification for command execution
     */
    private V1Pod createPod(String podName, String command) {
        V1Pod pod = new V1Pod();
        V1ObjectMeta metadata = new V1ObjectMeta();
        metadata.setName(podName);
        metadata.setLabels(Collections.singletonMap("app", "task-execution"));
        pod.setMetadata(metadata);

        V1Container container = new V1Container();
        container.setName("task-container");
        container.setImage("busybox:latest");
        container.setCommand(java.util.Arrays.asList("sh", "-c", command));

        V1PodSpec spec = new V1PodSpec();
        spec.setRestartPolicy("Never");
        spec.setContainers(java.util.Collections.singletonList(container));

        pod.setSpec(spec);
        return pod;
    }
    
    /**
     * Wait for pod to complete execution
     */
    private String waitForPodCompletion(String podName, int timeoutSeconds) throws Exception {
        int elapsed = 0;
        while (elapsed < timeoutSeconds) {
            try {
                V1Pod pod = api.readNamespacedPod(podName, namespace, null);
                String phase = pod.getStatus().getPhase();
                
                if ("Succeeded".equals(phase) || "Failed".equals(phase)) {
                    return phase;
                }
                
                Thread.sleep(1000);
                elapsed++;
            } catch (ApiException e) {
                logger.error("Error checking pod status: " + e.getMessage());
                throw e;
            }
        }
        throw new Exception("Pod execution timeout");
    }
    
    /**
     * Get logs from a pod
     */
    private String getPodLogs(String podName) throws ApiException {
        try {
            return api.readNamespacedPodLog(
                podName, 
                namespace, 
                null,  // container
                null,  // follow
                null,  // insecureSkipTLSVerifyBackend
                null,  // limitBytes
                null,  // pretty
                null,  // previous
                null,  // sinceSeconds
                null,  // tailLines
                null   // timestamps
            );
        } catch (ApiException e) {
            logger.error("Error getting pod logs: " + e.getMessage());
            return "Error retrieving logs: " + e.getMessage();
        }
    }
    
    /**
     * Delete a pod
     */
    private void deletePod(String podName) {
        try {
            api.deleteNamespacedPod(
                podName, 
                namespace, 
                null, 
                null, 
                null, 
                null, 
                null, 
                null
            );
            logger.info("Deleted pod: " + podName);
        } catch (ApiException e) {
            logger.error("Error deleting pod: " + e.getMessage());
        }
    }
    
    /**
     * Check if running in Kubernetes environment
     */
    public boolean isKubernetesAvailable() {
        return enabled && api != null;
    }
}
