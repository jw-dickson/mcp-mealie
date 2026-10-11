"""Serve mcp-mealie over Streamable HTTP as one long-lived process (jwdev deployment).

Upstream's console script only speaks stdio, so a stdio→HTTP bridge
(supergateway) started a fresh Python process, plus a Mealie probe, for every
MCP session. Behind a gateway that opens a session per tool call, that cost
~1.5 s per call. This reuses upstream's own startup check and server builder
and only swaps the transport. Not part of the upstream PR.
"""

import asyncio
import os

from mealie_mcp.config import Config
from mealie_mcp.server import _verify, build_server, configure_logging

config = Config.from_env()
configure_logging(config.log_level)
asyncio.run(_verify(config))  # fail fast on a bad URL or token, like main()
build_server(config).run(
    transport="http",
    # 0.0.0.0: in a container, reachable only on the gateway's internal overlay.
    host=os.environ.get("MCP_HOST", "0.0.0.0"),
    port=int(os.environ.get("MCP_PORT", "8000")),
    path="/mcp",
)
