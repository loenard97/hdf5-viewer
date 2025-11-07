import pathlib

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QMenu, QPushButton, QStyle, QToolButton, QWidget


class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.main_window = parent
        self.initial_pos = None

        title_bar_layout = QHBoxLayout(self)
        # title_bar_layout.setContentsMargins(1, 1, 1, 1)
        title_bar_layout.setContentsMargins(0, 0, 0, 0)
        title_bar_layout.setSpacing(2)

        btn_file = QPushButton()
        btn_file.setFixedSize(QSize(3 * 35, 35))
        btn_file.setIcon(QIcon(str(pathlib.Path(r"D:\Projects\Python\hdf5-viewer\src\img\hamburger.svg"))))
        btn_file.setIconSize(btn_file.size())
        btn_file.setStyleSheet(
            """
            QPushButton {
                border: 0px solid #dbdfe5;
                background-color: #f5f5f6;
                border-radius: 0px;
                padding: 0px 0px;
            }
            QPushButton:hover {
                background-color: #e7eef4;
            }
            QPushButton:pressed {
                background-color: #e7eef4;
            }
            """
        )

        # menu_file = QMenu()
        # act_file = QAction("&Open File...", self)
        # # act_file.setIcon(QIcon(str(pathlib.Path(self.main_window.icon_dir, "file.svg"))))
        # act_file.setShortcut("Ctrl+O")
        # act_file.triggered.connect(self.main_window._handle_action_open_file)
        # menu_file.addAction(act_file)
        # act_open_folder = QAction("&Open Folder...", self)
        # # act_open_folder.setIcon(QIcon(str(pathlib.Path(self.icon_dir, "group.svg"))))
        # act_open_folder.triggered.connect(self.main_window._handle_action_open_folder)
        # menu_file.addAction(act_open_folder)
        # act_clear_files = QAction("&Close all Files", self)
        # # act_clear_files.setIcon(QIcon(str(pathlib.Path(self.icon_dir, "file_clear.svg"))))
        # act_clear_files.triggered.connect(self.main_window._handle_action_clear_files)
        # menu_file.addAction(act_clear_files)
        # menu_file.addSeparator()
        # act_quit = QAction("&Quit", self)
        # # act_quit.setIcon(QIcon(str(pathlib.Path(self.icon_dir, "quit.svg"))))
        # act_quit.setShortcut("Ctrl+Q")
        # act_quit.triggered.connect(self.main_window._handle_close)
        # menu_file.addAction(act_quit)
        # btn_file.setMenu(menu_file)
        # title_bar_layout.addWidget(btn_file)

        # btn_help = QPushButton("Help")
        # btn_help.setFixedSize(QSize(50, 35))
        # btn_help.setStyleSheet(
        #     """
        #     QPushButton {
        #         border: 0px solid #dbdfe5;
        #         background-color: #f5f5f6;
        #         border-radius: 0px;
        #         padding: 0px 0px;
        #     }
        #     QPushButton:hover {
        #         background-color: #e7eef4;
        #     }
        #     QPushButton:pressed {
        #         background-color: #e7eef4;
        #     }
        #     """
        # )
        # title_bar_layout.addWidget(btn_help)

        self.title = QLabel("HDF5 Viewer", self)
        # self.title.setStyleSheet("font-weight: bold; margin: 2px;")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_bar_layout.addWidget(self.title)

        self.min_button = QToolButton(self)
        # min_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarMinButton)
        self.min_button.setFixedSize(QSize(35, 35))
        min_icon = QIcon(str(pathlib.Path(r"D:\Projects\Python\hdf5-viewer\src\img\minimize.svg")))
        self.min_button.setIcon(min_icon)
        # self.min_button.setIconSize(btn_file.size())
        self.min_button.clicked.connect(self.window().showMinimized)
        self.min_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.min_button.setStyleSheet(
            """QToolButton { border: 2px; }
            QToolButton:hover {
                background-color: #e2e5e9;
            }
            """
        )
        title_bar_layout.addWidget(self.min_button)

        self.max_button = QToolButton(self)
        max_icon = QIcon(str(pathlib.Path(r"D:\Projects\Python\hdf5-viewer\src\img\maximize.svg")))
        self.max_button.setIcon(max_icon)
        self.max_button.clicked.connect(self.window().showMaximized)
        self.max_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.max_button.setFixedSize(QSize(35, 35))
        self.max_button.setStyleSheet(
            """QToolButton { border: 2px; }
            QToolButton:hover {
                background-color: #e2e5e9;
            }
            """
        )
        title_bar_layout.addWidget(self.max_button)

        self.close_button = QToolButton(self)
        close_icon = QIcon(str(pathlib.Path(r"D:\Projects\Python\hdf5-viewer\src\img\close.svg")))
        self.close_button.setIcon(close_icon)
        self.close_button.clicked.connect(self.window().close)
        self.close_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.close_button.setFixedSize(QSize(35, 35))
        self.close_button.setStyleSheet(
            """QToolButton { border: 2px; }
            QToolButton:hover {
                background-color: #DD0000;
            }
            """
        )
        title_bar_layout.addWidget(self.close_button)

        self.normal_button = QToolButton(self)
        normal_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarNormalButton)
        self.normal_button.setIcon(normal_icon)
        self.normal_button.clicked.connect(self.window().showNormal)
        self.normal_button.setVisible(False)
        self.normal_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.normal_button.setFixedSize(QSize(35, 35))
        self.normal_button.setStyleSheet(
            """QToolButton { border: 2px; }
            QToolButton:hover {
                background-color: #e2e5e9;
            }
            """
        )
        title_bar_layout.addWidget(self.normal_button)

    def window_state_changed(self, state):
        if state == Qt.WindowState.WindowMaximized:
            self.normal_button.setVisible(True)
            self.max_button.setVisible(False)
        else:
            self.normal_button.setVisible(False)
            self.max_button.setVisible(True)
