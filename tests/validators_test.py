from validators import is_valid_ip, dns_resolve_ip, is_valid_url
from unittest.mock import patch, MagicMock
import dns.resolver


def test_valid_ip():
    assert is_valid_ip("81.41.222.0") == True
    assert is_valid_ip("127.0.0.1") == False
    assert is_valid_ip("hellothere") == False
    assert is_valid_ip("-1.0.2.3") == False
    assert is_valid_ip("0.0.0.0") == False
    assert is_valid_ip("255.255.255.255") == False
    assert is_valid_ip("") == False
    assert is_valid_ip(" 192.168.0.1 ") == False


def test_valid_url():
    assert is_valid_url("http://example.com") == True
    assert is_valid_url("google.com") == True
    assert is_valid_url("http://") == False


@patch("dns.resolver.Resolver.resolve")
@patch("dns.resolver.Resolver")
@patch("os.getenv", return_value="8.8.8.8")
def test_valid_domain(self, mock_getenv, mock_resolver, mock_resolve):
    mock_resolver_instance = mock_resolver.return_value
    mock_resolve.return_value = [MagicMock(to_text=lambda: "93.184.216.34")]

    result = dns_resolve_ip("example.com")
    self.assertEqual(result, "93.184.216.34")


@patch("dns.resolver.Resolver.resolve", side_effect=dns.resolver.NXDOMAIN)
@patch("dns.resolver.Resolver")
def test_domain_not_found(self, mock_resolver, mock_resolve):
    with self.assertRaises(Exception) as context:
        dns_resolve_ip("nonexistent.com")
    self.assertEqual(context.exception.description, "Domain not found in DNS")


@patch("dns.resolver.Resolver.resolve", side_effect=dns.resolver.NoAnswer)
@patch("dns.resolver.Resolver")
def test_no_a_record(self, mock_resolver, mock_resolve):
    with self.assertRaises(Exception) as context:
        dns_resolve_ip("no-a-record.com")
    self.assertEqual(context.exception.description, "No A record found for domain")


@patch("dns.resolver.Resolver.resolve", side_effect=dns.resolver.NoNameservers)
@patch("dns.resolver.Resolver")
def test_no_nameservers(self, mock_resolver, mock_resolve):
    with self.assertRaises(Exception) as context:
        dns_resolve_ip("bad-nameservers.com")
    self.assertEqual(context.exception.description, "Unable to resolve domain")


@patch("dns.resolver.Resolver.resolve", side_effect=dns.resolver.Timeout)
@patch("dns.resolver.Resolver")
def test_dns_timeout(self, mock_resolver, mock_resolve):
    with self.assertRaises(Exception) as context:
        dns_resolve_ip("timeout.com")
    self.assertEqual(context.exception.description, "Unable to resolve domain")
