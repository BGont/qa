import argparse
from collections import defaultdict, Counter
import json
from pathlib import Path
import re
import sys

# https://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html
RFC_COMMON_METHODS = ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "TRACE", "CONNECT"]


class MethodException(Exception):
    pass


def parse_log_row(log_row):
    found = re.search(r"^(.+) .+ .+ \[.+\] \"(.+)\" (\d+) .+ \".*\" \".*\" (\d+)$", log_row)
    ip, method_url, status, duration = found.groups()
    method, url, *_ = method_url.split()
    method = method.upper()
    if method not in RFC_COMMON_METHODS:
        raise MethodException
    duration = int(duration)
    return ip, method, url, status, duration


def parse_log(logfile):
    output_log_data = {
        "request_types": defaultdict(int),
        "ips": defaultdict(int),
        "long_reqs": [],
        "client_error_reqs": defaultdict(int),
        "server_error_reqs": defaultdict(int),
        "log_rows_count": 0,
    }
    for log_row in logfile:
        try:
            ip, method, url, status, duration = parse_log_row(log_row.strip())
        except MethodException:
            continue
        finally:
            output_log_data["log_rows_count"] += 1

        output_log_data["request_types"][method] += 1
        output_log_data["ips"][ip] += 1
        output_log_data["long_reqs"].append(
            {"ip": ip, "metod": method, "url": url, "duration": duration}
        )
        if status.startswith('4'):
            output_log_data["client_error_reqs"][(ip, url, method)] += 1
        if status.startswith('5'):
            output_log_data["server_error_reqs"][(ip, url, method)] += 1

    return output_log_data


def report(file_path, log_data):
    report_data = {
        "file_path": file_path,
        "rfc_common_methods_stat": log_data["request_types"],
        "requests_count": log_data["log_rows_count"],
        "top_10_ips": Counter(log_data["ips"]).most_common(10),
        "top_10_longest_reqs": sorted(log_data["long_reqs"], key=lambda item: item["duration"], reverse=True)[:10],
        "top_10_client_errors": Counter(log_data["client_error_reqs"]).most_common(10),
        "top_10_server_errors": Counter(log_data["server_error_reqs"]).most_common(10)
    }

    return report_data


def report_ouput_json(report_logs, path_to_json):
    path = Path(path_to_json)
    with open(path, "w") as f:
        f.write(json.dumps(report_logs, indent=4))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-df", "--df",
                        dest='path',
                        required=True,
                        help='Path to log file or dir with multiple log files')
    args = parser.parse_args()

    arg_path = Path(args.path)
    if not arg_path.exists():
        print("Log file or directory doesn't exist")
        sys.exit(-1)
    if arg_path.is_file():
        logfile_paths = [arg_path]
    elif arg_path.is_dir():
        logfile_paths = [arg_path / filename for filename in arg_path.iterdir() if filename.is_file()]
        if not logfile_paths:
            print("Directory doesn't contain files")
            sys.exit(-1)
    else:
        print("Path doesn't point to regular file or directory")
        sys.exit(-1)

    try:
        report_logs = []
        for logfile_path in logfile_paths:
            with open(logfile_path) as logfile:
                parsed_log = parse_log(logfile)
                report_logs.append(report(str(logfile_path), parsed_log))
    except OSError:
        print("Can't open {filepath}".format(filepath=str(logfile_path)))
        sys.exit(-1)

    report_ouput_json(report_logs, "report_logs.json")
