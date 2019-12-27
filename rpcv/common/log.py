import logging
import structlog
from structlog.stdlib import filter_by_level


def get_logger(log_name: str = __name__) -> structlog._config.BoundLoggerLazyProxy:
    """Just stubbed out in case we want later configuration."""
    structlog.configure(
        processors=[
            # This performs the initial filtering, so we don't
            # evaluate e.g. DEBUG when unnecessary
            structlog.stdlib.filter_by_level,
            # Adds logger=module_name (e.g __main__)
            structlog.stdlib.add_logger_name,
            # Adds level=info, debug, etc.
            structlog.stdlib.add_log_level,
            # Who doesnt like timestamps?
            structlog.processors.TimeStamper(fmt="iso"),
            # Performs the % string interpolation as expected
            structlog.stdlib.PositionalArgumentsFormatter(),
            # Include the stack when stack_info=True
            structlog.processors.StackInfoRenderer(),
            # Include the exception when exc_info=True
            # e.g log.exception() or log.warning(exc_info=True)'s behavior
            structlog.processors.format_exc_info,
            # Decodes the unicode values in any kv pairs
            structlog.processors.UnicodeDecoder(),
            # Creates the necessary args, kwargs for log()
            structlog.stdlib.render_to_log_kwargs,
        ],
        # Our "event_dict" is explicitly a dict
        # There's also structlog.threadlocal.wrap_dict(dict) in some examples
        # which keeps global context as well as thread locals
        context_class=dict,
        # Provides the logging.Logger for the underlaying log call
        logger_factory=structlog.stdlib.LoggerFactory(),
        # Provides predefined methods - log.debug(), log.info(), etc.
        wrapper_class=structlog.stdlib.BoundLogger,
        # Caching of our logger
        cache_logger_on_first_use=True,
    )
    logging.basicConfig(level=logging.DEBUG)
    logger = structlog.wrap_logger(
        logging.getLogger(log_name),
        processors=[
            filter_by_level,
            structlog.processors.JSONRenderer(indent=2, sort_keys=True),
        ],
    )
    return logger
