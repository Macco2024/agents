"""
主窗口模块

应用程序的主窗口界面。
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QMenuBar, QStatusBar, QToolBar, QSplitter,
    QTextEdit, QLabel, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction, QIcon

from config.settings import AppConfig
from utils.logger import get_logger


class MainWindow(QMainWindow):
    """主窗口类"""
    
    # 信号定义
    content_generated = pyqtSignal(str)
    image_generated = pyqtSignal(str)
    voice_generated = pyqtSignal(str)
    
    def __init__(self):
        """初始化主窗口"""
        super().__init__()
        self.logger = get_logger(__name__)
        self.config = AppConfig()
        
        self.init_ui()
        self.setup_connections()
        
        self.logger.info("主窗口初始化完成")
    
    def init_ui(self):
        """初始化用户界面"""
        # 设置窗口属性
        self.setWindowTitle(self.config.APP_NAME)
        self.setGeometry(100, 100, self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT)
        self.setMinimumSize(self.config.WINDOW_MIN_WIDTH, self.config.WINDOW_MIN_HEIGHT)
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建工具栏
        self.create_tool_bar()
        
        # 创建状态栏
        self.create_status_bar()
        
        # 创建中央部件
        self.create_central_widget()
        
        # 应用样式
        self.apply_styles()
    
    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu('文件(&F)')
        
        new_action = QAction('新建(&N)', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.new_document)
        file_menu.addAction(new_action)
        
        open_action = QAction('打开(&O)', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_document)
        file_menu.addAction(open_action)
        
        save_action = QAction('保存(&S)', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_document)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('退出(&X)', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 编辑菜单
        edit_menu = menubar.addMenu('编辑(&E)')
        
        # 工具菜单
        tools_menu = menubar.addMenu('工具(&T)')
        
        # 帮助菜单
        help_menu = menubar.addMenu('帮助(&H)')
        
        about_action = QAction('关于(&A)', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_tool_bar(self):
        """创建工具栏"""
        toolbar = self.addToolBar('主工具栏')
        
        # 新建按钮
        new_btn = QPushButton('新建')
        new_btn.clicked.connect(self.new_document)
        toolbar.addWidget(new_btn)
        
        # 生成内容按钮
        generate_btn = QPushButton('生成内容')
        generate_btn.clicked.connect(self.generate_content)
        toolbar.addWidget(generate_btn)
        
        # 生成配图按钮
        image_btn = QPushButton('生成配图')
        image_btn.clicked.connect(self.generate_image)
        toolbar.addWidget(image_btn)
        
        # 生成语音按钮
        voice_btn = QPushButton('生成语音')
        voice_btn.clicked.connect(self.generate_voice)
        toolbar.addWidget(voice_btn)
    
    def create_status_bar(self):
        """创建状态栏"""
        self.status_bar = self.statusBar()
        self.status_bar.showMessage('就绪')
        
        # 添加状态标签
        self.status_label = QLabel('状态：就绪')
        self.status_bar.addPermanentWidget(self.status_label)
    
    def create_central_widget(self):
        """创建中央部件"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QHBoxLayout(central_widget)
        
        # 创建分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # 左侧面板（编辑区域）
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # 右侧面板（预览区域）
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # 设置分割器比例
        splitter.setSizes([600, 600])
    
    def create_left_panel(self):
        """创建左侧面板"""
        left_widget = QWidget()
        layout = QVBoxLayout(left_widget)
        
        # 标题
        title_label = QLabel('内容编辑')
        title_label.setStyleSheet("font-size: 14px; font-weight: bold; margin: 5px;")
        layout.addWidget(title_label)
        
        # 文本编辑器
        self.text_editor = QTextEdit()
        self.text_editor.setPlaceholderText('在此输入或生成文章内容...')
        layout.addWidget(self.text_editor)
        
        return left_widget
    
    def create_right_panel(self):
        """创建右侧面板"""
        right_widget = QWidget()
        layout = QVBoxLayout(right_widget)
        
        # 标题
        title_label = QLabel('预览区域')
        title_label.setStyleSheet("font-size: 14px; font-weight: bold; margin: 5px;")
        layout.addWidget(title_label)
        
        # 预览区域
        self.preview_area = QTextEdit()
        self.preview_area.setReadOnly(True)
        self.preview_area.setPlaceholderText('内容预览将在此显示...')
        layout.addWidget(self.preview_area)
        
        return right_widget
    
    def apply_styles(self):
        """应用样式"""
        # 这里可以加载QSS样式表
        pass
    
    def setup_connections(self):
        """设置信号连接"""
        self.content_generated.connect(self.on_content_generated)
        self.image_generated.connect(self.on_image_generated)
        self.voice_generated.connect(self.on_voice_generated)
    
    # 槽函数
    def new_document(self):
        """新建文档"""
        self.text_editor.clear()
        self.preview_area.clear()
        self.status_bar.showMessage('新建文档')
        self.logger.info("创建新文档")
    
    def open_document(self):
        """打开文档"""
        # TODO: 实现文档打开功能
        self.status_bar.showMessage('打开文档')
        self.logger.info("打开文档")
    
    def save_document(self):
        """保存文档"""
        # TODO: 实现文档保存功能
        self.status_bar.showMessage('保存文档')
        self.logger.info("保存文档")
    
    def generate_content(self):
        """生成内容"""
        # TODO: 实现内容生成功能
        self.status_bar.showMessage('正在生成内容...')
        self.logger.info("开始生成内容")
    
    def generate_image(self):
        """生成配图"""
        # TODO: 实现图片生成功能
        self.status_bar.showMessage('正在生成配图...')
        self.logger.info("开始生成配图")
    
    def generate_voice(self):
        """生成语音"""
        # TODO: 实现语音生成功能
        self.status_bar.showMessage('正在生成语音...')
        self.logger.info("开始生成语音")
    
    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(
            self,
            '关于',
            f'{self.config.APP_NAME} v{self.config.APP_VERSION}\n\n'
            f'作者：{self.config.APP_AUTHOR}\n\n'
            '一个现代化的微信公众号内容生成系统。'
        )
    
    def on_content_generated(self, content):
        """内容生成完成"""
        self.text_editor.setPlainText(content)
        self.status_bar.showMessage('内容生成完成')
    
    def on_image_generated(self, image_path):
        """图片生成完成"""
        self.status_bar.showMessage(f'配图生成完成：{image_path}')
    
    def on_voice_generated(self, voice_path):
        """语音生成完成"""
        self.status_bar.showMessage(f'语音生成完成：{voice_path}')
    
    def cleanup(self):
        """清理资源"""
        self.logger.info("清理主窗口资源")
        # TODO: 清理资源
