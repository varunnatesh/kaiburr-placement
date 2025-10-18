import React from 'react';
import { Modal, Typography, Empty, Timeline, Tag } from 'antd';
import { ClockCircleOutlined, CheckCircleOutlined } from '@ant-design/icons';
import { Task } from '../types/Task';
import dayjs from 'dayjs';

const { Title, Text, Paragraph } = Typography;

interface TaskDetailProps {
  visible: boolean;
  task: Task | null;
  onClose: () => void;
}

const TaskDetail: React.FC<TaskDetailProps> = ({ visible, task, onClose }) => {
  if (!task) return null;

  const formatDate = (dateStr: string) => {
    return dayjs(dateStr).format('YYYY-MM-DD HH:mm:ss');
  };

  const calculateDuration = (start: string, end: string) => {
    const startTime = dayjs(start);
    const endTime = dayjs(end);
    const duration = endTime.diff(startTime, 'millisecond');
    return `${duration}ms`;
  };

  return (
    <Modal
      title="Task Details"
      open={visible}
      onCancel={onClose}
      footer={null}
      width={700}
      destroyOnHidden
    >
      <div style={{ marginBottom: 24 }}>
        <Title level={4}>{task.name}</Title>
        <div style={{ marginBottom: 8 }}>
          <Text strong>ID: </Text>
          <Tag color="blue">{task.id}</Tag>
        </div>
        <div style={{ marginBottom: 8 }}>
          <Text strong>Owner: </Text>
          <Text>{task.owner}</Text>
        </div>
        <div style={{ marginBottom: 8 }}>
          <Text strong>Command: </Text>
          <Text code>{task.command}</Text>
        </div>
      </div>

      <Title level={5}>Execution History</Title>
      {task.taskExecutions && task.taskExecutions.length > 0 ? (
        <Timeline
          items={task.taskExecutions.map((execution, index) => ({
            color: 'green',
            dot: index === task.taskExecutions.length - 1 ? 
              <CheckCircleOutlined style={{ fontSize: '16px' }} /> : 
              <ClockCircleOutlined style={{ fontSize: '16px' }} />,
            children: (
              <div key={index}>
                <div>
                  <Text strong>Start: </Text>
                  <Text>{formatDate(execution.startTime)}</Text>
                </div>
                <div>
                  <Text strong>End: </Text>
                  <Text>{formatDate(execution.endTime)}</Text>
                </div>
                <div>
                  <Text strong>Duration: </Text>
                  <Text>{calculateDuration(execution.startTime, execution.endTime)}</Text>
                </div>
                <div style={{ marginTop: 8 }}>
                  <Text strong>Output:</Text>
                  <Paragraph
                    code
                    style={{
                      backgroundColor: '#f5f5f5',
                      padding: '8px',
                      marginTop: 4,
                      borderRadius: 4,
                      whiteSpace: 'pre-wrap',
                      maxHeight: 200,
                      overflow: 'auto'
                    }}
                  >
                    {execution.output || 'No output'}
                  </Paragraph>
                </div>
              </div>
            )
          }))}
        />
      ) : (
        <Empty 
          description="No executions yet"
          style={{ margin: '20px 0' }}
        />
      )}
    </Modal>
  );
};

export default TaskDetail;
