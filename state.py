"""State utilities for chatbot sample.

Provides a simple helper to generate a random integer.
"""

from __future__ import annotations

import random
from typing import Optional


def generate_random_number(min_value: int = 0, max_value: int = 100, seed: Optional[int] = None) -> int:
	"""Return a random integer between min_value and max_value (inclusive).

	Args:
		min_value: Lower bound (inclusive).
		max_value: Upper bound (inclusive).
		seed: Optional random seed for reproducible results.

	Returns:
		A random integer in [min_value, max_value].
	"""
	if seed is not None:
		random.seed(seed)
	return random.randint(min_value, max_value)


if __name__ == "__main__":
	# Quick demo
	print(generate_random_number())

