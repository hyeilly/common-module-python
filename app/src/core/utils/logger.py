import sys
import logging
import functools
from pathlib import Path
from datetime import datetime
from typing import Optional, Callable, Any
from zoneinfo import ZoneInfo 

class StreamToLogger:
    """
    print문 로깅에 출력
    """
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())
    
    def flush(self):
        pass


class Logger:
    def __init__(
        self,
        log_dir: str = "logs/dev",
        level: int = logging.INFO,
        format_string: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        timezone: str = 'Asia/Seoul'
    ):
        self.project_root = self._find_project_root()
        self.log_dir = self.project_root / log_dir
        self.level = level
        self.format_string = format_string
        self.timezone = ZoneInfo(timezone)
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def _setup_logger(
        self,
        name: str,
        log_file: Path
    ) -> logging.Logger:
        """로거 설정 메서드"""
        logger = logging.getLogger(name)
        logger.setLevel(self.level)

        logger.handlers = []

        formatter = logging.Formatter(
            self.format_string,
            datefmt='%Y-%m-%d %H:%M:%S %z'
        )
        formatter.converter = lambda *args: datetime.now(self.timezone).timetuple()

        file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        return logger


    def _find_project_root(self) -> Path:
        """프로젝트 루트 디렉토리를 찾는 메서드"""
        current_dir = Path.cwd()
        root_indicators = [
            'pyproject.toml',
            'setup.py',
            '.git',
            'src',
            'tests'
        ]
        while current_dir != current_dir.parent:
            if any((current_dir / indicator).exists() for indicator in root_indicators):
                return current_dir
            current_dir = current_dir.parent
            
        return Path.cwd()

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # 로그 파일명 생성
            today = datetime.now(self.timezone).strftime("%Y%m%d")
            log_file = self.log_dir / f"{func.__name__}_{today}.log"

            logger = self._setup_logger(func.__name__, log_file)
            current_time = datetime.now(self.timezone).strftime("%Y-%m-%d %H:%M:%S %z")

            stdout_logger = StreamToLogger(logger, logging.INFO)
            stderr_logger = StreamToLogger(logger, logging.ERROR)
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            
            try:
                sys.stdout = stdout_logger
                sys.stderr = stderr_logger

                logger.info(f"[{current_time}] Starting function: {func.__name__}")
                result = func(*args, **kwargs)
                logger.info(f"[{current_time}] Function completed successfully: {func.__name__}")
                return result
                
            except Exception as e:
                logger.error(f"Test failed: {func.__name__}")
                logger.error(f"Error: {str(e)}", exc_info=True)
                raise
            finally:
                sys.stdout = old_stdout
                sys.stderr = old_stderr
        return wrapper