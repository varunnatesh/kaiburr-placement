import React from 'react';
import { ConfigProvider, theme } from 'antd';
import TaskList from './components/TaskList';
import './App.css';

const App: React.FC = () => {
  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: '#1890ff',
          borderRadius: 6,
        },
        algorithm: theme.defaultAlgorithm,
      }}
    >
      <div className="App">
        <TaskList />
      </div>
    </ConfigProvider>
  );
};

export default App;
