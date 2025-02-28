import sys
import asyncio
from pathlib import Path
from typing import Optional

current_dir = Path(__file__).resolve().parent

src_path = current_dir.parent.parent
sys.path.append(str(src_path.parent))
print(str(src_path.parent))

from src.core.xml.reader import XMLReader
from src.core.database.pymongo import MongoDB

class XMLProcessor:
    def __init__(self, db_name: str):
        self.xml_reader = XMLReader()
        self.db_name = db_name

    async def process_file(self, file_path: Path) -> dict:
        """XML 파일을 처리하고 DB에 저장"""
        try:
            # XML 파일 읽기
            root = self.xml_reader.read_file(file_path)
            
            # 데이터 변환
            data = self._transform_data(root)
            
            # DB 저장
            async with MongoDB(self.db_name) as db:
                result = await db.collection.insert_one(data)
                
            return {"status": "success", "id": str(result.inserted_id)}
            
        except Exception as e:
            raise ProcessingError(f"Failed to process file: {str(e)}")

    def _transform_data(self, root) -> dict:
        """XML 데이터를 DB 스키마에 맞게 변환"""
        # 변환 로직 구현
        pass