from unittest.mock import patch

import dns.resolver
import pytest

from validators import dns_resolve_ip, is_valid_ip, is_valid_url


def test_valid_ip():
    assert is_valid_ip("81.41.222.0") is True
    assert is_valid_ip("127.0.0.1") is False
    assert is_valid_ip("hellothere") is False
    assert is_valid_ip("-1.0.2.3") is False
    assert is_valid_ip("0.0.0.0") is False
    assert is_valid_ip("255.255.255.255") is False
    assert is_valid_ip("") is False
    assert is_valid_ip(" 192.168.0.1 ") is False


def test_valid_url():
    assert is_valid_url("http://example.com") is True
    assert is_valid_url("google.com") is True
    assert is_valid_url("http://") is False


@patch("dns.resolver.Resolver")
@patch("os.getenv")
def test_valid_domain(mock_getenv, mock_resolver):
    mock_getenv.return_value = "8.8.8.8"
    mock_resolver.return_value.resolve.return_value = ["93.184.216.34"]
    result = dns_resolve_ip("example.com")
    assert result == "93.184.216.34"


@patch("dns.resolver.Resolver")
def test_domain_not_found(mock_resolver):
    mock_resolver.return_value.resolve.side_effect = dns.resolver.NXDOMAIN
    with pytest.raises(Exception) as context:
        dns_resolve_ip("nonexistent.com")
    assert "Domain not found in DNS" in str(context.value)


@patch("dns.resolver.Resolver")
def test_dns_timeout(mock_resolver):
    mock_resolver.return_value.resolve.side_effect = dns.resolver.Timeout
    with pytest.raises(Exception) as context:
        dns_resolve_ip("timeout.com")
    assert "Unable to resolve domain" in str(context.value)
