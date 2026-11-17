# Security notes

SmartDesk is a local training project. It uses synthetic data only and
binds to 127.0.0.1. Do not deploy it publicly as-is: it has no
authentication, no TLS and no logging.

Debug mode is off by default. Set SMARTDESK_DEBUG=1 only for local
development.

Found a security issue? Open a GitHub issue or contact the repository
owner.
