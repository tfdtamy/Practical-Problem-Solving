// 所有后端请求统一从这里发出。
// 页面组件不要直接写 fetch 和后端地址，以后打包成桌面端或移动端时只需改这一个文件。

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, options)
  if (!res.ok) {
    throw new Error(`${res.status} ${res.statusText}`)
  }
  return res.json()
}

/** 健康检查：返回 { status: "ok", version } */
export function getHealth() {
  return request('/api/health')
}
