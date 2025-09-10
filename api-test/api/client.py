"""
@File:client.py
@Author:xzk
@Time: 2025/8/22 09:43
@Description: API客户端
"""
import json

import requests
from typing  import  Dict,Optional,Any,Union
from api.config import  APIConfig

class WeatherAPIClient:
    #和风天气api客户端
    def __init__(self, config: APIConfig):
        """初始化客户端

        Args:
            config: API配置对象
        """
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            "X-QW-Api-Key": self.config.api_key,
            "Accept": "application/json",
            "Accept-Encoding": "gzip"
        })

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Union[int, str, Dict[str, Any]]]:
        """发送GET请求

        Args:
            endpoint: API端点路径
            params: 查询参数

        Returns:
            响应JSON数据，包含status_code和响应内容
        """
        url = f"{self.config.base_url}{endpoint}"
        response_json: Dict[str, Union[int, str, Dict[str, Any]]] = {}  # 修正类型注解

        try:
            response = self.session.get(
                url,
                params=params or {},
                timeout=self.config.timeout
            )

            # 解析JSON响应
            try:
                data = response.json()
            except json.JSONDecodeError:
                data = {"error": {"detail": "Invalid JSON response"}}

            # 状态码是int类型，添加到响应数据
            response_json["status_code"] = response.status_code  # 现在类型匹配
            response_json["data"] = data

            return response_json

        except requests.exceptions.RequestException as e:
            error_msg = f"API请求失败: {str(e)}"
            response_json["status_code"] = 500  # int类型
            response_json["error"] = {"detail": error_msg}
            return response_json