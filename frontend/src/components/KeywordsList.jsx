import React from 'react'
import { Card, Tag, Empty } from 'antd'
import './KeywordsList.css'

function KeywordsList({ keywords }) {
  if (!keywords || keywords.length === 0) {
    return (
      <Card title="关键词提取" className="keywords-card">
        <Empty description="暂无数据" />
      </Card>
    )
  }

  // 根据频率设置标签颜色
  const getTagColor = (freq, maxFreq) => {
    const ratio = freq / maxFreq
    if (ratio > 0.7) return 'red'
    if (ratio > 0.4) return 'orange'
    return 'blue'
  }

  const maxFreq = Math.max(...keywords.map(k => k.freq))

  return (
    <Card title="关键词提取（Top 20）" className="keywords-card">
      <div className="keywords-container">
        {keywords.map((item, index) => (
          <Tag
            key={index}
            color={getTagColor(item.freq, maxFreq)}
            className="keyword-tag"
          >
            {item.word} ({item.freq})
          </Tag>
        ))}
      </div>
    </Card>
  )
}

export default KeywordsList

