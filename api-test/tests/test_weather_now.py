import pytest
from typing import Dict, Any
from api.client import WeatherAPIClient
from utils.file_utils import load_test_data
from api.config import APIConfig, TestConfig

# 加载测试数据
TEST_DATA = load_test_data(
    "weather_now_tests.json",
    data_dir=TestConfig.test_data_dir
)


@pytest.fixture(scope="session")
def api_client():
    """API客户端fixture"""
    config = APIConfig.from_env()
    return WeatherAPIClient(config)


@pytest.mark.parametrize("test_case", TEST_DATA, ids=[case["name"] for case in TEST_DATA])
def test_weather_now_simple(api_client: WeatherAPIClient, test_case: Dict[str, Any]):
    """实时天气接口测试：仅断言状态码和错误信息"""
    # 发送请求
    response = api_client.get(
        endpoint="/v7/weather/now",
        params=test_case["params"]
    )

    # 1. 断言状态码是否符合预期
    assert str(response["status_code"]) == test_case["expected_code"], \
        f"测试用例 [{test_case['name']}] 状态码验证失败: " \
        f"预期 {test_case['expected_code']}, 实际 {response['status_code']}"

    # 2. 对于失败用例，断言错误消息存在
    if test_case["expected_code"] != "200":
        assert "arror" in response["data"], \
            f"测试用例 [{test_case['name']}] 失败但未返回错误信息"
        assert "detail" in response["data"]["error"], \
            f"测试用例 [{test_case['name']}] 失败但未返回详细错误原因"



if __name__ == "__main__":

    pytest.main([__file__, "-v"])
