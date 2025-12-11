import React, { useEffect, useRef } from 'react'
import * as echarts from 'echarts'
import { Card, Empty } from 'antd'
import './LineChart.css'

function LineChart({ data }) {
  const chartRef = useRef(null)
  const chartInstance = useRef(null)

  useEffect(() => {
    if (!chartRef.current) return

    // 初始化图表
    if (!chartInstance.current) {
      chartInstance.current = echarts.init(chartRef.current)
    }

    if (data && data.dates && data.dates.length > 0) {
      const option = {
        title: {
          text: '情感趋势分析',
          left: 'center',
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
          },
        },
        legend: {
          data: ['正面', '负面', '总计'],
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
          boundaryGap: false,
          data: data.dates,
        },
        yAxis: {
          type: 'value',
        },
        series: [
          {
            name: '正面',
            type: 'line',
            stack: 'Total',
            smooth: true,
            data: data.positive,
            itemStyle: {
              color: '#52c41a',
            },
            areaStyle: {
              color: {
                type: 'linear',
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [
                  { offset: 0, color: 'rgba(82, 196, 26, 0.3)' },
                  { offset: 1, color: 'rgba(82, 196, 26, 0.1)' },
                ],
              },
            },
          },
          {
            name: '负面',
            type: 'line',
            stack: 'Total',
            smooth: true,
            data: data.negative,
            itemStyle: {
              color: '#ff4d4f',
            },
            areaStyle: {
              color: {
                type: 'linear',
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [
                  { offset: 0, color: 'rgba(255, 77, 79, 0.3)' },
                  { offset: 1, color: 'rgba(255, 77, 79, 0.1)' },
                ],
              },
            },
          },
          {
            name: '总计',
            type: 'line',
            smooth: true,
            data: data.total,
            itemStyle: {
              color: '#1890ff',
            },
            lineStyle: {
              type: 'dashed',
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

  if (!data || !data.dates || data.dates.length === 0) {
    return (
      <Card title="情感趋势分析" className="line-chart-card">
        <Empty description="暂无数据" />
      </Card>
    )
  }

  return (
    <Card title="情感趋势分析" className="line-chart-card">
      <div ref={chartRef} className="line-chart" />
    </Card>
  )
}

export default LineChart

