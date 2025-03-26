import statsd

# Initialize StatsD client with host and port of CloudWatch Agent or StatsD exporter
statsd_host = '127.0.0.1'  # Replace with your StatsD host if different
statsd_port = 8125         # Default StatsD port

# Create a StatsD client with a prefix for metrics
statsd_client = statsd.StatsClient(host=statsd_host, port=statsd_port, prefix="webapp")

def increment_counter(metric_name):
    """Increment a counter metric."""
    statsd_client.incr(metric_name)

def record_timer(metric_name, duration):
    """Record a timer metric."""
    statsd_client.timing(metric_name, duration)

def record_gauge(metric_name, value):
    """Record a gauge metric."""
    statsd_client.gauge(metric_name, value)
