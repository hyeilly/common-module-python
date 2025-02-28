import functools
from pathlib import Path
from datetime import datetime
from ..utils.logger import Logger

def log_test(test_dir: str = "tests/logs"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 로그 파일 경로 설정
            log_dir = Path(test_dir)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = log_dir / f"{func.__name__}_{timestamp}.log"
            
            # 로거 설정
            logger = Logger.setup_logger(
                name=func.__name__,
                log_file=log_file
            )
            
            try:
                logger.info(f"Starting test: {func.__name__}")
                result = func(*args, **kwargs)
                logger.info(f"Test completed successfully: {func.__name__}")
                return result
            except Exception as e:
                logger.error(f"Test failed: {func.__name__}, Error: {str(e)}")
                raise
            
        return wrapper
    return decorator