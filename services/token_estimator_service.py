"""
ForgeBud

Token estimator service.

Provides a fast provider-independent estimate of the number of
tokens contained in generated prompt text.
"""

from __future__ import annotations

import math


class TokenEstimatorService:
    """
    Estimates prompt token usage without calling an AI provider.
    """

    CHARACTERS_PER_TOKEN = 4

    @classmethod
    def estimate(cls, text: str) -> int:
        """
        Return an approximate token count for the supplied text.

        The estimate uses four characters per token, which is suitable
        for fast prompt-size guidance before provider integration.
        """
        if not text:
            return 0

        return math.ceil(
            len(text) / cls.CHARACTERS_PER_TOKEN
        )