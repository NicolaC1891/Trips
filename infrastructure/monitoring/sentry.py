import sentry_sdk


def init_sentry():
    sentry_sdk.init(
        dsn="https://e1d4252cb6720e71a6804c69a9d5f774@o4509660372533248.ingest.de.sentry.io/4509660384854096"
    )
