import openai
from config import OPENAI_API, MODEL, TEMPERATURE, MAX_TOKENS
from gs import make_today_report, make_yesterday_report, make_last_week_report
from texts import t_gpt_report, t_gs_report, t_prompts



openai.api_key = OPENAI_API

def call_ai(prompt: str) -> str:
    """ Принимает запрос. Возращает ответ от ChatGPT. """
    completion = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "assistant", "content": f"{prompt}"}
        ],
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )
    
    return(completion["choices"][0]["message"]["content"])

def make_gpt_request(report_data: dict) -> str:
    """ 
    Запускает формирование отчета GS на основании выбранного пользователем временного промежутка.
    Объеденяет результат с заготовленным промптом, так-же выбранным пользователем.
    """
    if report_data["report_range"] == t_gs_report.report_today:
        data = make_today_report()
    elif report_data["report_range"] == t_gs_report.report_yesterday:
        data = make_yesterday_report()
    elif report_data["report_range"] == t_gs_report.report_last_week:
        data = make_last_week_report()
    
    if report_data["report_type"] == t_gpt_report.analysis:
        prompt = t_prompts.analysis+data
    elif report_data["report_type"] == t_gpt_report.anomaly:
        prompt = t_prompts.anomaly+data
    elif report_data["report_type"] == t_gpt_report.recommendations:
        prompt = t_prompts.recommendation+data

    answer = call_ai(prompt)
    return(answer)

def make_gpt_free_prompt_request(free_prompt: str, report_data: str) -> str:
    """ 
    Запускает формирование отчета GS на основании выбранного пользователем временного промежутка.
    Объеденяет результат с промптом введенным вручную.
    """
    if report_data == t_gs_report.report_today:
        data = make_today_report()
    elif report_data == t_gs_report.report_yesterday:
        data = make_yesterday_report()
    elif report_data == t_gs_report.report_last_week:
        data = make_last_week_report()
    prompt = free_prompt+data
    answer = call_ai(prompt)
    return(answer)