# Task 3: React Frontend with TypeScript and Ant Design

## Overview
A modern, accessible web UI for the Task Manager application built with React 19, TypeScript, and Ant Design. Provides full CRUD operations, task execution, and execution history viewing.

## Technologies Used
- React 19
- TypeScript
- Ant Design 5.x
- Axios (API client)
- Vite (Build tool)
- Day.js (Date formatting)

## Features
- ✅ Create new tasks with validation
- ✅ View all tasks in a sortable, paginated table
- ✅ Search tasks by name
- ✅ Execute tasks and view real-time results
- ✅ View detailed execution history with timestamps
- ✅ Delete tasks with confirmation
- ✅ Fully accessible (WCAG 2.1 compliant)
- ✅ Responsive design
- ✅ Error handling and user feedback

## Prerequisites
- Node.js 18+ and npm/yarn
- Task 1 backend running on http://localhost:8080

## Installation

### 1. Install Dependencies

```powershell
cd task3-react-frontend
npm install
```

### 2. Start Development Server

```powershell
npm run dev
```

The application will start on http://localhost:3000

### 3. Build for Production

```powershell
npm run build
```

Built files will be in the `dist/` directory.

## Project Structure

```
task3-react-frontend/
├── src/
│   ├── components/
│   │   ├── TaskList.tsx       # Main task list view
│   │   ├── TaskForm.tsx        # Create/edit task form
│   │   └── TaskDetail.tsx      # Task details modal
│   ├── services/
│   │   └── taskService.ts      # API service layer
│   ├── types/
│   │   └── Task.ts             # TypeScript interfaces
│   ├── App.tsx                 # Main app component
│   ├── App.css                 # Global styles
│   └── main.tsx                # Entry point
├── index.html
├── vite.config.ts              # Vite configuration
├── tsconfig.json               # TypeScript config
├── package.json
└── README.md
```

## Component Overview

### TaskList Component
The main view showing all tasks in a table format.

**Features:**
- Paginated table with 10 tasks per page
- Real-time search functionality
- Inline actions (Run, View, Delete)
- Loading states
- Empty states

**Accessibility:**
- ARIA labels on all interactive elements
- Keyboard navigation support
- Screen reader friendly
- Focus indicators

### TaskForm Component
Modal form for creating/editing tasks.

**Features:**
- Form validation
- Required field indicators
- Command safety warning
- Error handling
- Loading states during submission

**Accessibility:**
- Proper form labels
- Required field announcements
- Error message associations
- Keyboard accessible

### TaskDetail Component
Modal showing detailed task information and execution history.

**Features:**
- Task metadata display
- Timeline of all executions
- Formatted timestamps and durations
- Output display with scrolling
- Empty state for tasks without executions

**Accessibility:**
- Semantic HTML structure
- Readable date formats
- Color-coded visual indicators
- Keyboard navigation

## API Integration

The application communicates with the backend through the `taskService`:

```typescript
// Get all tasks
taskService.getAllTasks()

// Search tasks
taskService.searchTasks(name)

// Create/update task
taskService.saveTask(taskData)

// Execute task
taskService.executeTask(taskId)

// Delete task
taskService.deleteTask(taskId)
```

## Configuration

### API Endpoint
The API endpoint is configured in `vite.config.ts` (proxy via kubectl proxy):

```typescript
server: {
  port: 3000,
  proxy: {
    '/api': {
      target: 'http://localhost:8001/api/v1/namespaces/default/services/task-manager:8080/proxy',
      changeOrigin: true,
      rewrite: (path) => path,
    }
  }
}
```

To change the backend URL, modify the `target` value. If you prefer NodePort, point to `http://localhost:30080` instead and remove the path suffix.

## Accessibility Features

### WCAG 2.1 AA Compliance
- ✅ Semantic HTML
- ✅ ARIA labels and roles
- ✅ Keyboard navigation
- ✅ Focus indicators
- ✅ Color contrast ratios
- ✅ Screen reader support
- ✅ Form validation announcements
- ✅ Error message associations

### Keyboard Navigation
- `Tab` - Navigate between elements
- `Enter` - Activate buttons
- `Esc` - Close modals
- `Arrow keys` - Navigate tables and dropdowns

### Screen Reader Support
All interactive elements have descriptive labels:
- Buttons announce their action
- Form fields announce their purpose and requirements
- Tables announce row and column context
- Modals announce their purpose

## Usage Guide

### Creating a Task
1. Click "Create Task" button
2. Fill in the form:
   - **ID**: Unique identifier
   - **Name**: Descriptive name
   - **Owner**: Person responsible
   - **Command**: Shell command to execute
3. Click "Save"

### Executing a Task
1. Find the task in the table
2. Click the "Run" button
3. Wait for execution to complete
4. View the result in the task details

### Viewing Task Details
1. Click the "View" button on any task
2. See task metadata and execution history
3. Review command outputs and timestamps

### Searching Tasks
1. Type in the search box
2. Press Enter or click search icon
3. Choose search by Name or Owner using the dropdown
4. Clear search to see all tasks

### Deleting a Task
1. Click the delete button (trash icon)
2. Confirm deletion in the modal
3. Task is removed from the list

## Testing the Application

### Manual Testing Checklist
- [ ] Create a new task successfully
- [ ] Create task with empty fields (should show validation errors)
- [ ] Create task with unsafe command (should be rejected by backend)
- [ ] View all tasks in the table
- [ ] Search for existing task by name
- [ ] Search for non-existent task (should show empty state)
- [ ] Execute a task and view the output
- [ ] View task details and execution history
- [ ] Delete a task
- [ ] Cancel delete operation
- [ ] Test keyboard navigation (Tab, Enter, Esc)
- [ ] Test responsive design on different screen sizes
- [ ] Test with screen reader (if available)

## Common Issues

### Backend Connection Error
**Problem:** Cannot connect to API
**Solution:** Ensure Task 1 backend is running on http://localhost:8080

### CORS Issues
**Problem:** CORS policy blocking requests
**Solution:** Backend should allow CORS from frontend origin

### Build Errors
**Problem:** TypeScript errors during build
**Solution:** Run `npm install` to ensure all dependencies are installed

## Development Scripts

```powershell
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linter
npm run lint
```

## Deployment

### Build and Deploy
```powershell
# Build the application
npm run build

# Deploy the dist/ folder to your hosting service
# Examples: Netlify, Vercel, GitHub Pages, AWS S3, etc.
```

### Environment Variables
For production, update the API URL in `vite.config.ts` or use environment variables.

## Screenshots

[Add screenshots showing:]
1. Main task list view with data
2. Create task form
3. Task execution in progress
4. Task details modal with execution history
5. Search functionality
6. Delete confirmation
7. Responsive design on mobile
8. Accessibility features (focus indicators, keyboard navigation)
9. Your name and timestamp visible in each screenshot

## Browser Support
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## Next Steps
- Task 4: Set up CI/CD pipeline for automated builds and deployments

## Author
[Your Name]
Date: October 16, 2025
