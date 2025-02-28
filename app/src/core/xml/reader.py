from pathlib import Path
import xml.etree.ElementTree as ET
from typing import Union, Optional

class XMLReader:
    def __init__(self, encoding: str = 'utf-8'):
        self.encoding = encoding

    def read_file(self, file_path: Union[str, Path]) -> ET.Element:
        """XML 파일을 읽어서 Element 객체로 반환"""
        try:
            tree = ET.parse(file_path)
            return tree.getroot()
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML file: {e}")
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")

    def read_string(self, xml_string: str) -> ET.Element:
        """XML 문자열을 읽어서 Element 객체로 반환"""
        try:
            return ET.fromstring(xml_string)
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML string: {e}")