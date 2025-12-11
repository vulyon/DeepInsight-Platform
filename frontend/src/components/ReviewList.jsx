import React, { useState, useEffect } from 'react'
import { Card, Table, Tag, Select, Pagination, Space, Typography } from 'antd'
import { LikeOutlined, DislikeOutlined } from '@ant-design/icons'
import { getReviews } from '../services/api'
import './ReviewList.css'

const { Option } = Select
const { Text } = Typography

function ReviewList({ taskId }) {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(false)
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [pageSize, setPageSize] = useState(20)
  const [sentiment, setSentiment] = useState(null)

  useEffect(() => {
    if (taskId) {
      fetchReviews()
    }
  }, [taskId, page, pageSize, sentiment])

  const fetchReviews = async () => {
    setLoading(true)
    try {
      const params = {
        page,
        page_size: pageSize,
      }
      if (sentiment) {
        params.sentiment = sentiment
      }
      const result = await getReviews(taskId, params)
      setData(result.data || [])
      setTotal(result.total || 0)
    } catch (error) {
      console.error('获取评论列表失败:', error)
    } finally {
      setLoading(false)
    }
  }

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 80,
    },
    {
      title: '评论内容',
      dataIndex: 'content',
      key: 'content',
      ellipsis: true,
      render: (text) => <Text>{text}</Text>,
    },
    {
      title: '情感',
      dataIndex: 'sentiment',
      key: 'sentiment',
      width: 120,
      render: (sentiment) => {
        const isPositive = sentiment === 'pos' || sentiment === 'positive'
        return (
          <Tag
            icon={isPositive ? <LikeOutlined /> : <DislikeOutlined />}
            color={isPositive ? 'success' : 'error'}
          >
            {isPositive ? '正面' : '负面'}
          </Tag>
        )
      },
    },
    {
      title: '置信度',
      dataIndex: 'confidence',
      key: 'confidence',
      width: 120,
      render: (confidence) => {
        const percent = (confidence * 100).toFixed(1)
        const color = confidence > 0.7 ? '#52c41a' : confidence > 0.5 ? '#faad14' : '#ff4d4f'
        return <Text style={{ color, fontWeight: 500 }}>{percent}%</Text>
      },
      sorter: (a, b) => a.confidence - b.confidence,
    },
  ]

  return (
    <Card
      title="评论列表"
      className="review-list-card"
      extra={
        <Select
          placeholder="筛选情感"
          allowClear
          style={{ width: 120 }}
          value={sentiment}
          onChange={setSentiment}
        >
          <Option value="positive">正面</Option>
          <Option value="negative">负面</Option>
        </Select>
      }
    >
      <Table
        columns={columns}
        dataSource={data}
        loading={loading}
        rowKey="id"
        pagination={false}
        scroll={{ x: 'max-content' }}
      />
      <div className="review-pagination">
        <Pagination
          current={page}
          pageSize={pageSize}
          total={total}
          showSizeChanger
          showQuickJumper
          showTotal={(total) => `共 ${total} 条评论`}
          onChange={(newPage, newPageSize) => {
            setPage(newPage)
            setPageSize(newPageSize)
          }}
          pageSizeOptions={['10', '20', '50', '100']}
        />
      </div>
    </Card>
  )
}

export default ReviewList

