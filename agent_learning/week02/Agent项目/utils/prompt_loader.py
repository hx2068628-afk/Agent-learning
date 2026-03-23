import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config_handler import prompts_config
from logger_handler import logger
from path_tool import get_abs_path


def load_system_prompt():
    try:
        system_prompt_path = get_abs_path(prompts_config["main_prompt_path"])
    except KeyError as e:
        logger.error("[load_system_prompt]yaml配置中缺少 main_prompt_path")
        raise e

    try:
        return open(system_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_system_prompt]读取系统提示词失败，错误信息: {str(e)}")
        raise e


def load_system_prompts():
    return load_system_prompt()


def load_rag_summarize_prompt():
    try:
        rag_prompt_path = get_abs_path(prompts_config["rag_summarize_prompt_path"])
    except KeyError as e:
        logger.error("[load_rag_summarize_prompt]yaml配置中缺少 rag_summarize_prompt_path")
        raise e

    try:
        return open(rag_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_rag_summarize_prompt]读取RAG总结提示词失败，错误信息: {str(e)}")
        raise e


def load_report_prompt():
    try:
        report_prompt_path = get_abs_path(prompts_config["report_prompt_path"])
    except KeyError as e:
        logger.error("[load_report_prompt]yaml配置中缺少 report_prompt_path")
        raise e

    try:
        return open(report_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_report_prompt]读取报告提示词失败，错误信息: {str(e)}")
        raise e


def load_report_prompts():
    return load_report_prompt()


if __name__ == "__main__":
    print(load_system_prompt())
