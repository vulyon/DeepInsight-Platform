import React from 'react'
import { Card, Empty } from 'antd'
import './WordCloudChart.css'

function WordCloudChart({ title, imageData, sentiment }) {
  if (!imageData) {
    return (
      <Card title={title} className="wordcloud-card">
        <Empty description="暂无词云数据" />
      </Card>
    )
  }

  return (
    <Card
      title={title}
      className="wordcloud-card"
      style={{
        borderColor: sentiment === 'positive' ? '#52c41a' : '#ff4d4f',
      }}
    >
      <div className="wordcloud-container">
        <img
          src={imageData}
          alt={title}
          className="wordcloud-image"
          onError={(e) => {
            e.target.style.display = 'none'
            e.target.parentElement.innerHTML = '<div style="text-align: center; padding: 40px; color: #999;">图片加载失败</div>'
          }}
        />
      </div>
    </Card>
  )
}

export default WordCloudChart

