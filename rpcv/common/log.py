import structlog


def get_logger() -> structlog._config.BoundLoggerLazyProxy:
    """Just stubbed out in case we want later configuration."""
    logger = structlog.getLogger()
    return logger
