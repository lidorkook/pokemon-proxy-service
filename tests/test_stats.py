from app.stats import EndpointLogger, StatsTracker


def test_endpoint_logger():
    logger = EndpointLogger()
    logger.log(success=True, response_time=100, incoming_bytes=200, outgoing_bytes=300)
    assert logger.count == 1
    assert logger.errors == 0
    assert logger.incoming_bytes == 200
    assert logger.outgoing_bytes == 300
    assert logger.response_times == 100
    logger.log(success=False, response_time=200, incoming_bytes=300, outgoing_bytes=400)
    assert logger.count == 2
    assert logger.errors == 1
    assert logger.incoming_bytes == 500
    assert logger.outgoing_bytes == 700
    assert logger.response_times == 300


def test_stats_tracker():
    tracker = StatsTracker()
    tracker.log_request(
        "test_endpoint",
        success=True,
        response_time=100,
        incoming_bytes=200,
        outgoing_bytes=300,
    )
    stats = tracker.get_stats()
    assert "test_endpoint" in stats
    assert stats["test_endpoint"]["request_count"] == 1
    assert stats["test_endpoint"]["incoming_bytes"] == 200
    assert stats["test_endpoint"]["outgoing_bytes"] == 300
    assert stats["test_endpoint"]["error_rate"] == 0
    assert stats["test_endpoint"]["average_response_time"] == 100
    tracker.log_request(
        "test_endpoint",
        success=False,
        response_time=200,
        incoming_bytes=300,
        outgoing_bytes=400,
    )
    stats = tracker.get_stats()
    assert "test_endpoint" in stats
    assert stats["test_endpoint"]["request_count"] == 2
    assert stats["test_endpoint"]["incoming_bytes"] == 500
    assert stats["test_endpoint"]["outgoing_bytes"] == 700
    assert stats["test_endpoint"]["error_rate"] == 50.0
    assert stats["test_endpoint"]["average_response_time"] == 150
