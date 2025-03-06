import ipaddress
import logging
import os
from typing import Optional

import dns.resolver
from flask import abort
from urllib3.util import parse_url


def is_valid_ip(ip: str) -> bool:
    try:
        ip_obj = ipaddress.IPv4Address(ip)
        if ip_obj.is_private:
            return False
        return True
    except ipaddress.AddressValueError:
        return False
    except ipaddress.NetmaskValueError:
        return False


def is_valid_url(url: str) -> Optional[bool]:
    try:
        parsed = parse_url(url)
        return bool(parsed.host)
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        abort(400, description="Invalid URL provided")


def dns_resolve_ip(domain: str) -> str:
    is_valid_url(domain)
    domain = domain.replace("https://", "").replace("http://", "")
    resolver = dns.resolver.Resolver()
    resolver.nameservers = os.getenv("DNS_SERVERS", "8.8.8.8").split(",")
    try:
        answer = resolver.resolve(domain, "A")
        if answer:
            return str(answer[0])
        else:
            abort(404, description="No A record found for domain")
    except dns.resolver.NXDOMAIN:
        abort(404, description="Domain not found in DNS")
    except dns.resolver.NoAnswer:
        abort(404, description="No A record found for domain")
    except dns.resolver.NoNameservers:
        abort(500, description="Unable to resolve domain")
    except dns.resolver.Timeout:
        abort(500, description="Unable to resolve domain")
