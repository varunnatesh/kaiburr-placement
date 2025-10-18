import React, { useState, useEffect } from 'react';
import {
  Table,
  Button,
  Space,
  Input,
  Card,
  Typography,
  Tag,
  App as AntApp,
  Select,
} from 'antd';
import {
  PlusOutlined,
  DeleteOutlined,
  PlayCircleOutlined,
  EyeOutlined,
  SearchOutlined,
  ReloadOutlined,
} from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import { Task } from '../types/Task';
import { taskService } from '../services/taskService';
import TaskForm from './TaskForm';
import TaskDetail from './TaskDetail';

const { Title } = Typography;
const { Search } = Input;

const TaskList: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(false);
  const [formVisible, setFormVisible] = useState(false);
  const [detailVisible, setDetailVisible] = useState(false);
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);
  const [searchText, setSearchText] = useState('');
  const [searchType, setSearchType] = useState<'name' | 'owner'>('name');

  // Ant Design App context (React 19 compatible APIs)
  const { message, modal } = AntApp.useApp();

  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      setLoading(true);
      const data = await taskService.getAllTasks();
      setTasks(data);
    } catch (error) {
      message.error('Failed to load tasks');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (value: string) => {
    if (!value.trim()) {
      loadTasks();
      setSearchText('');
      return;
    }

    try {
      setLoading(true);
      setSearchText(value);
      const params = searchType === 'name' ? { name: value } : { owner: value };
      const data = await taskService.searchTasksBy(params);
      setTasks(data);
      if (data.length === 0) {
        message.info(`No tasks found ${searchType === 'name' ? 'with that name' : 'assigned to that person'}`);
      }
    } catch (error) {
      message.error('Failed to search tasks');
      setTasks([]);
    } finally {
      setLoading(false);
    }
  };

  const handleExecute = async (taskId: string) => {
    try {
      setLoading(true);
      await taskService.executeTask(taskId);
      message.success('Task executed successfully');
      loadTasks();
    } catch (error: any) {
      message.error(error.response?.data?.error || 'Failed to execute task');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = (taskId: string, taskName: string) => {
    modal.confirm({
      title: 'Delete Task',
      content: `Are you sure you want to delete "${taskName}"?`,
      okText: 'Delete',
      okType: 'danger',
      cancelText: 'Cancel',
      onOk: async () => {
        try {
          await taskService.deleteTask(taskId);
          message.success('Task deleted successfully');
          loadTasks();
        } catch (error) {
          message.error('Failed to delete task');
        }
      },
    });
  };

  const handleViewDetails = (task: Task) => {
    setSelectedTask(task);
    setDetailVisible(true);
  };

  const columns: ColumnsType<Task> = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 100,
      render: (id: string) => <Tag color="blue">{id}</Tag>,
    },
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
      width: 200,
    },
    {
      title: 'Owner',
      dataIndex: 'owner',
      key: 'owner',
      width: 150,
    },
    {
      title: 'Command',
      dataIndex: 'command',
      key: 'command',
      ellipsis: true,
      render: (command: string) => (
        <code style={{ fontSize: '12px' }}>{command}</code>
      ),
    },
    {
      title: 'Executions',
      dataIndex: 'taskExecutions',
      key: 'executions',
      width: 100,
      align: 'center',
      render: (executions: any[]) => (
        <Tag color={executions?.length > 0 ? 'green' : 'default'}>
          {executions?.length || 0}
        </Tag>
      ),
    },
    {
      title: 'Actions',
      key: 'actions',
      width: 200,
      fixed: 'right',
      render: (_, record) => (
        <Space size="small">
          <Button
            type="primary"
            icon={<PlayCircleOutlined />}
            onClick={() => handleExecute(record.id)}
            size="small"
            aria-label={`Execute task ${record.name}`}
          >
            Run
          </Button>
          <Button
            icon={<EyeOutlined />}
            onClick={() => handleViewDetails(record)}
            size="small"
            aria-label={`View details of task ${record.name}`}
          >
            View
          </Button>
          <Button
            danger
            icon={<DeleteOutlined />}
            onClick={() => handleDelete(record.id, record.name)}
            size="small"
            aria-label={`Delete task ${record.name}`}
          />
        </Space>
      ),
    },
  ];

  return (
    <div style={{ padding: '24px' }}>
      <Card>
        <div style={{ marginBottom: 16 }}>
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              marginBottom: 16,
            }}
          >
            <Title level={2} style={{ margin: 0 }}>
              Task Manager
            </Title>
            <Space>
              <Button
                icon={<ReloadOutlined />}
                onClick={loadTasks}
                aria-label="Reload tasks"
              >
                Refresh
              </Button>
              <Button
                type="primary"
                icon={<PlusOutlined />}
                onClick={() => setFormVisible(true)}
                aria-label="Create new task"
              >
                Create Task
              </Button>
            </Space>
          </div>

          <Space.Compact style={{ maxWidth: 500 }}>
            <Select
              value={searchType}
              onChange={setSearchType}
              style={{ width: 140 }}
              options={[
                { value: 'name', label: 'By Name' },
                { value: 'owner', label: 'By Owner' },
              ]}
            />
            <Search
              placeholder={searchType === 'name' ? 'Search by task name' : 'Search by owner'}
              allowClear
              enterButton={<SearchOutlined />}
              size="large"
              onSearch={handleSearch}
              value={searchText}
              onChange={(e) => {
                setSearchText(e.target.value);
                if (!e.target.value) {
                  loadTasks();
                }
              }}
              style={{ width: 360 }}
              aria-label="Search tasks"
            />
          </Space.Compact>
        </div>

        <Table
          columns={columns}
          dataSource={tasks}
          rowKey="id"
          loading={loading}
          pagination={{
            pageSize: 10,
            showSizeChanger: true,
            showTotal: (total) => `Total ${total} tasks`,
          }}
          scroll={{ x: 1000 }}
          aria-label="Tasks table"
        />
      </Card>

      <TaskForm
        visible={formVisible}
        onClose={() => {
          setFormVisible(false);
          setSelectedTask(null);
        }}
        onSuccess={loadTasks}
        task={selectedTask ? {
          id: selectedTask.id,
          name: selectedTask.name,
          owner: selectedTask.owner,
          command: selectedTask.command,
        } : undefined}
      />

      <TaskDetail
        visible={detailVisible}
        task={selectedTask}
        onClose={() => {
          setDetailVisible(false);
          setSelectedTask(null);
        }}
      />
    </div>
  );
};

export default TaskList;
