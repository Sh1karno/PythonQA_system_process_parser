#! /usr/bin/env python3

import re
import os
import subprocess

from datetime import datetime
from collections import Counter


class SystemProcessParser:

    _REGEX = r"(\S+)\s+\d+\s+(\d+\.\d+)\s+(\d+\.\d+)\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+(.+)"

    def __init__(self):
        self.processes_list = self.get_system_processes_list()
        self.users = []
        self.total_processes = 0
        self.user_processes = Counter()
        self.total_memory = 0.0
        self.total_cpu = 0.0
        self.max_memory_process = 0.0
        self.max_memory_process_name = ""
        self.max_cpu_process = 0.0
        self.max_cpu_process_name = ""

    @staticmethod
    def get_system_processes_list():
        ps = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE).communicate()[0]
        return ps.decode("UTF-8").split("\n")[1:-1]

    def parse_system_processes(self):
        for line in self.processes_list:
            self.total_processes += 1
            regex_line = re.search(self._REGEX, line).groups()
            user = regex_line[0]
            if user not in self.users:
                self.users.append(user)

            self.user_processes[user] += 1

            memory = float(regex_line[2])
            self.total_memory += memory
            if memory > self.max_memory_process:
                self.max_memory_process = memory
                self.max_memory_process_name = regex_line[3][:20]

            cpu = float(regex_line[1])
            self.total_cpu += cpu
            if cpu > self.max_cpu_process:
                self.max_cpu_process = cpu
                self.max_cpu_process_name = regex_line[3][:20]

    def get_users_prosesses(self):
        _data = ""
        for user, count in self.user_processes.items():
            _data += f"{user}: {count} "
        return _data

    def get_data(self):
        _data = f"Пользователи системы: {self.users}\n" \
                f"Процессов запущено: {self.total_processes}\n" \
                f"Процессы по пользователям: {self.get_users_prosesses()}\n" \
                f"Всего памяти используется: {round(self.total_memory, 2)}%\n" \
                f"Всего CPU используется: {round(self.total_cpu, 2)}%\n" \
                f"Больше всего памяти ест: {self.max_memory_process_name}: {self.max_memory_process}%\n" \
                f"Больше всего CPU ест: {self.max_cpu_process_name}: {self.max_cpu_process}%\n"
        return _data

    def create_result_file(self):
        now = datetime.now().strftime("%d-%m-%Y-%H:%M")
        filename = os.path.join(os.path.dirname(__file__), f"result/{now}-scan.txt")
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as file:
            file.write(self.get_data())


if __name__ == "__main__":
    parser = SystemProcessParser()
    parser.parse_system_processes()
    print(parser.get_data())
    parser.create_result_file()
