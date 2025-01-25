from typing import Dict


class EndpointLogger:
    def __init__(self):
        self.count = 0
        self.errors = 0
        self.incoming_bytes = 0
        self.outgoing_bytes = 0
        self.response_times = 0

    def log(
        self,
        success: bool,
        response_time: int,
        incoming_bytes: int,
        outgoing_bytes: int,
    ):
        self.count += 1
        if not success:
            self.errors += 1
        self.incoming_bytes += incoming_bytes
        self.outgoing_bytes += outgoing_bytes
        self.response_times += response_time

    def get_log_data(self):
        return {
            "request_count": self.count,
            "incoming_bytes": self.incoming_bytes,
            "outgoing_bytes": self.outgoing_bytes,
            **(
                {
                    "error_rate": (self.errors / self.count) * 100,
                    "average_response_time": self.response_times / self.count,
                }
                if self.count
                else {
                    "error_rate": 0,
                    "average_response_time": 0,
                }
            ),
        }


class StatsTracker:
    def __init__(self):
        self.data: Dict[str, EndpointLogger] = {}

    def log_request(
        self,
        endpoint: str,
        success: bool,
        response_time: int,
        incoming_bytes: int,
        outgoing_bytes: int,
    ):
        self.data.setdefault(endpoint, EndpointLogger()).log(
            success=success,
            response_time=response_time,
            incoming_bytes=incoming_bytes,
            outgoing_bytes=outgoing_bytes,
        )

    def get_stats(self):
        return {endpoint: stats.get_log_data() for endpoint, stats in self.data.items()}
