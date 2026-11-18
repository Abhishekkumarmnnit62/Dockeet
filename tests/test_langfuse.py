# test_langfuse.py

from backend.observability.langfuse_client import (
    langfuse
)

print(langfuse)

import langfuse as lf

print(
    lf.__version__
)

print(
    type(langfuse)
)
