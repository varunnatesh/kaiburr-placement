import React, { useState } from 'react';
import { Modal, Form, Input, message } from 'antd';
import { TaskFormData } from '../types/Task';
import { taskService } from '../services/taskService';

interface TaskFormProps {
  visible: boolean;
  task?: TaskFormData;
  onClose: () => void;
  onSuccess: () => void;
}

const TaskForm: React.FC<TaskFormProps> = ({ visible, task, onClose, onSuccess }) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);

  React.useEffect(() => {
    if (visible) {
      if (task) {
        form.setFieldsValue(task);
      } else {
        form.resetFields();
      }
    }
  }, [visible, task, form]);

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      console.log('Submitting task values:', values);
      setLoading(true);

      const result = await taskService.saveTask(values);
      console.log('Save result:', result);
      message.success(task ? 'Task updated successfully' : 'Task created successfully');
      onSuccess();
      onClose();
    } catch (error: any) {
      console.error('Save error:', error);
      if (error.response?.data?.error) {
        message.error(error.response.data.error);
      } else if (error.errorFields) {
        message.error('Please fill in all required fields');
      } else {
        message.error('Failed to save task');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal
      title={task ? 'Edit Task' : 'Create New Task'}
      open={visible}
      onOk={handleSubmit}
      onCancel={onClose}
      confirmLoading={loading}
      okText="Save"
      cancelText="Cancel"
      destroyOnHidden
    >
      <Form
        form={form}
        layout="vertical"
        aria-label={task ? 'Edit task form' : 'Create task form'}
      >
        <Form.Item
          name="id"
          label="Task ID"
          rules={[{ required: true, message: 'Please enter task ID' }]}
        >
          <Input 
            placeholder="Enter task ID" 
            disabled={!!task}
            aria-label="Task ID"
            aria-required="true"
          />
        </Form.Item>

        <Form.Item
          name="name"
          label="Task Name"
          rules={[{ required: true, message: 'Please enter task name' }]}
        >
          <Input 
            placeholder="Enter task name"
            aria-label="Task name"
            aria-required="true"
          />
        </Form.Item>

        <Form.Item
          name="owner"
          label="Owner"
          rules={[{ required: true, message: 'Please enter owner name' }]}
        >
          <Input 
            placeholder="Enter owner name"
            aria-label="Owner name"
            aria-required="true"
          />
        </Form.Item>

        <Form.Item
          name="command"
          label="Command"
          rules={[{ required: true, message: 'Please enter command' }]}
          extra="Enter a safe shell command (dangerous commands are blocked)"
        >
          <Input.TextArea
            placeholder="Enter command (e.g., echo Hello World)"
            rows={3}
            aria-label="Command"
            aria-required="true"
            aria-describedby="command-help"
          />
        </Form.Item>
      </Form>
    </Modal>
  );
};

export default TaskForm;
