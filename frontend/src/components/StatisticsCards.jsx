import React from 'react'
import { Row, Col, Card, Statistic } from 'antd'
import {
  FileTextOutlined,
  LikeOutlined,
  DislikeOutlined,
  CheckCircleOutlined,
} from '@ant-design/icons'
import './StatisticsCards.css'

function StatisticsCards({ statistics }) {
  if (!statistics) return null

  const { total, positive, negative, positive_rate, accuracy } = statistics

  const cards = [
    {
      title: '总评论数',
      value: total || 0,
      prefix: <FileTextOutlined />,
      valueStyle: { color: '#1890ff' },
    },
    {
      title: '正面评论',
      value: positive || 0,
      suffix: `(${((positive_rate || 0) * 100).toFixed(1)}%)`,
      prefix: <LikeOutlined />,
      valueStyle: { color: '#52c41a' },
    },
    {
      title: '负面评论',
      value: negative || 0,
      suffix: `${(((negative || 0) / (total || 1)) * 100).toFixed(1)}%`,
      prefix: <DislikeOutlined />,
      valueStyle: { color: '#ff4d4f' },
    },
    {
      title: '模型准确率',
      value: accuracy ? (accuracy * 100).toFixed(1) : '0.0',
      suffix: '%',
      prefix: <CheckCircleOutlined />,
      valueStyle: { color: '#722ed1' },
    },
  ]

  return (
    <Row gutter={[16, 16]} className="statistics-cards">
      {cards.map((card, index) => (
        <Col xs={24} sm={12} lg={6} key={index}>
          <Card className="stat-card" hoverable>
            <Statistic
              title={card.title}
              value={card.value}
              suffix={card.suffix}
              prefix={card.prefix}
              valueStyle={card.valueStyle}
            />
          </Card>
        </Col>
      ))}
    </Row>
  )
}

export default StatisticsCards

