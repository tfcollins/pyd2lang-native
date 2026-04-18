"""Tests for d2.sphinx.cache."""

from __future__ import annotations

from pathlib import Path

import pytest

from d2.sphinx import cache


def test_make_key_is_deterministic():
    k1 = cache.make_key("a -> b", "adi", "light", "0.1.1")
    k2 = cache.make_key("a -> b", "adi", "light", "0.1.1")
    assert k1 == k2


def test_make_key_changes_with_source():
    k1 = cache.make_key("a -> b", "adi", "light", "0.1.1")
    k2 = cache.make_key("a -> c", "adi", "light", "0.1.1")
    assert k1 != k2


def test_make_key_changes_with_library():
    k1 = cache.make_key("x", "adi", "light", "0.1.1")
    k2 = cache.make_key("x", "sw", "light", "0.1.1")
    assert k1 != k2


def test_make_key_changes_with_theme():
    k1 = cache.make_key("x", "adi", "light", "0.1.1")
    k2 = cache.make_key("x", "adi", "dark", "0.1.1")
    assert k1 != k2


def test_make_key_changes_with_version():
    k1 = cache.make_key("x", "adi", "light", "0.1.1")
    k2 = cache.make_key("x", "adi", "light", "0.1.2")
    assert k1 != k2


def test_make_key_handles_none_library():
    k = cache.make_key("x", None, "light", "0.1.1")
    assert isinstance(k, str) and len(k) == 64  # sha256 hex


def test_put_and_get_round_trip(tmp_path: Path):
    key = cache.make_key("a", "adi", "light", "0.1.1")
    cache.put(tmp_path, key, "<svg>hello</svg>")
    assert cache.get(tmp_path, key) == "<svg>hello</svg>"


def test_get_returns_none_when_missing(tmp_path: Path):
    key = cache.make_key("missing", None, "light", "0.1.1")
    assert cache.get(tmp_path, key) is None


def test_cache_path_uses_two_char_fanout(tmp_path: Path):
    key = "abcdef0123456789" + "0" * 48
    path = cache.cache_path(tmp_path, key)
    assert path.parent.name == "ab"
    assert path.name == f"{key}.svg"


def test_put_creates_fanout_directory(tmp_path: Path):
    key = cache.make_key("x", None, "light", "0.1.1")
    cache.put(tmp_path, key, "<svg/>")
    assert (tmp_path / key[:2]).is_dir()
    assert (tmp_path / key[:2] / f"{key}.svg").is_file()
