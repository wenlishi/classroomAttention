<template>
  <div class="layout-page-container">
    <!-- 1. 复用您已创建的侧边栏组件 -->
    <Sidebar />

    <!-- 2. 这是教室布局页面的主内容区域 -->
    <main class="main-content">
      <header class="page-header">
        <h2>教室布局管理</h2>
        <p>在这里创建、标注并管理所有教室的座位布局。</p>
      </header>
      
      <!-- 3. 主功能区，使用 grid 布局 -->
      <div class="workspace-grid">
        
        <!-- 左侧：布局定义与编辑 -->
        <div class="panel define-panel">
          <div class="panel-header">
            <h3>第一步：定义布局</h3>
            <p>创建或加载一个布局，并定义座位网格。</p>
          </div>
          <div class="panel-content">
            <div class="controls">
              <button @click="createNewLayout" class="btn btn-primary">创建新布局</button>
              <div class="control-group">
                <label for="load-layout-select">或加载已有布局:</label>
                <select v-model="selectedLayoutId" @change="handleLoadLayout" id="load-layout-select">
                  <option disabled value="">-- 请选择 --</option>
                  <option v-for="layout in layouts" :key="layout.id" :value="layout.id">
                    {{ layout.name }}
                  </option>
                </select>
              </div>
            </div>
            <div id="layout-editor-container" v-if="currentLayout.grid.length > 0">
              <div id="layout-info">{{ currentLayout.name }} ({{ currentLayout.grid[0].length }}列 x {{ currentLayout.grid.length }}排)</div>
              <!-- [核心修改] 移除了多余的 .grid-row 容器，使用 template 来循环 -->
              <div id="layout-editor" :style="{ gridTemplateColumns: `repeat(${currentLayout.grid[0].length}, 40px)` }">
                <template v-for="(row, r) in currentLayout.grid" :key="r">
                  <div 
                    v-for="(cell, c) in row" 
                    :key="`cell-${r}-${c}`" 
                    class="layout-cell"
                    :class="{ 'desk': cell === 1, 'aisle': cell === 0 }"
                    @click="toggleDesk(r, c)"
                  >
                    <span v-if="cell === 1">🪑</span>
                    <span v-else>·</span>
                  </div>
                </template>
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧：背景图与标注 -->
        <div class="panel annotate-panel">
           <div class="panel-header">
            <h3>第二步：标注座位</h3>
            <p>上传背景图并在图上标注每个座位的精确位置。</p>
          </div>
          <div class="panel-content">
            <div class="controls">
              <label for="frame-uploader" class="btn btn-secondary">上传背景图</label>
              <input type="file" id="frame-uploader" @change="handleFileChange" accept="image/jpeg, image/png" class="hidden-input">
              <button @click="startAnnotation" class="btn btn-warning" :disabled="!imageFile || currentLayout.grid.length === 0">开始/重新标注</button>
              <button @click="undoAnnotation" class="btn btn-danger" :disabled="annotationHistory.length === 0">撤销上一步</button>
            </div>
            <div id="annotation-status">{{ annotationStatus }}</div>
            <div id="image-container" ref="imageContainerRef">
              <img :src="imagePreviewUrl" id="frame-image" ref="frameImageRef" v-if="imagePreviewUrl" @load="onImageLoad"/>
              <canvas id="annotation-canvas" ref="canvasRef" @click="handleCanvasClick"></canvas>
              <div v-if="!imagePreviewUrl" class="upload-placeholder">
                <p>请上传一张课堂背景图</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 底部：保存操作 -->
        <div class="panel save-panel">
          <div class="panel-header">
            <h3>第三步：保存</h3>
            <p>完成所有步骤后，将完整布局保存到服务器。</p>
          </div>
          <button @click="saveLayout" class="btn btn-success btn-large" :disabled="!isSaveable">
            {{ isSaving ? '正在保存...' : '保存完整布局' }}
          </button>
        </div>

      </div>
    </main>

    <!-- 对话框：输入名称 -->
    <div v-if="isPromptVisible" class="prompt-overlay">
      <div class="prompt-modal">
        <h3>请输入新布局的名称</h3>
        <input v-model="promptValue" @keyup.enter="confirmPrompt" type="text" placeholder="例如：高三(1)班">
        <div class="prompt-buttons">
          <button @click="cancelPrompt" class="btn-secondary">取消</button>
          <button @click="confirmPrompt" class="btn-primary">确定</button>
        </div>
      </div>
    </div>
    
    <!-- [新增] 对话框：选择网格尺寸 -->
    <div v-if="isGridSelectorVisible" class="prompt-overlay">
      <div class="prompt-modal">
        <h3>选择网格尺寸</h3>
        <div class="grid-inputs">
          <div class="input-group">
            <label for="grid-rows">排 (行):</label>
            <input v-model.number="gridSize.rows" id="grid-rows" type="number" min="1" max="20">
          </div>
          <div class="input-group">
            <label for="grid-cols">列:</label>
            <input v-model.number="gridSize.cols" id="grid-cols" type="number" min="1" max="20">
          </div>
        </div>
        <div class="prompt-buttons">
          <button @click="cancelGridSelection" class="btn-secondary">取消</button>
          <button @click="confirmGridSelection" class="btn-primary">确定</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import Sidebar from '../components/Sidebar.vue'; 
import { useToast } from '../composables/useToast';

const { showToast } = useToast();
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';
const VITE_BASE_URL = import.meta.env.VITE_BASE_URL || '';
console.log(VITE_BASE_URL)

// --- 响应式状态 ---
const layouts = ref([]);
const selectedLayoutId = ref('');
const currentLayout = reactive({ id: null, name: '', grid: [], annotations: {} });
const imageFile = ref(null);
const imagePreviewUrl = ref('');
const annotationQueue = ref([]);
const annotationHistory = ref([]);
const annotationStatus = ref('请先创建或加载布局，并上传背景图。');
const isSaving = ref(false);

// --- 模板引用 ---
const imageContainerRef = ref(null);
const frameImageRef = ref(null);
const canvasRef = ref(null);

// --- 对话框状态 ---
const isPromptVisible = ref(false);
const promptValue = ref('');
let promptResolve = null;

// [新增] 网格选择器状态
const isGridSelectorVisible = ref(false);
const gridSize = reactive({ rows: 5, cols: 10 });
let gridSelectorResolve = null;

// --- 计算属性 ---
const isSaveable = computed(() => {
  const totalDesks = currentLayout.grid.flat().filter(cell => cell === 1).length;
  return currentLayout.name && totalDesks > 0 && imageFile.value && annotationQueue.value.length === 0 && Object.keys(currentLayout.annotations).length === totalDesks;
});

// --- 方法 ---

// 重置所有状态
function resetState() {
  selectedLayoutId.value = '';
  currentLayout.id = null;
  currentLayout.name = '';
  currentLayout.grid = [];
  currentLayout.annotations = {};
  imageFile.value = null;
  imagePreviewUrl.value = '';
  annotationQueue.value = [];
  annotationHistory.value = [];
  annotationStatus.value = '请先创建或加载布局，并上传背景图。';
}

// 获取布局列表
async function fetchLayouts() {
  try {
    const response = await fetch(`${API_BASE_URL}/layouts/me`, { credentials: 'include' });
    if (!response.ok) throw new Error('获取布局列表失败');
    layouts.value = await response.json();
  } catch (error) {
    showToast(error.message, 'error');
  }
}

// [核心修改] 创建新布局流程
async function createNewLayout() {
  const name = await showPrompt("请为新布局命名");
  if (name) {
    const dimensions = await showGridSelector();
    if (dimensions) {
      resetState();
      currentLayout.name = name;
      currentLayout.grid = Array.from({ length: dimensions.rows }, () => Array(dimensions.cols).fill(1));
    }
  }
}

// 处理加载布局
async function handleLoadLayout() {
  if (!selectedLayoutId.value) return;
  try {
    const response = await fetch(`${API_BASE_URL}/layouts/${selectedLayoutId.value}`, { credentials: 'include' });
    if (!response.ok) throw new Error('加载布局详情失败');
    const data = await response.json();
    
    resetState();
    selectedLayoutId.value = data.id;
    currentLayout.id = data.id;
    currentLayout.name = data.name;

    const newAnnotations = {};
    const rows = Math.max(...data.desks.map(d => d.row_num)) + 1;
    const cols = Math.max(...data.desks.map(d => d.col_num)) + 1;
    const newGrid = Array.from({ length: rows }, () => Array(cols).fill(0));

    data.desks.forEach(desk => {
      newGrid[desk.row_num][desk.col_num] = 1;
      newAnnotations[`r${desk.row_num}c${desk.col_num}`] = { x: desk.pos_x, y: desk.pos_y };
    });
    
    currentLayout.grid = newGrid;
    currentLayout.annotations = newAnnotations;
    
    imagePreviewUrl.value = `${VITE_BASE_URL}${data.background_image_url}`;
    imageFile.value = new File([], "background.jpg"); 

  } catch (error) {
    showToast(error.message, 'error');
  }
}

// 切换座位/过道
function toggleDesk(r, c) {
  currentLayout.grid[r][c] = currentLayout.grid[r][c] === 1 ? 0 : 1;
  delete currentLayout.annotations[`r${r}c${c}`];
}

// 处理文件上传
function handleFileChange(event) {
  const file = event.target.files[0];
  if (file) {
    imageFile.value = file;
    imagePreviewUrl.value = URL.createObjectURL(file);
  }
}

// 图片加载完成后的回调
function onImageLoad() {
  redrawAllAnnotations();
}

// 开始标注
function startAnnotation() {
  currentLayout.annotations = {};
  annotationHistory.value = [];
  const desks = [];
  currentLayout.grid.forEach((row, r) => {
    row.forEach((cell, c) => {
      if (cell === 1) {
        desks.push({ r, c });
      }
    });
  });
  annotationQueue.value = desks;
  promptNextAnnotation();
}

// 提示下一个要标注的座位
function promptNextAnnotation() {
  if (annotationQueue.value.length > 0) {
    const next = annotationQueue.value[0];
    annotationStatus.value = `请点击 [第 ${next.r + 1} 排, 第 ${next.c + 1} 列] 座位的位置`;
  } else {
    annotationStatus.value = '所有座位标注完成！可以保存了。';
  }
}

// 处理画布点击
function handleCanvasClick(event) {
  if (annotationQueue.value.length === 0) return;

  const canvas = canvasRef.value;
  const rect = canvas.getBoundingClientRect();
  const scaleX = frameImageRef.value.naturalWidth / rect.width;
  const scaleY = frameImageRef.value.naturalHeight / rect.height;

  const canvasX = event.clientX - rect.left;
  const canvasY = event.clientY - rect.top;
  
  const imageX = Math.round(canvasX * scaleX);
  const imageY = Math.round(canvasY * scaleY);

  const currentSeat = annotationQueue.value.shift();
  const seatId = `r${currentSeat.r}c${currentSeat.c}`;
  currentLayout.annotations[seatId] = { x: imageX, y: imageY };
  annotationHistory.value.push({ ...currentSeat, seatId });
  
  redrawAllAnnotations();
  promptNextAnnotation();
}

// 撤销上一步标注
function undoAnnotation() {
  const lastAnnotation = annotationHistory.value.pop();
  if (lastAnnotation) {
    delete currentLayout.annotations[lastAnnotation.seatId];
    annotationQueue.value.unshift({ r: lastAnnotation.r, c: lastAnnotation.c });
    redrawAllAnnotations();
    promptNextAnnotation();
  }
}

// 重绘所有标注点
function redrawAllAnnotations() {
  const canvas = canvasRef.value;
  const image = frameImageRef.value;
  if (!canvas || !image || !image.complete) return;

  const rect = image.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  canvas.width = rect.width * dpr;
  canvas.height = rect.height * dpr;
  canvas.style.width = `${rect.width}px`;
  canvas.style.height = `${rect.height}px`;
  
  const ctx = canvas.getContext('2d');
  ctx.scale(dpr, dpr);

  const scaleX = rect.width / image.naturalWidth;
  const scaleY = rect.height / image.naturalHeight;

  Object.values(currentLayout.annotations).forEach(coords => {
    const canvasX = coords.x * scaleX;
    const canvasY = coords.y * scaleY;
    ctx.beginPath();
    ctx.arc(canvasX, canvasY, 4, 0, 2 * Math.PI);
    ctx.fillStyle = 'rgba(239, 68, 68, 0.8)';
    ctx.fill();
    ctx.strokeStyle = 'white';
    ctx.lineWidth = 1.5;
    ctx.stroke();
  });
}

// 保存布局
async function saveLayout() {
  isSaving.value = true;
  try {
    const formData = new FormData();
    const desks = Object.entries(currentLayout.annotations).map(([key, value]) => {
      const [_, r, c] = key.match(/r(\d+)c(\d+)/);
      return {
        row_num: parseInt(r),
        col_num: parseInt(c),
        pos_x: value.x,
        pos_y: value.y,
      };
    });

    const layoutPayload = {
      name: currentLayout.name,
      description: `一个 ${currentLayout.grid.length}x${currentLayout.grid[0]?.length || 0} 的布局`,
      desks: desks
    };

    formData.append('layout_data', JSON.stringify(layoutPayload));
    formData.append('file', imageFile.value);

    const url = currentLayout.id 
      ? `${API_BASE_URL}/layouts/${currentLayout.id}`
      : `${API_BASE_URL}/layouts/`;
    const method = currentLayout.id ? 'PUT' : 'POST';

    const response = await fetch(url, {
      method: method,
      body: formData,
      credentials: 'include'
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || '保存失败');
    }
    
    const savedLayout = await response.json();
    showToast(`布局 "${savedLayout.name}" 已成功保存！`);
    await fetchLayouts();
    selectedLayoutId.value = savedLayout.id;

  } catch (error) {
    showToast(error.message, 'error');
  } finally {
    isSaving.value = false;
  }
}

// --- 对话框方法 ---
function showPrompt(title) {
  isPromptVisible.value = true;
  promptValue.value = '';
  return new Promise(resolve => { promptResolve = resolve; });
}
function confirmPrompt() {
  if (promptValue.value.trim()) {
    promptResolve(promptValue.value.trim());
    isPromptVisible.value = false;
  }
}
function cancelPrompt() {
  promptResolve(null);
  isPromptVisible.value = false;
}

// [新增] 网格选择器方法
function showGridSelector() {
  isGridSelectorVisible.value = true;
  gridSize.rows = 5;
  gridSize.cols = 10;
  return new Promise(resolve => { gridSelectorResolve = resolve; });
}
function confirmGridSelection() {
  if (gridSize.rows > 0 && gridSize.cols > 0) {
    gridSelectorResolve({ rows: gridSize.rows, cols: gridSize.cols });
    isGridSelectorVisible.value = false;
  }
}
function cancelGridSelection() {
  gridSelectorResolve(null);
  isGridSelectorVisible.value = false;
}


// --- 生命周期钩子 ---
onMounted(() => {
  fetchLayouts();
  const resizeObserver = new ResizeObserver(() => { redrawAllAnnotations(); });
  if (imageContainerRef.value) { resizeObserver.observe(imageContainerRef.value); }
});

</script>

<style scoped>
/* 主布局 */
.layout-page-container {
  display: flex;
  height: 100vh;
  background-color: #f8f9fa;
}
.main-content {
  flex-grow: 1;
  padding: 2.5rem;
  overflow-y: auto;
}
.page-header {
  margin-bottom: 2rem;
  border-bottom: 1px solid #dee2e6;
  padding-bottom: 1.5rem;
}
.page-header h2 {
  font-size: 1.75rem;
  font-weight: 600;
  color: #343a40;
}
.page-header p {
  color: #6c757d;
  font-size: 1rem;
  margin-top: 0.25rem;
}

/* 工作区网格布局 */
.workspace-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: auto auto;
  gap: 1.5rem;
}
.define-panel { grid-column: 1 / 2; }
.annotate-panel { grid-column: 2 / 3; }
.save-panel {
  grid-column: 1 / -1;
  text-align: center;
}

/* 面板样式 */
.panel {
  background-color: #ffffff;
  padding: 1.5rem;
  border-radius: 0.75rem;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
}
.panel-header {
  margin-bottom: 1.5rem;
}
.panel-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #343a40;
}
.panel-header p {
  color: #6c757d;
  font-size: 0.9rem;
  margin-top: 0.25rem;
}

/* 控件样式 */
.controls {
  display: flex;
  gap: 1rem;
  align-items: flex-end;
  margin-bottom: 1.5rem;
}
.control-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #495057;
}
select, input[type="file"] {
  padding: 0.5rem;
  border-radius: 0.375rem;
  border: 1px solid #ced4da;
}
.hidden-input {
  display: none;
}

/* 布局编辑器 */
#layout-editor-container {
  margin-top: 1rem;
}
#layout-info {
  font-weight: 500;
  color: #495057;
  margin-bottom: 1rem;
}
#layout-editor {
  display: inline-grid;
  gap: 4px;
  padding: 8px;
  border: 1px solid #e9ecef;
  border-radius: 0.5rem;
  background-color: #f8f9fa;
}
.layout-cell {
  width: 40px;
  height: 40px;
  border: 1px solid #dee2e6;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s ease;
}
.layout-cell.desk {
  background-color: #fff3bf;
}
.layout-cell.aisle {
  background-color: #e9ecef;
  color: #adb5bd;
}
.layout-cell:hover {
  border-color: #4c6ef5;
}

/* 标注区域 */
#annotation-status {
  padding: 0.75rem;
  background-color: #fff9db;
  color: #856404;
  border-radius: 0.5rem;
  text-align: center;
  margin-bottom: 1rem;
  min-height: 40px;
}
#image-container {
  position: relative;
  width: 100%;
  aspect-ratio: 4 / 3;
  border: 2px dashed #ced4da;
  border-radius: 0.5rem;
  background-color: #f1f3f5;
  display: flex;
  align-items: center;
  justify-content: center;
}
#frame-image, #annotation-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
}
#annotation-canvas {
  cursor: crosshair;
}
.upload-placeholder {
  color: #6c757d;
}

/* 按钮样式 */
.btn {
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}
.btn-large {
  padding: 0.8rem 2rem;
  font-size: 1.1rem;
}
.btn-primary { background-color: #4c6ef5; color: white; }
.btn-primary:hover:not(:disabled) { background-color: #3b5bdb; }
.btn-secondary { background-color: #f1f3f5; color: #495057; border: 1px solid #dee2e6; }
.btn-secondary:hover:not(:disabled) { background-color: #e9ecef; }
.btn-success { background-color: #28a745; color: white; }
.btn-success:hover:not(:disabled) { background-color: #218838; }
.btn-warning { background-color: #ffc107; color: #212529; }
.btn-warning:hover:not(:disabled) { background-color: #e0a800; }
.btn-danger { background-color: #dc3545; color: white; }
.btn-danger:hover:not(:disabled) { background-color: #c82333; }
.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 对话框样式 */
.prompt-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.prompt-modal {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1);
  width: 90%;
  max-width: 400px;
}
.prompt-modal h3 {
  font-size: 1.25rem;
  margin-bottom: 1rem;
}
.prompt-modal input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ced4da;
  border-radius: 0.375rem;
  margin-bottom: 1rem;
}
.prompt-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}

/* [新增] 网格选择器对话框的特定样式 */
.prompt-modal .grid-inputs {
  display: flex;
  justify-content: space-around;
  align-items: center;
  margin-bottom: 1.5rem;
  gap: 1rem;
}
.prompt-modal .grid-inputs .input-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}
.prompt-modal .grid-inputs label {
  font-size: 0.9rem;
  color: #495057;
}
.prompt-modal .grid-inputs input {
  width: 80px;
  text-align: center;
  padding: 0.5rem;
  border: 1px solid #ced4da;
  border-radius: 0.375rem;
}
</style>
