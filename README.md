# 五子棋游戏 (Gomoku Game)

一个基于Python开发的多功能五子棋游戏，支持本地对战、网络对战和人机对战三种游戏模式。

## 🎮 游戏特性

- **多种游戏模式**
  - 本地双人对战：支持同一设备上的双人游戏
  - 网络对战：支持局域网内多设备联机对战
  - 人机对战：内置AI智能对手，基于Minimax算法和Alpha-Beta剪枝

- **现代化图形界面**
  - 使用OpenGL渲染，提供流畅的游戏体验
  - 支持动态棋盘绘制和棋子动画效果
  - 直观的用户界面和游戏状态显示

- **完整的音效系统**
  - 背景音乐播放
  - 落子音效
  - 胜利音效

- **智能AI系统**
  - 基于Minimax算法的AI对手
  - Alpha-Beta剪枝优化，提升计算效率
  - 多层次评估函数，支持攻防策略

## 🛠️ 技术栈

- **Python 3.x**
- **Pygame** - 游戏引擎和事件处理
- **OpenGL** - 图形渲染
- **NumPy** - 数据处理和棋盘状态管理
- **Socket** - 网络通信
- **Tkinter** - 弹窗提示界面
- **Threading** - 多线程处理

## 📁 项目结构

```
Game_Code/
├── main.py                 # 主程序入口和菜单系统
├── game_core.py           # 游戏核心逻辑（棋盘、规则判定）
├── local_game.py          # 本地双人对战模式
├── network_game.py        # 网络对战模式
├── ai_game.py            # 人机对战模式
├── ai_player.py          # AI玩家实现（Minimax算法）
├── opengl_renderer.py    # OpenGL图形渲染器
├── audio_manager.py      # 音频管理系统
├── tkinter_part.py       # Tkinter弹窗组件
├── audio_resources/      # 音效资源文件夹
│   ├── background.mp3    # 背景音乐
│   ├── piece.mp3        # 落子音效
│   └── win.mp3          # 胜利音效
├── tkinter_renderer/     # Tkinter界面资源
│   ├── 认可.jpg         # 胜利提示图片
│   └── DORO.ico         # 应用图标
├── Dataset/             # AI训练数据集
│   ├── x_train.npz
│   ├── x_test.npz
│   ├── y_train.npz
│   └── y_test.npz
└── old_version/         # 旧版本文件
    ├── desert.py
    ├── model.pth
    ├── model.py
    ├── Tradition.py
    └── train_model.py
```

## 🚀 安装与运行

### 系统要求

- Python 3.7+
- 支持OpenGL的图形卡

### 安装依赖

```bash
pip install pygame PyOpenGL PyOpenGL_accelerate numpy pillow awthemes
```

### 运行游戏

```bash
python main.py
```

## 🎯 游戏说明

### 基本规则

- 15×15棋盘
- 黑棋先手，白棋后手
- 率先形成五子连珠者获胜
- 支持横、竖、斜四个方向的连珠判定

### 操作方式

- **鼠标左键**：落子
- **R键**：重新开始游戏
- **ESC键**：退出当前模式/游戏

### 游戏模式详解

#### 1. 本地双人对战
- 同一设备上的双人游戏
- 轮流操作，实时显示当前玩家
- 支持游戏重置功能

#### 2. 网络对战
- 基于TCP Socket的局域网联机
- 支持创建房间和加入房间
- 实时同步游戏状态
- 默认端口：5555

**网络对战使用方法：**
1. 一方选择"创建房间"作为服务器
2. 另一方选择"加入房间"作为客户端
3. 确保双方在同一局域网内
4. 服务器端先手（黑棋）

#### 3. 人机对战
- AI使用Minimax算法和Alpha-Beta剪枝
- 支持多层深度搜索（默认3层）
- 智能评估函数，具备攻防能力
- 人类玩家先手（黑棋），AI后手（白棋）

## 🤖 AI算法说明

### Minimax算法
- 经典的博弈树搜索算法
- 通过递归搜索评估每个可能的走法
- 假设对手总是选择最优策略

### Alpha-Beta剪枝
- 优化Minimax算法的搜索效率
- 剪除不必要的分支，减少计算量
- 大幅提升AI响应速度

### 评估函数
- 基于棋型模式的评分系统
- 区分攻击和防守模式
- 支持多种连珠模式识别

## 🎵 音效系统

游戏内置完整的音效系统：
- **背景音乐**：游戏全程播放
- **落子音效**：每次落子时播放
- **胜利音效**：游戏结束时播放

## 🔧 自定义配置

### AI难度调整
在 `ai_player.py` 中可以调整以下参数：
```python
self.max_depth = 3        # 搜索深度（1-5推荐）
self.expand_radius = 1    # 落子扩展半径
```

### 网络设置
在 `network_game.py` 中可以修改：
```python
host = "127.0.0.1"        # 服务器IP地址
port = 5555               # 通信端口
```

## 🐛 故障排除

### 常见问题

1. **OpenGL初始化失败**
   - 确保显卡驱动程序最新
   - 检查是否支持OpenGL 2.0+

2. **音效无法播放**
   - 检查音频文件是否存在于 `audio_resources/` 目录
   - 确认系统音频设备正常工作

3. **网络连接失败**
   - 检查防火墙设置
   - 确保端口5555未被占用
   - 验证双方IP地址可达

4. **AI响应缓慢**
   - 降低AI搜索深度
   - 检查系统CPU使用率


## 📄 许可证

本项目仅用于学习和教育目的。

## 🔮 未来功能

- [ ] 支持更多AI难度等级
- [ ] 添加棋谱保存和回放功能
- [ ] 实现在线排行榜系统
- [ ] 支持自定义棋盘大小
- [ ] 添加更多游戏模式（如禁手规则）
- [ ] 添加深度学习模型

## 其他说明

1. dataset中是尝试使用深度学习模型的数据集，但是因为训练效果一般没有使用
2. 这个项目只是个simple_demo，可以很多功能都未有良好的实现，但是本人因为某些原因，对这个项目的维护很少，所以这个项目的改进估计会暂时搁置，更新时间未知

**最后——祝你享受游戏！** 🎮
