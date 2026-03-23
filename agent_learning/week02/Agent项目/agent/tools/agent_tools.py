import os
import random
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from langchain_core.tools import tool

from rag.rag_service import RagSummarizeService
from utils.config_handler import agent_conf
from utils.logger_handler import logger
from utils.path_tool import get_abs_path

rag = RagSummarizeService()

user_ids = ["1001", "1002", "1003", "1004", "1005", "1006", "1007", "1008", "1009", "1010"]
month_arr = [
    "2025-01",
    "2025-02",
    "2025-03",
    "2025-04",
    "2025-05",
    "2025-06",
    "2025-07",
    "2025-08",
    "2025-09",
    "2025-10",
    "2025-11",
    "2025-12",
]

external_data = {}


@tool(description="用于回答扫地机器人相关的保养、故障排查、功能说明、选购建议、耗材维护和使用建议等问题。遇到这些问题时应优先调用本工具，从知识库检索依据后再作答。")
def rag_summarize(query: str) -> str:
    return rag.rag_summarize(query)


@tool(description="获取指定城市的天气信息，参数 city 必须是明确的城市名。")
def get_weather(city: str) -> str:
    return (
        f"城市{city}天气为晴天，气温26摄氏度，空气湿度50%，"
        f"南风1级，AQI21，最近6小时降雨概率极低"
    )


@tool(description="获取当前用户所在城市名称，返回纯文本城市名。")
def get_user_location() -> str:
    return random.choice(["深圳市", "合肥市", "杭州市"])


@tool(description="获取当前用户所在城市的天气。用户提到“我所在地区”“本地”“当地”“我这里”时，优先使用这个工具，不要自行猜测城市名。")
def get_weather_for_user_location() -> str:
    city = get_user_location.invoke({})
    weather = get_weather.invoke({"city": city})
    return f"当前用户所在地：{city}。{weather}"


@tool(description="获取当前用户 ID，返回纯文本字符串。")
def get_user_id() -> str:
    return random.choice(user_ids)


@tool(description="获取当前使用记录对应的自然月份。")
def get_current_month() -> str:
    return random.choice(month_arr)


def generate_external_data():
    if not external_data:
        external_data_path = get_abs_path(agent_conf["external_data_path"])

        if not os.path.exists(external_data_path):
            raise FileNotFoundError(f"外部数据文件不存在: {external_data_path}")

        with open(external_data_path, "r", encoding="utf-8") as f:
            for line in f.readlines()[1:]:
                if not line.strip():
                    continue

                arr = line.strip().split(",")
                user_id = arr[0].replace('"', "")
                feature = arr[1].replace('"', "")
                efficiency = arr[2].replace('"', "")
                consumables = arr[3].replace('"', "")
                comparison = arr[4].replace('"', "")
                time = arr[5].replace('"', "")

                if user_id not in external_data:
                    external_data[user_id] = {}

                external_data[user_id][time] = {
                    "特征": feature,
                    "效率": efficiency,
                    "耗材": consumables,
                    "对比": comparison,
                }


@tool(description="从外部系统中获取指定用户在指定月份的使用记录。若未查询到数据，返回空字符串。")
def fetch_external_data(user_id: str, month: str) -> str:
    generate_external_data()

    try:
        return external_data[user_id][month]
    except KeyError:
        logger.warning(f"[fetch_external_data]未查询到用户 {user_id} 在 {month} 的使用记录")
        return ""


@tool(description="无入参工具。调用后会切换到报告生成场景，用于后续生成正式分析报告。")
def fill_context_for_report():
    return "fill_context_for_report已调用"
