from pathlib import Path
import sys
import logging
current_file = Path(__file__).resolve()
app_dir = current_file.parent.parent  # app 디렉토리 찾기
sys.path.append(str(app_dir))

print(f"Added to Python path: {app_dir}")

# 이제 app 디렉토리를 기준으로 import 가능
from src.core.utils.logger import Logger


@Logger(
    log_dir="logs/dev",
    level=logging.INFO,
    format_string='%(asctime)s [%(levelname)s] %(message)s',
    timezone='Asia/Seoul'
)
def main():
    try:
        print("Test function executed")
        
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    main()