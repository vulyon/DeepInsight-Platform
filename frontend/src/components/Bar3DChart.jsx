import React, { useEffect, useRef } from 'react'
import * as echarts from 'echarts'
import { Card, Empty } from 'antd'
import './Bar3DChart.css'

function Bar3DChart({ data }) {
  const chartRef = useRef(null)
  const chartInstance = useRef(null)

  useEffect(() => {
    if (!chartRef.current) return

    // 初始化图表
    if (!chartInstance.current) {
      chartInstance.current = echarts.init(chartRef.current)
    }

    if (data && data.categories && data.categories.length > 0) {
      const option = {
        title: {
          text: '情感置信度分布',
          left: 'center',
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow',
          },
        },
        legend: {
          data: ['正面', '负面'],
          top: 30,
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true,
        },
        xAxis: {
          type: 'category',
          data: data.categories,
          axisLabel: {
            rotate: 45,
          },
        },
        yAxis: {
          type: 'value',
        },
        series: [
          {
            name: '正面',
            type: 'bar',
            stack: 'confidence',
            data: data.positive,
            itemStyle: {
              color: '#52c41a',
            },
            emphasis: {
              focus: 'series',
            },
          },
          {
            name: '负面',
            type: 'bar',
            stack: 'confidence',
            data: data.negative,
            itemStyle: {
              color: '#ff4d4f',
            },
            emphasis: {
              focus: 'series',
            },
          },
        ],
      }
      chartInstance.current.setOption(option)
    } else {
      chartInstance.current.setOption({
        graphic: {
          type: 'text',
          left: 'center',
          top: 'middle',
          style: {
            text: '暂无数据',
            fontSize: 16,
            fill: '#999',
          },
        },
      })
    }

    // 响应式
    const handleResize = () => {
      if (chartInstance.current) {
        chartInstance.current.resize()
      }
    }
    window.addEventListener('resize', handleResize)

    return () => {
      window.removeEventListener('resize', handleResize)
    }
  }, [data])

  if (!data || !data.categories || data.categories.length === 0) {
    return (
      <Card title="情感置信度分布" className="bar-3d-chart-card">
        <Empty description="暂无数据" />
      </Card>
    )
  }

  return (
    <Card title="情感置信度分布" className="bar-3d-chart-card">
      <div ref={chartRef} className="bar-3d-chart" />
    </Card>
  )
}

export default Bar3DChart

