import re
import shutil
import sys
import time
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtGui import QFontDatabase, QPixmap
from PySide6.QtCore import Qt, QTimer, QPoint
import os
import subprocess
import git
from pypdl import Pypdl
import requests
import ctypes
import threading

import ui_launcher

# Constants
GAME_DOWNLOAD_URL = "https://huggingface.co/CloudTron/Beyond-2089329/resolve/main/Beyond_Release-2089329-32_os_prod_cbt.7z"
GAME_INSTALL_PATH = "./EndfieldGame"
GAME_DOWNLOAD_CACHE = os.path.join(GAME_INSTALL_PATH, "cache")
GAME_DOWNLOAD_PATH = os.path.join(GAME_DOWNLOAD_CACHE, "EndfieldGame.7z")
GAME_EXECUTABLE_PATH = os.path.join(GAME_INSTALL_PATH, "Beyond_Release-2089329-32_os_prod_cbt", "Endfield_TBeta_OS.exe")

SERVER_REPO = "https://github.com/SuikoAkari/ArkFieldPS.git"
SERVER_INSTALL_PATH= "./EndfieldServer"
SERVER_REPO_PATH = os.path.join(SERVER_INSTALL_PATH, "ArkfieldPS")
SERVER_SOLUTION_FILE = os.path.join(SERVER_REPO_PATH, "ArkfieldPS.sln")
SERVER_ARTIFACT_PATH = os.path.join(SERVER_REPO_PATH, "ArkfieldPS", "bin", "Release", "net8.0")
SERVER_EXECUTABLE_PATH = os.path.join(SERVER_ARTIFACT_PATH, "ArkfieldPS.exe")

SERVER_DATA_REPO = "https://github.com/PotRooms/EndFieldData.git"
SERVER_DATA_REPO_PATH = os.path.join(SERVER_INSTALL_PATH, "EndFieldData")
SERVER_DATA_INSTALL_PATH = [
    (os.path.join(SERVER_DATA_REPO_PATH, "DynamicAssets"), os.path.join(SERVER_ARTIFACT_PATH, "DynamicAssets")),
    (os.path.join(SERVER_DATA_REPO_PATH, "Json"), os.path.join(SERVER_ARTIFACT_PATH, "Json")),
    (os.path.join(SERVER_DATA_REPO_PATH, "TableCfg"), os.path.join(SERVER_ARTIFACT_PATH, "TableCfg"))
]

# Popup: mode = 0 (information), mode = 1 (confirmation)
def show_popup(title, message, mode=0):
    msg_box = QMessageBox()
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    
    if mode == 1:
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = msg_box.exec()
        return result == QMessageBox.Yes
    else:
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()
        return None

def extract7z(archive_path, output_dir, progress_tracker):
    cmd = [
        "7za.exe", "x", archive_path, f"-o{output_dir}",
        "-bsp1", "-y"
    ]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    progress_re = re.compile(r"^\s*(\d+)%")
    while True:
        if progress_tracker.isCancelled:
            process.terminate()
            break
        line = process.stdout.readline()
        if not line:
            break
        line = line.strip()
        match = progress_re.match(line)
        if match:
            progress = int(match.group(1))
            progress_tracker.update(progress)
    process.stdout.close()
    return_code = process.wait()
    if return_code != 0:
        raise Exception(f"7za.exe exited with code {return_code}")

def empty_folder(folder_path):
    if not os.path.exists(folder_path):
        return
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)  # remove the file or link
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)  # remove directory and all its contents
        except Exception as e:
            pass

# Game Launcher
class GameLauncherBackend:
    def __init__(self):
        self.progress = 0
        self.statusText = ""
        self.dl = None
        self.extractTracker = None
        self.status = 0 # 0: idle, 1: downloading, 2: extracting, 3: launching, 4: failed

    def initiateInstallation(self):
        # download game #
        self.progress = 0
        self.status = 1

        # get url
        self.statusText = "Contacting Endfield Distribution Server..."
        real_url = self.get_real_url(GAME_DOWNLOAD_URL)
        if real_url is None:
            self.statusText = "Failed to obtain download URL."
            self.status = 4
            return False
        
        # ensure cache directory exists
        if not os.path.exists(GAME_DOWNLOAD_CACHE):
            os.makedirs(GAME_DOWNLOAD_CACHE)

        # download
        self.statusText = "Downloading critical data..."
        self.dl = Pypdl()
        self.dl.start(
            url=real_url,
            file_path=GAME_DOWNLOAD_PATH,
            multisegment=True,
            segments=8,
            overwrite=True,
            retries=3,
            display=True,
            clear_terminal=False,
            block=False,
        )

    def initiateExtracting(self):
        # extract game client #
        self.progress = 0
        self.status = 2
        self.statusText = "Extracting critical data..."

        class ExtractProgressTracker():
            def __init__(self):
                self.statusText = "Extracting critical data... 0%"
                self.progressValue = 0
                self.isCancelled = False
            def update(self, newProgress):
                self.progressValue = newProgress
                self.statusText = f"Extracting critical data... {newProgress}%"

        self.extractTracker = ExtractProgressTracker()
        try:
            extract7z(GAME_DOWNLOAD_PATH, GAME_INSTALL_PATH, self.extractTracker)
        except Exception as e:
            self.statusText = f"Extraction failed: {e}"
            self.status = 4
            return False

        # clean up cache
        empty_folder(GAME_DOWNLOAD_CACHE)

        self.status = 0
        return True
    
    def fetchInstallationProgress(self):
        if self.dl is None:
            return 0

        def format_size(size):
            if type(size) is not int:
                return "0 B"
            if size < 1024 * 1024:
                return f"{size/1024:.2f} KB"
            elif size < 1024 * 1024 * 1024:
                return f"{size/1024/1024:.2f} MB"
            else:
                return f"{size/1024/1024/1024:.2f} GB"

        if self.dl.failed:
            self.statusText = "Download failed."
            self.status = 2
            return -1

        if not self.dl.is_idle:
            if self.dl.progress is None:
                self.progress = 0
            else:
                self.progress = round(self.dl.progress, 1)
            # eta is in seconds, convert to hh:mm:ss
            eta_formatted_string = time.strftime("%H:%M:%S", time.gmtime(self.dl.eta))
            self.statusText = f"Downloading critical data... {format_size(self.dl.current_size)}/{format_size(self.dl.size)} {self.progress}% | {self.dl.speed:.2f} MB/s | ETA: {eta_formatted_string}"
            return 0
        
        if self.dl.completed:
            self.statusText = "Download completed."
            self.status = 0
            return 1
    
    def cancelInstallation(self):
        if self.dl is not None:
            self.dl.stop()
        if self.extractTracker is not None:
            self.extractTracker.isCancelled = True
        # clean up cache
        empty_folder(GAME_DOWNLOAD_CACHE)

    def launchGame(self):
        # call game executable 
        self.progress = 0
        self.statusText = "Launching game..."
        self.status = 3
        try:
            ret = ctypes.windll.shell32.ShellExecuteW(None, "runas", GAME_EXECUTABLE_PATH, "", None, 1)
            if ret <= 32:
                self.statusText = f"Failed to launch game: Error code {ret}"
                self.status = 4
                return False
            return True
        except Exception as e:
            self.statusText = f"Failed to launch game: {e}"
            self.status = 4
            return False

    def getStatus(self):
        # check if game is installed
        return os.path.exists(GAME_EXECUTABLE_PATH)
    
    def get_real_url(self, initial_url):
        session = requests.Session()
        try:
            response = session.head(initial_url, allow_redirects=True, timeout=10)
            if response.status_code >= 400:
                response = session.get(initial_url, allow_redirects=True, stream=True, timeout=10)
        except Exception as e:
            return None
        finally:
            session.close()
        return response.url

# Server Launcher
class ServerLauncherBackend:
    def __init__(self):
        self.progress = 0
        self.statusText = ""
        self.fetchProgress = None
        self.buildProgress = None
        self.status = 0 # 0: idle, 1: downloading, 2: building, 3: launching, 4: failed

    def initiateDownload(self):
        # clone server repo
        self.status = 1
        self.progress = 1
        self.statusText = "Downloading Endfield Network deployment dependencies..."
        self.clone_repo(SERVER_REPO, SERVER_REPO_PATH)
        self.clone_repo(SERVER_DATA_REPO, SERVER_DATA_REPO_PATH)

    def initiateBuild(self):
        # compile server
        self.progress = 0
        self.status = 2
        
        class BuildProgressTracker():
            def __init__(self):
                self.statusText = "Compiling Endfield Network Server..."
                self.progressValue = 0
                self.isCancelled = False
            
        self.buildProgress = BuildProgressTracker()

        # find msbuild
        try:
            msbuild_path = self.find_msbuild()
        except Exception as e:
            self.buildProgress.statusText = f"Failed to locate build tools!"
            show_popup("Error", f"Failed to locate build tools: {e}")
            self.status = 4
            return False
        self.buildProgress.progressValue = 10

        # compile project

        # clean up old build
        empty_folder(SERVER_ARTIFACT_PATH)
        try:
            ret = self.compile_project(msbuild_path, SERVER_SOLUTION_FILE, progress_tracker=self.buildProgress)
            if not ret:
                self.status = 4
                return False
        except Exception as e:
            self.buildProgress.statusText = f"Compilation failed: {e}"
            self.status = 4
            return False
        self.buildProgress.progressValue = 50

        # clone assets
        for (i, dataInstall) in enumerate(SERVER_DATA_INSTALL_PATH):
            self.buildProgress.statusText = f"Copying Endfield critical data... {i+1}/{len(SERVER_DATA_INSTALL_PATH)}"
            empty_folder(dataInstall[1])
            shutil.copytree(dataInstall[0], dataInstall[1])
            self.buildProgress.progressValue = 50 + int( (i+1) / len(SERVER_DATA_INSTALL_PATH) * 50 )

        self.buildProgress.statusText = "Deployment completed."
        return True
        
    def launchServer(self):
        # call server executable
        self.progress = 0
        self.statusText = "Launching server..."
        self.status = 3
        try:
            CREATE_NEW_CONSOLE = 0x00000010
            creationflags = CREATE_NEW_CONSOLE
            subprocess.Popen(SERVER_EXECUTABLE_PATH, cwd=SERVER_ARTIFACT_PATH, creationflags=creationflags)
            return True
        except Exception as e:
            self.statusText = f"Failed to launch Endfield Network Server!"
            self.status = 4
            show_popup("Error", f"Failed to launch Endfield Network Server: {e}")
            return False
        
    def cancelInstallation(self):
        show_popup("Notice", "I'm too lazy to implement force-kill for msbuild and git\
                    Please manually kill the processes by closing this launcher. You\
                    might have to kill the processes manually in Task Manager in some cases.")

    def getStatus(self):
        # check if server is installed
        return os.path.exists(SERVER_EXECUTABLE_PATH)

    def clone_repo(self, repo_url, clone_path):
        class CloneProgressTracker(git.RemoteProgress):
            def __init__(self):
                super().__init__()
                self.statusText = "Downloading Endfield Network deployment dependencies..."
                self.progressValue = 0
                self.isCancelled = False
                self.status = 0 # 1: downloading, 2: finished, 3: failed
            def update(self, op_code, cur_count, max_count, message):
                self.progressValue = int ( int(cur_count) / int(max_count) * 100)
                self.statusText = f"Dowloading Endfield Network deployment dependencies... [{int(cur_count)}/{int(max_count)}] {self.progressValue}%"
        self.fetchProgress = CloneProgressTracker()
        self.fetchProgress.status = 1
        try:
            # if the repo already exists, pull instead of clone
            if os.path.exists(clone_path):
                repo = git.Repo(clone_path)
                repo.remotes.origin.pull(progress=self.fetchProgress)
            else:
                git.Repo.clone_from(repo_url, clone_path, progress=self.fetchProgress)
            self.fetchProgress.status = 2
        except Exception as e:
            self.fetchProgress.statusText = f"Failed to download Endfield Network deployment dependencies: {e}"
            self.fetchProgress.status = 3
            print(f"Failed to download Endfield Network deployment dependencies: {e}")
            return False

    def find_msbuild(self):
        vswhere_path = os.path.join(
            os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"),
            "Microsoft Visual Studio",
            "Installer",
            "vswhere.exe"
        )
        if not os.path.exists(vswhere_path):
            raise FileNotFoundError(f"vswhere.exe not found at {vswhere_path}. Ensure Visual Studio is installed.")
        command = [
            vswhere_path,
            "-latest",
            "-products", "*",
            "-requires", "Microsoft.Component.MSBuild",
            "-find", "MSBuild\\**\\Bin\\MSBuild.exe"
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        msbuild_path = result.stdout.strip()
        if not msbuild_path or not os.path.exists(msbuild_path):
            raise FileNotFoundError("MSBuild.exe not found via vswhere.")
        return msbuild_path

    def compile_project(self, msbuild_path, solution_file, configuration="Release", progress_tracker=None):
        if not os.path.exists(solution_file):
            progress_tracker.statusText = f"Solution file not found: {solution_file}"
            progress_tracker.status = 3
            return False
        
        progress_tracker.statusText = f"Compiling Endfield Network Server..."
        progress_tracker.status = 1 # 1: working, 2: finished, 3: failed

        command = [
            msbuild_path,
            "/restore",  # Automatically run NuGet package restore.
            solution_file,
            f"/p:Configuration={configuration}"
        ]

        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            with open("msbuild_output.log", "w") as f:
                f.write(result.stdout)
                f.write(result.stderr)
            progress_tracker.statusText = f"Compilation failed. See msbuild_output.log for details."
            return False
        progress_tracker.statusText = "Compilation successful."
        return True

# Launcher UI
class Launcher(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = ui_launcher.Ui_MainWindow()
        self.ui.setupUi(self)

        self.setFixedSize(800, 500)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.ui.closeButton.clicked.connect(self.close)
        self.ui.minimizeButton.clicked.connect(self.showMinimized)

        # drag window
        self._isDragging = False
        self._dragPos = QPoint()
        self.ui.titleBar.mousePressEvent = self.titleBar_mousePressEvent
        self.ui.titleBar.mouseMoveEvent = self.titleBar_mouseMoveEvent
        self.ui.titleBar.mouseReleaseEvent = self.titleBar_mouseReleaseEvent

        # initialize backend
        self.gameLauncher = GameLauncherBackend()
        self.serverLauncher = ServerLauncherBackend()

        # setup server launch page
        self.ui.serverLauncherPage.hide()
        self.ui.serverLauncherNavButton.clicked.connect(self.onServerLauncherPageBtnClicked)
        self.ui.serverLaunchInfo.hide()
        self.ui.serverLaunchProgressBar.hide()
        self.ui.serverLaunchProgressBar.setValue(0)
        # 0: not installed, 1: installed, 2: installing
        self.serverReadyStatus = self.serverLauncher.getStatus()
        if self.serverReadyStatus == 0:
            self.ui.serverLaunchButton.setText("Install")
        elif self.serverReadyStatus == 1:
            self.ui.serverLaunchButton.setText("Launch")
        elif self.serverReadyStatus == 2:
            self.ui.serverLaunchButton.setText("Cancel")
        self.ui.serverLaunchButton.clicked.connect(self.onServerLaunchButtonClicked)

        # setup client launch page
        self.ui.gameLauncherPage.show()
        self.ui.gameLauncherNavButton.clicked.connect(self.onGameLauncherPageBtnClicked)
        self.ui.gameLaunchInfo.hide()
        self.ui.gameLaunchProgressBar.hide()
        self.ui.gameLaunchProgressBar.setValue(0)
        # 0: not installed, 1: installed, 2: installing
        self.gameReadyStatus = self.gameLauncher.getStatus()
        if self.gameReadyStatus == 0:
            self.ui.gameLaunchButton.setText("Install")
        elif self.gameReadyStatus == 1:
            self.ui.gameLaunchButton.setText("Launch")
        elif self.gameReadyStatus == 2:
            self.ui.gameLaunchButton.setText("Cancel")
        self.ui.gameLaunchButton.clicked.connect(self.onGameLaunchButtonClicked)

        # setup update ticker
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.onUpdate)
        self.timer.start(100)  # Tick every 100 ms

    # drag window related
    def titleBar_mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._isDragging = True
            self._dragPos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def titleBar_mouseMoveEvent(self, event):
        if self._isDragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self._dragPos)
            event.accept()

    def titleBar_mouseReleaseEvent(self, event):
        self._isDragging = False
        event.accept()

    # button callbacks
    def onServerLauncherPageBtnClicked(self):
        self.ui.gameLauncherPage.hide()
        self.ui.serverLauncherPage.show()
        self.ui.backgroundImage.setPixmap(QPixmap(":/assets/launcher_bg_b.png"))
        self.ui.label_20.setPixmap(QPixmap(":/assets/endfield_logo_v2_w.png"))
        self.ui.minimizeButton.setStyleSheet(u"QPushButton {\n"
"	background-color: rgba(0,0,0,0);\n"
"	color: rgb(30, 30, 30);\n"
"	border: 0px;\n"
"	border-image: url(:/assets/minimize_icon_w.png) no-repeat center center fixed;\n"
"	margin: 3px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(235, 235, 235, 50); /* Slightly lighter green */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgba(235, 235, 235, 100); /* Slightly darker green */\n"
"}")
        self.ui.closeButton.setStyleSheet(u"QPushButton {\n"
"	background-color: rgba(0,0,0,0);\n"
"	color: rgb(30, 30, 30);\n"
"	border: 0px;\n"
"	border-image: url(:/assets/close_icon_w.png) no-repeat center center fixed;\n"
"	margin: 3px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(235, 235, 235, 50); /* Slightly lighter green */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgba(235, 235, 235, 100); /* Slightly darker green */\n"
"}")

    def onGameLauncherPageBtnClicked(self):
        self.ui.serverLauncherPage.hide()
        self.ui.gameLauncherPage.show()
        self.ui.backgroundImage.setPixmap(QPixmap(":/assets/launcher_bg_a.png"))
        self.ui.label_20.setPixmap(QPixmap(":/assets/endfield_logo_v2.png"))
        self.ui.minimizeButton.setStyleSheet(u"QPushButton {\n"
"	background-color: rgba(0,0,0,0);\n"
"	color: rgb(30, 30, 30);\n"
"	border: 0px;\n"
"	border-image: url(:/assets/minimize_icon.png) no-repeat center center fixed;\n"
"	margin: 3px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(20, 20, 20, 50); /* Slightly lighter green */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgba(20, 20, 20, 100); /* Slightly darker green */\n"
"}")
        self.ui.closeButton.setStyleSheet(u"QPushButton {\n"
"	background-color: rgba(0,0,0,0);\n"
"	color: rgb(30, 30, 30);\n"
"	border: 0px;\n"
"	border-image: url(:/assets/close_icon.png) no-repeat center center fixed;\n"
"	margin: 3px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(20, 20, 20, 50); /* Slightly lighter green */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgba(20, 20, 20, 100); /* Slightly darker green */\n"
"}")

    def onGameLaunchButtonClicked(self):
        if self.gameReadyStatus == 0:
            # install game in a separate thread
            self.gameInstallerThread = threading.Thread(target=self.gameLauncher.initiateInstallation)
            # confirmation
            conf = show_popup("Confirmation", f"The game client will be installed at {GAME_INSTALL_PATH}. Do you want to proceed?", 1)
            if not conf:
                return
            self.gameInstallerThread.start()
            self.gameReadyStatus = 2
            self.ui.gameLaunchButton.setText("Cancel")
            self.ui.gameLaunchInfo.show()
            self.ui.gameLaunchProgressBar.show()

        elif self.gameReadyStatus == 1:
            ret = self.gameLauncher.launchGame()
            if not ret:
                show_popup("Error", "Failed to launch game: " + self.gameLauncher.statusText)
            else:
                self.close()

        elif self.gameReadyStatus == 2:
            self.gameLauncher.cancelInstallation()
            self.gameReadyStatus = 0
            self.ui.gameLaunchButton.setText("Install")
            self.ui.gameLaunchInfo.hide()
            self.ui.gameLaunchProgressBar.hide()

    def onServerLaunchButtonClicked(self):
        if self.serverReadyStatus == 0:
            # install server in a separate thread
            self.serverInstallerThread = threading.Thread(target=self.serverLauncher.initiateDownload)
            # confirmation
            conf = show_popup("Confirmation", f"The server will be installed at {SERVER_INSTALL_PATH}. Do you want to proceed?", 1)
            if not conf:
                return
            self.serverInstallerThread.start()
            self.serverReadyStatus = 2
            self.ui.serverLaunchButton.setText("Cancel")
            self.ui.serverLaunchInfo.show()
            self.ui.serverLaunchProgressBar.show()

        elif self.serverReadyStatus == 1:
            ret = self.serverLauncher.launchServer()
            if not ret:
                show_popup("Error", "Failed to launch server: " + self.serverLauncher.statusText)

        elif self.serverReadyStatus == 2:
            self.serverLauncher.cancelInstallation()
            self.serverReadyStatus = 0
            self.ui.serverLaunchButton.setText("Install")
            self.ui.serverLaunchInfo.hide()
            self.ui.serverLaunchProgressBar.hide()

    def onUpdate(self):
        # update game launcher info (only do when installing)
        if self.gameReadyStatus == 2:
            if self.gameLauncher.status == 1:   # downloading
                ret = self.gameLauncher.fetchInstallationProgress()
                if ret == 1:    # download completed -> start extracting
                    self.gameExtractorThread = threading.Thread(target=self.gameLauncher.initiateExtracting)
                    self.gameExtractorThread.start()
                    self.gameLauncher.status = 2    # ensure status is set to extracting
                elif ret == -1: # download failed
                    self.gameReadyStatus = 0

            elif self.gameLauncher.status == 4: # installation failed
                self.gameReadyStatus = 0

            elif self.gameLauncher.status == 2: # extracting
                if self.gameLauncher.extractTracker is None:
                    return
                self.ui.gameLaunchInfo.setText(self.gameLauncher.extractTracker.statusText)
                if self.gameLauncher.extractTracker.progressValue > 0 and self.gameLauncher.extractTracker.progressValue < 4: # for some odd reason the progress bar doesn't behave correctly when value is below 4
                    self.ui.gameLaunchProgressBar.setValue(4)
                else:
                    self.ui.gameLaunchProgressBar.setValue(self.gameLauncher.extractTracker.progressValue)
                return

            elif self.gameLauncher.status == 0: # installation completed
                self.gameReadyStatus = 1
                self.ui.gameLaunchButton.setText("Launch")
                self.ui.gameLaunchInfo.hide()
                self.ui.gameLaunchProgressBar.hide()

            # update display
            self.ui.gameLaunchInfo.setText(self.gameLauncher.statusText)
            if self.gameLauncher.progress > 0 and self.gameLauncher.progress < 4: # for some odd reason the progress bar doesn't behave correctly when value is below 4
                self.ui.gameLaunchProgressBar.setValue(4)
            else:
                self.ui.gameLaunchProgressBar.setValue(self.gameLauncher.progress)

        # update server launcher info (only do when installing)
        if self.serverReadyStatus == 2:
            if self.serverLauncher.status == 1: # downloading
                if self.serverLauncher.fetchProgress is None:
                    return
                elif self.serverLauncher.fetchProgress.status == 2: # download completed -> start building
                    self.serverBuilderThread = threading.Thread(target=self.serverLauncher.initiateBuild)
                    self.serverBuilderThread.start()
                    self.serverLauncher.status = 2  # ensure status is set to building
                elif self.serverLauncher.fetchProgress.status == 3: # download failed
                    self.serverReadyStatus = 0
                self.ui.serverLaunchInfo.setText(self.serverLauncher.fetchProgress.statusText)
                self.ui.serverLaunchProgressBar.setValue(self.serverLauncher.fetchProgress.progressValue)

            if self.serverLauncher.status == 2: # building
                if self.serverLauncher.buildProgress is None:
                    return
                self.ui.serverLaunchInfo.setText(self.serverLauncher.buildProgress.statusText)
                self.ui.serverLaunchProgressBar.setValue(self.serverLauncher.buildProgress.progressValue)
                if self.serverLauncher.buildProgress.progressValue == 100:
                    show_popup("Notice", "Don't forget to install MongoDB and start the service before launching the server.")
                    self.serverReadyStatus = 1
                    self.ui.serverLaunchButton.setText("Launch")
                    self.ui.serverLaunchInfo.hide()
                    self.ui.serverLaunchProgressBar.hide()

            if self.serverLauncher.status == 4:
                self.serverReadyStatus = 0
            
    def closeEvent(self, event):
        if self.gameLauncher.status != 0:
            self.gameLauncher.cancelInstallation()
        event.accept()

if __name__ == "__main__":

    app = QApplication(sys.argv)

    fontDatabase=QFontDatabase()
    fontDatabase.addApplicationFont(":/assets/fonts/NuberNext-Light.otf")
    fontDatabase.addApplicationFont(":/assets/fonts/NuberNext-Regular.otf")
    fontDatabase.addApplicationFont(":/assets/fonts/NuberNext-Bold.otf")

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    window = Launcher()
    window.show()
    sys.exit(app.exec())