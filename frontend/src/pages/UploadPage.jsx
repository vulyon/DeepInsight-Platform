import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Card,
  Upload,
  Button,
  message,
  Spin,
  Typography,
  Space,
  Alert,
} from 'antd'
import { InboxOutlined, UploadOutlined, FileTextOutlined, ThunderboltOutlined } from '@ant-design/icons'
import { uploadFile, startAnalysis } from '../services/api'
import './UploadPage.css'

const { Dragger } = Upload
const { Title, Paragraph, Text } = Typography

function UploadPage() {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [loadingDemo, setLoadingDemo] = useState(false)
  const [fileList, setFileList] = useState([])

  const handleLoadDemo = React.useCallback(async () => {
    if (loadingDemo) return // 防止重复调用
    
    setLoadingDemo(true)
    try {
      // 从后端加载示例数据
      message.loading('正在加载示例数据...', 0)
      
      const response = await fetch('/api/upload/demo/load', {
        method: 'POST',
      })
      
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || '无法加载示例数据')
      }
      
      const result = await response.json()
      message.destroy()
      message.success('示例数据加载成功！')
      
      // 开始分析
      message.loading('正在开始分析...', 0)
      const analysisResult = await startAnalysis(result.file_id)
      message.destroy()
      message.success('分析任务已启动！')
      
      // 跳转到分析结果页面
      navigate(`/analysis/${analysisResult.task_id}`)
    } catch (error) {
      message.destroy()
      message.error(error.message || '加载示例数据失败，请手动上传文件')
    } finally {
      setLoadingDemo(false)
    }
  }, [navigate, loadingDemo])

  // 检查URL参数，如果包含 autoLoadDemo=true，则自动加载示例数据
  React.useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search)
    if (urlParams.get('autoLoadDemo') === 'true' && !loadingDemo) {
      // 延迟一下，确保组件完全加载
      setTimeout(() => {
        handleLoadDemo()
      }, 500)
    }
  }, [handleLoadDemo, loadingDemo])

  const handleUpload = async () => {
    if (fileList.length === 0) {
      message.warning('请先选择要上传的文件')
      return
    }

    const file = fileList[0].originFileObj
    if (!file) {
      message.warning('文件无效')
      return
    }

    setLoading(true)
    try {
      // 上传文件
      message.loading('正在上传文件...', 0)
      const uploadResult = await uploadFile(file)
      message.destroy()
      message.success('文件上传成功！')

      // 开始分析
      message.loading('正在开始分析...', 0)
      const analysisResult = await startAnalysis(uploadResult.file_id)
      message.destroy()
      message.success('分析任务已启动！')

      // 跳转到分析结果页面
      navigate(`/analysis/${analysisResult.task_id}`)
    } catch (error) {
      message.destroy()
      message.error(error.message || '操作失败，请重试')
    } finally {
      setLoading(false)
    }
  }

  const uploadProps = {
    name: 'file',
    multiple: false,
    accept: '.csv',
    fileList,
    beforeUpload: (file) => {
      const isCSV = file.name.endsWith('.csv')
      if (!isCSV) {
        message.error('只能上传CSV格式的文件！')
        return Upload.LIST_IGNORE
      }
      const isLt10M = file.size / 1024 / 1024 < 10
      if (!isLt10M) {
        message.error('文件大小不能超过10MB！')
        return Upload.LIST_IGNORE
      }
      setFileList([{ ...file, status: 'done' }])
      return false
    },
    onRemove: () => {
      setFileList([])
    },
  }


  return (
    <div className="upload-page">
      <Card className="upload-card">
        <Space direction="vertical" size="large" style={{ width: '100%' }}>
          <div className="upload-header">
            <Title level={2}>
              <FileTextOutlined /> 数据上传
            </Title>
            <Paragraph type="secondary">
              请上传包含评论数据的CSV文件，系统将自动进行情感分析
            </Paragraph>
          </div>

          <Alert
            message="文件格式要求"
            description={
              <div>
                <p>• CSV格式文件，包含 <Text code>content</Text> 和 <Text code>content_type</Text> 列</p>
                <p>• 文件大小不超过10MB</p>
                <p>• 示例格式：</p>
                <pre className="format-example">
{`content,content_type
"这个产品很好用",pos
"质量太差了",neg`}
                </pre>
              </div>
            }
            type="info"
            showIcon
            style={{ marginBottom: 24 }}
          />

          <Dragger {...uploadProps} className="upload-dragger">
            <p className="ant-upload-drag-icon">
              <InboxOutlined />
            </p>
            <p className="ant-upload-text">点击或拖拽文件到此区域上传</p>
            <p className="ant-upload-hint">
              支持单个CSV文件上传，文件将自动进行验证
            </p>
          </Dragger>

          <Space direction="vertical" size="middle" style={{ width: '100%' }}>
            <Button
              type="default"
              size="large"
              icon={<ThunderboltOutlined />}
              onClick={handleLoadDemo}
              loading={loadingDemo}
              block
              className="demo-button"
            >
              {loadingDemo ? '加载中...' : '⚡ 快速体验（使用示例数据）'}
            </Button>
            
            <div style={{ textAlign: 'center', color: '#999', fontSize: '12px' }}>
              或
            </div>
            
            <Button
              type="primary"
              size="large"
              icon={<UploadOutlined />}
              onClick={handleUpload}
              loading={loading}
              block
              disabled={fileList.length === 0}
              className="upload-button"
            >
              {loading ? '处理中...' : '上传并开始分析'}
            </Button>
          </Space>
        </Space>
      </Card>
    </div>
  )
}

export default UploadPage

