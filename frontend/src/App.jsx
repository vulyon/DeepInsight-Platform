import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Layout } from 'antd'
import UploadPage from './pages/UploadPage'
import AnalysisPage from './pages/AnalysisPage'
import './App.css'

const { Header, Content } = Layout

function App() {
  return (
    <BrowserRouter>
      <Layout className="app-layout">
        <Header className="app-header">
          <div className="header-content">
            <h1 className="app-title">DeepInsight 电商产品分析平台</h1>
            <p className="app-subtitle">基于LSTM的情感分析可视化系统</p>
          </div>
        </Header>
        <Content className="app-content">
          <Routes>
            <Route path="/" element={<Navigate to="/upload" replace />} />
            <Route path="/upload" element={<UploadPage />} />
            <Route path="/analysis/:taskId" element={<AnalysisPage />} />
          </Routes>
        </Content>
      </Layout>
    </BrowserRouter>
  )
}

export default App

