import axios from 'axios'

const API_BASE_URL = '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 增加到60秒，但实际使用快速模式不会超时
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    const message = error.response?.data?.detail || error.message || '请求失败'
    return Promise.reject(new Error(message))
  }
)

/**
 * 上传文件
 * @param {File} file - CSV文件
 * @returns {Promise<{file_id: string, message: string}>}
 */
export const uploadFile = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  return api.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
}

/**
 * 开始分析
 * @param {string} fileId - 文件ID
 * @returns {Promise<{task_id: string, status: string}>}
 */
export const startAnalysis = async (fileId) => {
  return api.post('/analyze', { file_id: fileId })
}

/**
 * 获取分析结果
 * @param {string} taskId - 任务ID
 * @returns {Promise<Object>}
 */
export const getResults = async (taskId) => {
  return api.get(`/results/${taskId}`)
}

/**
 * 获取评论列表
 * @param {string} taskId - 任务ID
 * @param {Object} params - 查询参数
 * @returns {Promise<{total: number, page: number, data: Array}>}
 */
export const getReviews = async (taskId, params = {}) => {
  return api.get(`/results/${taskId}/reviews`, { params })
}

export default api

