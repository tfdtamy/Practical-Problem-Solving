<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'
import { PLYLoader } from 'three/examples/jsm/loaders/PLYLoader.js'

const props = defineProps({
  // 点云文件地址，放在 public/ 下的文件用 /xxx.ply 访问
  src: { type: String, required: true },
})

const container = ref(null)
const message = ref('加载点云中…')

let renderer, scene, camera, controls, points, resizeObserver, frameId

onMounted(() => {
  const el = container.value

  scene = new THREE.Scene()
  scene.background = new THREE.Color(0x1e1f22)

  camera = new THREE.PerspectiveCamera(60, el.clientWidth / el.clientHeight, 0.1, 5000)
  // 项目约定模型 z 轴竖直向上（Three.js 默认是 y 朝上）
  camera.up.set(0, 0, 1)

  renderer = new THREE.WebGLRenderer({ antialias: true })
  renderer.setPixelRatio(window.devicePixelRatio)
  renderer.setSize(el.clientWidth, el.clientHeight)
  el.appendChild(renderer.domElement)

  controls = new OrbitControls(camera, renderer.domElement)
  controls.enableDamping = true

  scene.add(new THREE.AxesHelper(2))

  new PLYLoader().load(
    props.src,
    (geometry) => {
      const material = new THREE.PointsMaterial({
        size: 0.08,
        vertexColors: geometry.hasAttribute('color'),
      })
      points = new THREE.Points(geometry, material)
      scene.add(points)
      frameCamera(geometry)
      message.value = ''
    },
    undefined,
    (err) => {
      message.value = `点云加载失败：${props.src}`
      console.error(err)
    },
  )

  resizeObserver = new ResizeObserver(() => {
    camera.aspect = el.clientWidth / el.clientHeight
    camera.updateProjectionMatrix()
    renderer.setSize(el.clientWidth, el.clientHeight)
  })
  resizeObserver.observe(el)

  const animate = () => {
    frameId = requestAnimationFrame(animate)
    controls.update()
    renderer.render(scene, camera)
  }
  animate()
})

// 把相机放到能看到整个点云的位置
function frameCamera(geometry) {
  geometry.computeBoundingSphere()
  const { center, radius } = geometry.boundingSphere
  controls.target.copy(center)
  camera.position.set(center.x + radius * 1.5, center.y - radius * 1.5, center.z + radius * 1.2)
  camera.near = radius / 100
  camera.far = radius * 100
  camera.updateProjectionMatrix()
  controls.update()
}

onUnmounted(() => {
  cancelAnimationFrame(frameId)
  resizeObserver?.disconnect()
  controls?.dispose()
  if (points) {
    points.geometry.dispose()
    points.material.dispose()
  }
  renderer?.dispose()
})
</script>

<template>
  <div ref="container" class="viewer">
    <div v-if="message" class="message">{{ message }}</div>
    <div class="hint">左键旋转 · 右键平移 · 滚轮缩放</div>
  </div>
</template>

<style scoped>
.viewer {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.message {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #bbb;
}

.hint {
  position: absolute;
  left: 16px;
  bottom: 16px;
  font-size: 12px;
  color: #888;
  pointer-events: none;
}
</style>
