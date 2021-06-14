from collections import defaultdict
from datetime import datetime
from pathlib import Path
import subprocess

USER_IDX = 0
CPU_IDX = 2
MEM_IDX = 3
CMD_IDX = 10


def parse():
    output_data = {
        "users": set(),
        "proc_total": 0,
        "proc_per_user": defaultdict(int),
        "mem_total": 0,
        "cpu_total": 0,
        "max_mem_proc": "",
        "max_cpu_proc": ""
    }
    max_mem = 0
    max_cpu = 0
    ps_aux_output = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE, universal_newlines=True).stdout.readlines()
    for row in ps_aux_output[1:]:
        # there may be spaces in the "command" field
        ps_aux_fields = row.strip().split(maxsplit=10)
        output_data["users"].add(ps_aux_fields[USER_IDX])
        output_data["proc_total"] += 1
        output_data["proc_per_user"][ps_aux_fields[USER_IDX]] += 1
        output_data["mem_total"] += float(ps_aux_fields[MEM_IDX])
        output_data["cpu_total"] += float(ps_aux_fields[CPU_IDX])
        if float(ps_aux_fields[MEM_IDX]) >= max_mem:
            max_mem = float(ps_aux_fields[MEM_IDX])
            output_data["max_mem_proc"] = ps_aux_fields[CMD_IDX]
        if float(ps_aux_fields[CPU_IDX]) >= max_cpu:
            max_cpu = float(ps_aux_fields[CPU_IDX])
            output_data["max_cpu_proc"] = ps_aux_fields[CMD_IDX]

    return output_data


def save_report(ps_aux_report, dir_path):
    now = datetime.now().strftime("%d-%m-%Y-%H:%M")
    output_filepath = dir_path / f"{now}-scan.txt"
    output_data = f'Пользователи системы: {list(ps_aux_report["users"])}\n' \
                  f'Процессов запущено: {ps_aux_report["proc_total"]}\n'
    proc_per_user = " ".join(
        [f"{username}: {proc_count}" for username, proc_count in ps_aux_report["proc_per_user"].items()])
    output_data = f'{output_data}' \
                  f'Процессы по пользователям: {proc_per_user}\n' \
                  f'Всего памяти используется: {round(ps_aux_report["mem_total"], 2)}\n' \
                  f'Всего CPU используется: {round(ps_aux_report["cpu_total"], 2)}\n' \
                  f'Больше всего памяти ест: {ps_aux_report["max_mem_proc"][:19]}\n' \
                  f'Больше всего CPU ест: {ps_aux_report["max_cpu_proc"][:19]}\n'
    with open(output_filepath, "w", encoding="utf-8") as f:
        f.write(output_data)


if __name__ == "__main__":
    data = parse()
    save_report(data, Path(__file__).resolve().parent)
