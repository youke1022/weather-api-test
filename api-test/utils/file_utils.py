"""
@File:file_utils.py
@Author:xzk
@Time: 2025/8/22 10:22
@Description: 测试数据加载工具
"""
import json
from pathlib import Path
from typing import List,Dict,Any

def load_test_data(file_name:str,data_dir:str="test_data")->List[Dict[str, Any]]:
    #加载测试json数据文件
    """
    :param file_name:测试数据文件名
    :param data_dir: 数据文件目录
    :return: 测试用例列表
    """
    file_path = Path(data_dir)/ file_name

    if not file_path.exists():
        raise FileNotFoundError(f"测试数据文件不存在:{file_path}")

    with open(file_path,"r",encoding="utf-8") as f:
        test_data = json.load(f)

    #验证测试数据格式
    if not isinstance(test_data,list):
        raise ValueError("测试数据文件必须包含一个数组")

    for index,case in enumerate(test_data):
        if not isinstance(case,dict):
            raise ValueError(f"测试用例{index}必须是字典")

        required_fields=["name","params","expected_code"]
        for field in required_fields:
            if field not in case:
                raise ValueError(f"测试用例{index}缺少必要字段:{field}")

    return test_data
