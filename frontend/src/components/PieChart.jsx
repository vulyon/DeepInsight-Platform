import React, { useEffect, useRef } from 'react'
import * as echarts from 'echarts'
import { Card, Empty } from 'antd'
import './PieChart.css'

function PieChart({ data }) {
  const chartRef = useRef(null)
  const chartInstance = useRef(null)

  useEffect(() => {
    if (!chartRef.current) return

    // 初始化图表
    if (!chartInstance.current) {
      chartInstance.current = echarts.init(chartRef.current)
    }

    if (data && data.length > 0) {
      const option = {
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)',
        },
        legend: {
          orient: 'vertical',
          left: 'left',
          top: 'middle',
        },
        series: [
          {
            name: '情感分布',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: {
              borderRadius: 10,
              borderColor: '#fff',
              borderWidth: 2,
            },
            label: {
              show: true,
              formatter: '{b}\n{d}%',
            },
            emphasis: {
              label: {
                show: true,
                fontSize: 16,
                fontWeight: 'bold',
              },
            },
            labelLine: {
              show: true,
            },
            data: data.map((item) => ({
              value: item.value,
              name: item.name,
              itemStyle: {
                color:
                  item.name === '正面'
                    ? '#52c41a'
                    : item.name === '负面'
                    ? '#ff4d4f'
                    : '#1890ff',
              },
            })),
          },
        ],
      }
      chartInstance.current.setOption(option)
    } else {
      chartInstance.current.setOption({
        title: {
          text: '暂无数据',
          left: 'center',
          top: 'middle',
          textStyle: {
            color: '#999',
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

  if (!data || data.length === 0) {
    return (
      <Card title="情感分布饼图" className="pie-chart-card">
        <Empty description="暂无数据" />
      </Card>
    )
  }

  return (
    <Card title="情感分布饼图" className="pie-chart-card">
      <div ref={chartRef} className="pie-chart" />
    </Card>
  )
}

export default PieChart

