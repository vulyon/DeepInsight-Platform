import React, { useEffect, useRef } from 'react'
import { Card, Empty, Alert, List, Tag } from 'antd'
import './LDAVisualization.css'

function LDAVisualization({ ldaData }) {
  const iframeRef = useRef(null)

  useEffect(() => {
    if (ldaData?.vis_html && iframeRef.current) {
      // 将HTML内容写入iframe
      const iframe = iframeRef.current
      const doc = iframe.contentDocument || iframe.contentWindow.document
      doc.open()
      doc.write(ldaData.vis_html)
      doc.close()
    }
  }, [ldaData])

  if (!ldaData) {
    return (
      <Card title="LDA主题模型分析" className="lda-card">
        <Empty description="暂无数据" />
      </Card>
    )
  }

  if (ldaData.error) {
    return (
      <Card title="LDA主题模型分析" className="lda-card">
        <Alert message="LDA分析失败" description={ldaData.error} type="warning" showIcon />
      </Card>
    )
  }

  return (
    <Card 
      title={`LDA主题模型分析（${ldaData.num_topics || 0}个主题）`} 
      className="lda-card"
    >
      {ldaData.topics && ldaData.topics.length > 0 && (
        <div className="lda-topics">
          <h4>主题列表：</h4>
          <List
            dataSource={ldaData.topics}
            renderItem={(topic) => (
              <List.Item>
                <div>
                  <Tag color="blue">主题 {topic.id + 1}</Tag>
                  <span style={{ marginLeft: 8 }}>
                    {topic.top_words?.join('、') || '无关键词'}
                  </span>
                </div>
              </List.Item>
            )}
          />
        </div>
      )}
      
      {ldaData.vis_html && (
        <div className="lda-visualization">
          <h4>主题可视化：</h4>
          <iframe
            ref={iframeRef}
            title="LDA Visualization"
            className="lda-iframe"
            sandbox="allow-same-origin allow-scripts"
          />
        </div>
      )}
    </Card>
  )
}

export default LDAVisualization

