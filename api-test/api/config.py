"""
@File:config.py
@Author:xzk
@Time: 2025/8/22 09:43
@Description: xxx
"""
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class APIConfig:
    api_key:str
    base_url:str
    timeout:int=10

    @classmethod
    def from_env(cls)->"APIConfig":
        #从环境变量加载配置
        return cls(
            api_key=os.getenv("QWEATHER_API_KEY", "4dc24cdfd9904976ac92a93dc824a1c2"),
            base_url=os.getenv("QWEATHER_BASE_URL", "https://p73jpewwq8.re.qweatherapi.com"),
            timeout=int(os.getenv("QWEATHER_TIMEOUT", "10"))
        )
@dataclass
class TestConfig:
    #测试配置
    test_data_dir :str ="test_data"
    default_location:str="101010100"
    invalid_location:str="999999999"