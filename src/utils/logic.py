import json

from dateutil.relativedelta import relativedelta

from pymongo.command_cursor import CommandCursor

from src.config import FORMAT_INTERVAL

from src.database import Request, get_queryset


async def generate_date_range(start_date, end_date, interval):
    datetime_list = []
    current_date = start_date
    interval = {f"{interval}s": +1}
    while current_date <= end_date:
        datetime_list.append(current_date)
        current_date += relativedelta(**interval)
    return datetime_list


async def build_answer_structure(
        queryset: CommandCursor,
        request: Request
) -> dict:
    dataset = []
    labels = []
    row = queryset.try_next()
    datetime_list = await generate_date_range(
        request.dt_from,
        request.dt_upto,
        request.group_type
    )
    for time_point in datetime_list:
        date = time_point.strftime(FORMAT_INTERVAL[request.group_type])
        labels.append(date)
        total_salary = 0
        if row and row["_id"] == date:
            total_salary = row["total_salary"]
            row = queryset.try_next()
        dataset.append(int(total_salary))
    return dict(dataset=dataset, labels=labels)


async def get_aggregate_data(request: dict) -> dict:
    req = Request(**request)
    queryset = await get_queryset(req)
    answer = await build_answer_structure(queryset, req)
    return answer


async def build_answer(request: str) -> str:
    try:
        request = json.loads(request)
    except (SyntaxError, ValueError):
        return "Не верный тип данных"
    result = await get_aggregate_data(request)
    return str(result).replace("'", '"')