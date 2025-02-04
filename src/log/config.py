import logfire
import orjson
import structlog
from structlog import BytesLoggerFactory, WriteLoggerFactory
from structlog.processors import JSONRenderer
from structlog.dev import ConsoleRenderer

from settings import settings


def get_renderer() -> JSONRenderer | ConsoleRenderer:
    return ConsoleRenderer() if settings.general_settings.app_mode == "DEV" else JSONRenderer(serializer=orjson.dumps)


def get_logger_factory() -> BytesLoggerFactory | WriteLoggerFactory:
    return WriteLoggerFactory() if settings.general_settings.app_mode == "DEV" else BytesLoggerFactory()


def get_time_stamper() -> structlog.processors.TimeStamper:
    return (
        structlog.processors.TimeStamper(fmt="%d-%m-%Y %H:%M:%S %Z", utc=True)
        if settings.general_settings.app_mode == "DEV"
        else structlog.processors.TimeStamper(fmt="iso", utc=True)
    )


logfire.configure(
    token=settings.logfire_settings.token.get_secret_value(),
    console=settings.logfire_settings.console,
    service_name=settings.logfire_settings.service_name,
    send_to_logfire=settings.logfire_settings.send_to_logfire,
)

structlog.configure(
    cache_logger_on_first_use=True,
    wrapper_class=structlog.make_filtering_bound_logger(settings.logger_settings.level),
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.format_exc_info,
        get_time_stamper(),
        logfire.StructlogProcessor(),
        get_renderer(),
    ],
    logger_factory=get_logger_factory(),
)

logger = structlog.getLogger(settings.logger_settings.name)
