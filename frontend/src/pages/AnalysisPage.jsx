import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  Spin,
  message,
  Row,
  Col,
  Button,
  Space,
  Card,
  Alert,
  Tabs,
} from 'antd'
import {
  ArrowLeftOutlined,
  ReloadOutlined,
  CheckCircleOutlined,
} from '@ant-design/icons'
import { getResults } from '../services/api'
import StatisticsCards from '../components/StatisticsCards'
import WordCloudChart from '../components/WordCloudChart'
import PieChart from '../components/PieChart'
import HeatmapChart from '../components/HeatmapChart'
import LineChart from '../components/LineChart'
import Bar3DChart from '../components/Bar3DChart'
import KeywordsList from '../components/KeywordsList'
import LDAVisualization from '../components/LDAVisualization'
import ReviewList from '../components/ReviewList'
import './AnalysisPage.css'

function AnalysisPage() {
  const { taskId } = useParams()
  const navigate = useNavigate()
  const [loading, setLoading] = useState(true)
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (taskId) {
      fetchResults()
    }
  }, [taskId])

  const fetchResults = async () => {
    setLoading(true)
    setError(null)
    try {
      const result = await getResults(taskId)
      setData(result)
    } catch (err) {
      setError(err.message || '获取分析结果失败')
      message.error(err.message || '获取分析结果失败')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="analysis-loading">
        <Spin size="large" tip="正在加载分析结果..." />
      </div>
    )
  }

  if (error || !data) {
    return (
      <div className="analysis-page">
        <Alert
          message="加载失败"
          description={error || '分析结果不存在'}
          type="error"
          showIcon
          action={
            <Space>
              <Button size="small" onClick={() => navigate('/upload')}>
                返回上传
              </Button>
              <Button size="small" type="primary" onClick={fetchResults}>
                重试
              </Button>
            </Space>
          }
        />
      </div>
    )
  }

  const { statistics, wordcloud, charts, status } = data

  return (
    <div className="analysis-page">
      <div className="analysis-header">
        <Space>
          <Button
            icon={<ArrowLeftOutlined />}
            onClick={() => navigate('/upload')}
          >
            返回上传
          </Button>
          <Button
            icon={<ReloadOutlined />}
            onClick={fetchResults}
            loading={loading}
          >
            刷新数据
          </Button>
        </Space>
        {status === 'completed' && (
          <Alert
            message="分析完成"
            description="所有数据已处理完成，可以查看详细结果"
            type="success"
            showIcon
            icon={<CheckCircleOutlined />}
            style={{ marginTop: 16 }}
          />
        )}
      </div>

      {/* 统计卡片 */}
      <StatisticsCards statistics={statistics} />

      {/* 分页显示 */}
      <Tabs
        defaultActiveKey="1"
        items={[
          {
            key: '1',
            label: '词云分析',
            children: (
              <Row gutter={[16, 16]}>
                <Col xs={24} lg={12}>
                  <WordCloudChart
                    title="正面评论词云"
                    imageData={wordcloud?.positive}
                    sentiment="positive"
                  />
                </Col>
                <Col xs={24} lg={12}>
                  <WordCloudChart
                    title="负面评论词云"
                    imageData={wordcloud?.negative}
                    sentiment="negative"
                  />
                </Col>
              </Row>
            ),
          },
          {
            key: '2',
            label: '统计分析',
            children: (
              <>
                <Row gutter={[16, 16]}>
                  <Col xs={24} lg={12}>
                    <PieChart data={charts?.pie_data} />
                  </Col>
                  <Col xs={24} lg={12}>
                    <HeatmapChart confusionMatrix={charts?.confusion_matrix} />
                  </Col>
                </Row>
                <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
                  <Col xs={24} lg={12}>
                    <LineChart data={charts?.time_series} />
                  </Col>
                  <Col xs={24} lg={12}>
                    <Bar3DChart data={charts?.bar_3d} />
                  </Col>
                </Row>
              </>
            ),
          },
          {
            key: '3',
            label: '主题模型',
            children: (
              <Row gutter={[16, 16]}>
                <Col xs={24}>
                  <LDAVisualization ldaData={charts?.lda} />
                </Col>
              </Row>
            ),
          },
          {
            key: '4',
            label: '关键词',
            children: (
              <Row gutter={[16, 16]}>
                <Col xs={24}>
                  <KeywordsList keywords={charts?.keywords} />
                </Col>
              </Row>
            ),
          },
          {
            key: '5',
            label: '评论列表',
            children: <ReviewList taskId={taskId} />,
          },
        ]}
      />
    </div>
  )
}

export default AnalysisPage

