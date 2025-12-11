import React, { useEffect, useRef } from 'react'
import * as echarts from 'echarts'
import { Card, Empty } from 'antd'
import './HeatmapChart.css'

function HeatmapChart({ confusionMatrix }) {
  const chartRef = useRef(null)
  const chartInstance = useRef(null)

  useEffect(() => {
    if (!chartRef.current) return

    // 初始化图表
    if (!chartInstance.current) {
      chartInstance.current = echarts.init(chartRef.current)
    }

    if (confusionMatrix && confusionMatrix.length > 0) {
      const data = []
      const maxValue = Math.max(...confusionMatrix.flat())

      confusionMatrix.forEach((row, i) => {
        row.forEach((value, j) => {
          data.push([j, i, value])
        })
      })

      const option = {
        tooltip: {
          position: 'top',
          formatter: function (params) {
            const labels = ['实际负面', '实际正面']
            const predictions = ['预测负面', '预测正面']
            return `${predictions[params.data[0]]}<br/>${labels[params.data[1]]}<br/>数量: ${params.data[2]}`
          },
        },
        grid: {
          height: '50%',
          top: '10%',
        },
        xAxis: {
          type: 'category',
          data: ['预测负面', '预测正面'],
          splitArea: {
            show: true,
          },
        },
        yAxis: {
          type: 'category',
          data: ['实际负面', '实际正面'],
          splitArea: {
            show: true,
          },
        },
        visualMap: {
          min: 0,
          max: maxValue,
          calculable: true,
          orient: 'horizontal',
          left: 'center',
          bottom: '5%',
          inRange: {
            color: ['#ff4d4f', '#ff7875', '#ffccc7', '#fff1f0'],
          },
        },
        series: [
          {
            name: '混淆矩阵',
            type: 'heatmap',
            data: data,
            label: {
              show: true,
              formatter: '{c}',
            },
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowColor: 'rgba(0, 0, 0, 0.5)',
              },
            },
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
  }, [confusionMatrix])

  if (!confusionMatrix || confusionMatrix.length === 0) {
    return (
      <Card title="混淆矩阵热力图" className="heatmap-card">
        <Empty description="暂无数据" />
      </Card>
    )
  }

  return (
    <Card title="混淆矩阵热力图" className="heatmap-card">
      <div ref={chartRef} className="heatmap-chart" />
    </Card>
  )
}

export default HeatmapChart

