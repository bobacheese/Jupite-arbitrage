#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║                                                                           ║
# ║     ██╗██╗   ██╗██████╗ ██╗████████╗███████╗██████╗                       ║
# ║     ██║██║   ██║██╔══██╗██║╚══██╔══╝██╔════╝██╔══██╗                      ║
# ║     ██║██║   ██║██████╔╝██║   ██║   █████╗  ██████╔╝                      ║
# ║     ██║██║   ██║██╔══██╗██║   ██║   ██╔══╝  ██╔══██╗                      ║
# ║     ██║╚██████╔╝██████╔╝██║   ██║   ███████╗██║  ██║                      ║
# ║     ╚═╝ ╚═════╝ ╚═════╝ ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝                      ║
# ║                                                                           ║
# ║     █████╗ ██████╗ ██████╗ ██╗████████╗██████╗  █████╗  ██████╗ ███████╗  ║
# ║    ██╔══██╗██╔══██╗██╔══██╗██║╚══██╔══╝██╔══██╗██╔══██╗██╔════╝ ██╔════╝  ║
# ║    ███████║██████╔╝██████╔╝██║   ██║   ██████╔╝███████║██║  ███╗█████╗    ║
# ║    ██╔══██║██╔══██╗██╔══██╗██║   ██║   ██╔══██╗██╔══██║██║   ██║██╔══╝    ║
# ║    ██║  ██║██║  ██║██║  ██║██║   ██║   ██║  ██║██║  ██║╚██████╔╝███████╗  ║
# ║    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝  ║
# ║                                                                           ║
# ║                    M O N I T O R   A R B I T R A G E                      ║
# ║                         S O L A N A  x  J U P I T E R                     ║
# ║                                                                           ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
#
# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  ⚡ DEVELOPER PROFILE ⚡                                                   ║
# ║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ║
# ║  👤 Creator    : AMARULLOH ZIKRI                                          ║
# ║  🐙 GitHub     : https://github.com/bobacheese                           ║
# ║  📺 YouTube    : https://youtube.com/@bobacheese?si=5M2leEilS3_VmNS6     ║
# ║  ☕ Coffee     : coff.ee/amarullohzd                                      ║
# ║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ║
# ║  🌌 "Scanning the Solana multiverse for alpha opportunities..."           ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

"""
Jupiter Arbitrage Monitor v1.0.0
=================================
A lightweight, Termux-optimized triangular arbitrage scanner for Solana.
Uses Jupiter Aggregator API v6 for real-time price discovery.

READ-ONLY MONITOR - NO WALLET CONNECTION REQUIRED
This script only monitors and displays potential arbitrage opportunities.
No private keys, no transactions, no risk.

Requirements:
    - Python 3.8+
    - aiohttp (async HTTP client)
    - Termux (Android)

Installation:
    pkg install python
    pip install aiohttp
    python jupiter_arbitrage_monitor.py
"""

import asyncio
import aiohttp
import json
import time
import sys
import os
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

# ═════════════════════════════════════════════════════════════════════════════
# CONFIGURATION & CONSTANTS
# ═════════════════════════════════════════════════════════════════════════════

class Config:
    """Configuration constants optimized for Termux environment."""
    
    # Jupiter API v6 Endpoints
    JUPITER_QUOTE_API = "https://quote-api.jup.ag/v6/quote"
    JUPITER_PRICE_API = "https://price.jup.ag/v4/price"
    
    # Request settings (Termux-friendly)
    TIMEOUT = 15  # seconds
    MAX_RETRIES = 3
    RETRY_DELAY = 1.0  # seconds
    
    # Rate limiting
    REQUESTS_PER_SECOND = 2
    MIN_CYCLE_INTERVAL = 5.0  # seconds between scan cycles
    
    # Arbitrage thresholds
    MIN_PROFIT_PERCENT = 0.1  # Minimum profit to display (0.1%)
    MAX_PROFIT_DISPLAY = 1000.0  # Cap for display purposes
    
    # UI Settings
    TERMINAL_WIDTH = 80
    COLOR_ENABLED = True


class TokenAddresses:
    """Popular Solana token mint addresses for arbitrage routes."""
    
    SOL = "So11111111111111111111111111111111111111112"
    USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
    USDT = "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"
    BONK = "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"
    JUP = "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN"
    RAY = "4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R"
    ORCA = "orcaEKTdK7LKz57vaAYr9QeNsVEPfiu6QeMU1kektZE"
    MSOL = "mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So"
    BSOL = "bSo13r4TkiE4xumBoiwQmtmrfz6bW1pHXkL8TDKDffUS"
    
    # Token symbols mapping
    SYMBOLS = {
        SOL: "SOL",
        USDC: "USDC",
        USDT: "USDT",
        BONK: "BONK",
        JUP: "JUP",
        RAY: "RAY",
        ORCA: "ORCA",
        MSOL: "mSOL",
        BSOL: "bSOL"
    }


class Colors:
    """ANSI color codes for terminal output."""
    
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    
    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Bright colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    
    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"


# ═════════════════════════════════════════════════════════════════════════════
# DATA CLASSES
# ═════════════════════════════════════════════════════════════════════════════

@dataclass
class QuoteResult:
    """Result from a single Jupiter quote request."""
    input_mint: str
    output_mint: str
    input_amount: int
    output_amount: int
    price_impact_pct: float
    route_found: bool
    error: Optional[str] = None
    
    @property
    def rate(self) -> float:
        """Calculate exchange rate."""
        if self.input_amount == 0 or not self.route_found:
            return 0.0
        return self.output_amount / self.input_amount


@dataclass
class ArbitrageRoute:
    """A triangular arbitrage route: A -> B -> C -> A"""
    token_a: str
    token_b: str
    token_c: str
    
    @property
    def symbols(self) -> Tuple[str, str, str]:
        """Get token symbols for display."""
        return (
            TokenAddresses.SYMBOLS.get(self.token_a, self.token_a[:4]),
            TokenAddresses.SYMBOLS.get(self.token_b, self.token_b[:4]),
            TokenAddresses.SYMBOLS.get(self.token_c, self.token_c[:4])
        )
    
    @property
    def name(self) -> str:
        """Get route name."""
        a, b, c = self.symbols
        return f"{a} → {b} → {c} → {a}"


@dataclass
class ArbitrageOpportunity:
    """Detected arbitrage opportunity with profit calculation."""
    route: ArbitrageRoute
    start_amount: int
    final_amount: int
    profit_percent: float
    timestamp: datetime
    details: Dict[str, Any]
    
    @property
    def is_profitable(self) -> bool:
        return self.profit_percent > 0


# ═════════════════════════════════════════════════════════════════════════════
# JUPITER API CLIENT
# ═════════════════════════════════════════════════════════════════════════════

class JupiterClient:
    """Async client for Jupiter Aggregator API v6."""
    
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.last_request_time = 0.0
        self.request_count = 0
        self.error_count = 0
        
    async def __aenter__(self):
        """Async context manager entry."""
        timeout = aiohttp.ClientTimeout(total=Config.TIMEOUT)
        connector = aiohttp.TCPConnector(
            limit=10,
            limit_per_host=5,
            enable_cleanup_closed=True,
            force_close=True
        )
        self.session = aiohttp.ClientSession(
            timeout=timeout,
            connector=connector,
            headers={
                "Accept": "application/json",
                "User-Agent": "JupiterArbitrageMonitor/1.0.0"
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def _rate_limit(self):
        """Implement rate limiting between requests."""
        min_interval = 1.0 / Config.REQUESTS_PER_SECOND
        elapsed = time.time() - self.last_request_time
        if elapsed < min_interval:
            await asyncio.sleep(min_interval - elapsed)
        self.last_request_time = time.time()
    
    async def get_quote(
        self,
        input_mint: str,
        output_mint: str,
        amount: int,
        slippage_bps: int = 50,
        retry_count: int = 0
    ) -> QuoteResult:
        """
        Fetch quote from Jupiter API v6.
        
        Args:
            input_mint: Input token mint address
            output_mint: Output token mint address
            amount: Input amount in smallest unit (lamports for SOL)
            slippage_bps: Slippage tolerance in basis points
            retry_count: Current retry attempt
            
        Returns:
            QuoteResult with exchange rate data
        """
        await self._rate_limit()
        
        params = {
            "inputMint": input_mint,
            "outputMint": output_mint,
            "amount": str(amount),
            "slippageBps": str(slippage_bps),
            "onlyDirectRoutes": "false",
            "asLegacyTransaction": "false"
        }
        
        try:
            if not self.session:
                raise RuntimeError("Session not initialized")
            
            async with self.session.get(
                Config.JUPITER_QUOTE_API,
                params=params
            ) as response:
                
                # Handle rate limiting
                if response.status == 429:
                    if retry_count < Config.MAX_RETRIES:
                        wait_time = (retry_count + 1) * Config.RETRY_DELAY * 2
                        await asyncio.sleep(wait_time)
                        return await self.get_quote(
                            input_mint, output_mint, amount,
                            slippage_bps, retry_count + 1
                        )
                    return QuoteResult(
                        input_mint=input_mint,
                        output_mint=output_mint,
                        input_amount=amount,
                        output_amount=0,
                        price_impact_pct=0.0,
                        route_found=False,
                        error="Rate limited (HTTP 429)"
                    )
                
                # Handle timeout
                if response.status == 408 or response.status == 504:
                    if retry_count < Config.MAX_RETRIES:
                        await asyncio.sleep(Config.RETRY_DELAY)
                        return await self.get_quote(
                            input_mint, output_mint, amount,
                            slippage_bps, retry_count + 1
                        )
                
                # Handle server errors
                if response.status >= 500:
                    if retry_count < Config.MAX_RETRIES:
                        await asyncio.sleep(Config.RETRY_DELAY * (retry_count + 1))
                        return await self.get_quote(
                            input_mint, output_mint, amount,
                            slippage_bps, retry_count + 1
                        )
                    return QuoteResult(
                        input_mint=input_mint,
                        output_mint=output_mint,
                        input_amount=amount,
                        output_amount=0,
                        price_impact_pct=0.0,
                        route_found=False,
                        error=f"Server error (HTTP {response.status})"
                    )
                
                # Handle other errors
                if response.status != 200:
                    return QuoteResult(
                        input_mint=input_mint,
                        output_mint=output_mint,
                        input_amount=amount,
                        output_amount=0,
                        price_impact_pct=0.0,
                        route_found=False,
                        error=f"HTTP {response.status}"
                    )
                
                # Parse JSON response
                try:
                    data = await response.json()
                except (json.JSONDecodeError, aiohttp.ContentTypeError) as e:
                    self.error_count += 1
                    return QuoteResult(
                        input_mint=input_mint,
                        output_mint=output_mint,
                        input_amount=amount,
                        output_amount=0,
                        price_impact_pct=0.0,
                        route_found=False,
                        error=f"Invalid JSON: {str(e)}"
                    )
                
                # Check for API error response
                if "error" in data:
                    return QuoteResult(
                        input_mint=input_mint,
                        output_mint=output_mint,
                        input_amount=amount,
                        output_amount=0,
                        price_impact_pct=0.0,
                        route_found=False,
                        error=data.get("error", "Unknown API error")
                    )
                
                # Extract quote data
                route_found = data.get("routePlan") is not None or data.get("outAmount") is not None
                
                if not route_found:
                    return QuoteResult(
                        input_mint=input_mint,
                        output_mint=output_mint,
                        input_amount=amount,
                        output_amount=0,
                        price_impact_pct=0.0,
                        route_found=False,
                        error="No route found"
                    )
                
                output_amount = int(data.get("outAmount", 0))
                price_impact = float(data.get("priceImpactPct", 0))
                
                self.request_count += 1
                
                return QuoteResult(
                    input_mint=input_mint,
                    output_mint=output_mint,
                    input_amount=amount,
                    output_amount=output_amount,
                    price_impact_pct=price_impact,
                    route_found=True
                )
                
        except asyncio.TimeoutError:
            if retry_count < Config.MAX_RETRIES:
                await asyncio.sleep(Config.RETRY_DELAY)
                return await self.get_quote(
                    input_mint, output_mint, amount,
                    slippage_bps, retry_count + 1
                )
            self.error_count += 1
            return QuoteResult(
                input_mint=input_mint,
                output_mint=output_mint,
                input_amount=amount,
                output_amount=0,
                price_impact_pct=0.0,
                route_found=False,
                error="Request timeout"
            )
            
        except aiohttp.ClientError as e:
            if retry_count < Config.MAX_RETRIES:
                await asyncio.sleep(Config.RETRY_DELAY)
                return await self.get_quote(
                    input_mint, output_mint, amount,
                    slippage_bps, retry_count + 1
                )
            self.error_count += 1
            return QuoteResult(
                input_mint=input_mint,
                output_mint=output_mint,
                input_amount=amount,
                output_amount=0,
                price_impact_pct=0.0,
                route_found=False,
                error=f"Connection error: {str(e)}"
            )
            
        except Exception as e:
            self.error_count += 1
            return QuoteResult(
                input_mint=input_mint,
                output_mint=output_mint,
                input_amount=amount,
                output_amount=0,
                price_impact_pct=0.0,
                route_found=False,
                error=f"Unexpected error: {str(e)}"
            )


# ═════════════════════════════════════════════════════════════════════════════
# ARBITRAGE SCANNER
# ═════════════════════════════════════════════════════════════════════════════

class ArbitrageScanner:
    """Scanner for triangular arbitrage opportunities."""
    
    def __init__(self, client: JupiterClient):
        self.client = client
        self.routes: List[ArbitrageRoute] = []
        self._setup_routes()
    
    def _setup_routes(self):
        """Define triangular arbitrage routes to monitor."""
        tokens = [
            TokenAddresses.SOL,
            TokenAddresses.USDC,
            TokenAddresses.USDT,
            TokenAddresses.JUP,
            TokenAddresses.BONK,
        ]
        
        # Generate triangular routes: A -> B -> C -> A
        for i, a in enumerate(tokens):
            for j, b in enumerate(tokens):
                if i == j:
                    continue
                for k, c in enumerate(tokens):
                    if i == k or j == k:
                        continue
                    # Limit to interesting routes involving SOL or stablecoins
                    if a == TokenAddresses.SOL or b in [TokenAddresses.USDC, TokenAddresses.USDT]:
                        route = ArbitrageRoute(token_a=a, token_b=b, token_c=c)
                        self.routes.append(route)
        
        # Limit total routes for Termux performance
        self.routes = self.routes[:15]
    
    async def scan_route(
        self,
        route: ArbitrageRoute,
        start_amount: int = 1_000_000_000  # 1 SOL in lamports
    ) -> Optional[ArbitrageOpportunity]:
        """
        Scan a single triangular arbitrage route.
        
        Args:
            route: The arbitrage route to scan
            start_amount: Starting amount in smallest unit
            
        Returns:
            ArbitrageOpportunity if scan completes, None on failure
        """
        try:
            # Step 1: A -> B
            quote1 = await self.client.get_quote(
                route.token_a, route.token_b, start_amount
            )
            if not quote1.route_found:
                return None
            
            # Step 2: B -> C
            quote2 = await self.client.get_quote(
                route.token_b, route.token_c, quote1.output_amount
            )
            if not quote2.route_found:
                return None
            
            # Step 3: C -> A
            quote3 = await self.client.get_quote(
                route.token_c, route.token_a, quote2.output_amount
            )
            if not quote3.route_found:
                return None
            
            # Calculate profit
            final_amount = quote3.output_amount
            profit = final_amount - start_amount
            profit_percent = (profit / start_amount) * 100
            
            return ArbitrageOpportunity(
                route=route,
                start_amount=start_amount,
                final_amount=final_amount,
                profit_percent=profit_percent,
                timestamp=datetime.now(),
                details={
                    "step1_rate": quote1.rate,
                    "step2_rate": quote2.rate,
                    "step3_rate": quote3.rate,
                    "step1_impact": quote1.price_impact_pct,
                    "step2_impact": quote2.price_impact_pct,
                    "step3_impact": quote3.price_impact_pct,
                }
            )
            
        except Exception as e:
            return None
    
    async def scan_all_routes(
        self,
        start_amount: int = 1_000_000_000
    ) -> List[ArbitrageOpportunity]:
        """
        Scan all configured routes concurrently.
        
        Args:
            start_amount: Starting amount for each route
            
        Returns:
            List of successful arbitrage opportunities
        """
        tasks = [
            self.scan_route(route, start_amount)
            for route in self.routes
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        opportunities = []
        for result in results:
            if isinstance(result, ArbitrageOpportunity):
                opportunities.append(result)
        
        return opportunities


# ═════════════════════════════════════════════════════════════════════════════
# UI DISPLAY
# ═════════════════════════════════════════════════════════════════════════════

class Display:
    """Terminal display manager with cyberpunk aesthetics."""
    
    def __init__(self):
        self.colors_enabled = Config.COLOR_ENABLED and self._supports_color()
        self.scan_count = 0
        self.start_time = time.time()
    
    def _supports_color(self) -> bool:
        """Check if terminal supports ANSI colors."""
        if os.environ.get("NO_COLOR"):
            return False
        if os.environ.get("TERM") in ("dumb", ""):
            return False
        return sys.stdout.isatty()
    
    def _color(self, color_code: str, text: str) -> str:
        """Apply color to text if enabled."""
        if self.colors_enabled:
            return f"{color_code}{text}{Colors.RESET}"
        return text
    
    def clear_screen(self):
        """Clear terminal screen."""
        if sys.stdout.isatty():
            os.system("clear" if os.name == "posix" else "cls")
    
    def print_header(self):
        """Print animated header."""
        header = f"""
{self._color(Colors.CYAN, "╔══════════════════════════════════════════════════════════════════════╗")}
{self._color(Colors.CYAN, "║")}  {self._color(Colors.BRIGHT_CYAN, "⚡ JUPITER ARBITRAGE MONITOR v1.0.0")}                                {self._color(Colors.CYAN, "║")}
{self._color(Colors.CYAN, "║")}  {self._color(Colors.DIM, "Solana Triangular Arbitrage Scanner")}                                  {self._color(Colors.CYAN, "║")}
{self._color(Colors.CYAN, "║")}  {self._color(Colors.BRIGHT_BLACK, "READ-ONLY MONITOR • NO WALLET REQUIRED")}                             {self._color(Colors.CYAN, "║")}
{self._color(Colors.CYAN, "╚══════════════════════════════════════════════════════════════════════╝")}
"""
        print(header)
    
    def print_status_bar(self, client: JupiterClient):
        """Print status bar with stats."""
        uptime = int(time.time() - self.start_time)
        uptime_str = f"{uptime // 3600:02d}:{(uptime % 3600) // 60:02d}:{uptime % 60:02d}"
        
        status = f"""
{self._color(Colors.BRIGHT_BLACK, "┌─────────────────────────────────────────────────────────────────────┐")}
{self._color(Colors.BRIGHT_BLACK, "│")} {self._color(Colors.CYAN, "📊 Scans:")} {self._color(Colors.WHITE, str(self.scan_count)):<6} {self._color(Colors.CYAN, "🌐 Requests:")} {self._color(Colors.WHITE, str(client.request_count)):<6} {self._color(Colors.CYAN, "⚠️  Errors:")} {self._color(Colors.YELLOW if client.error_count > 0 else Colors.WHITE, str(client.error_count)):<6} {self._color(Colors.CYAN, "⏱️  Uptime:")} {self._color(Colors.WHITE, uptime_str):<8} {self._color(Colors.BRIGHT_BLACK, "│")}
{self._color(Colors.BRIGHT_BLACK, "└─────────────────────────────────────────────────────────────────────┘")}
"""
        print(status)
    
    def print_opportunity(self, opp: ArbitrageOpportunity, rank: int = 1):
        """Print a single arbitrage opportunity."""
        a, b, c = opp.route.symbols
        
        # Color based on profitability
        if opp.profit_percent >= 1.0:
            profit_color = Colors.BRIGHT_GREEN
            icon = "🚀"
        elif opp.profit_percent >= 0.5:
            profit_color = Colors.GREEN
            icon = "📈"
        elif opp.profit_percent > 0:
            profit_color = Colors.YELLOW
            icon = "🟡"
        else:
            profit_color = Colors.RED
            icon = "📉"
        
        # Format profit string
        profit_str = f"{opp.profit_percent:+.4f}%"
        
        # Build route visualization
        route_line = f"{self._color(Colors.CYAN, a)} → {self._color(Colors.MAGENTA, b)} → {self._color(Colors.MAGENTA, c)} → {self._color(Colors.CYAN, a)}"
        
        box = f"""
{self._color(Colors.BRIGHT_BLACK, "┌─────────────────────────────────────────────────────────────────────┐")}
{self._color(Colors.BRIGHT_BLACK, "│")} {icon} {self._color(Colors.WHITE, f"Route #{rank}"):<8} {route_line:<45} {self._color(Colors.BRIGHT_BLACK, "│")}
{self._color(Colors.BRIGHT_BLACK, "│")}    {self._color(Colors.DIM, "Profit:")} {self._color(profit_color, profit_str):<15} {self._color(Colors.DIM, "Time:")} {self._color(Colors.WHITE, opp.timestamp.strftime('%H:%M:%S')):<20} {self._color(Colors.BRIGHT_BLACK, "│")}
{self._color(Colors.BRIGHT_BLACK, "└─────────────────────────────────────────────────────────────────────┘")}
"""
        print(box)
    
    def print_no_opportunities(self):
        """Print message when no opportunities found."""
        msg = f"""
{self._color(Colors.BRIGHT_BLACK, "┌─────────────────────────────────────────────────────────────────────┐")}
{self._color(Colors.BRIGHT_BLACK, "│")} {self._color(Colors.YELLOW, "⚠️  No profitable opportunities detected in this scan cycle")}          {self._color(Colors.BRIGHT_BLACK, "│")}
{self._color(Colors.BRIGHT_BLACK, "│")} {self._color(Colors.DIM, "   The market is efficient... for now.")}                                {self._color(Colors.BRIGHT_BLACK, "│")}
{self._color(Colors.BRIGHT_BLACK, "└─────────────────────────────────────────────────────────────────────┘")}
"""
        print(msg)
    
    def print_error(self, error_msg: str):
        """Print error message."""
        msg = f"""
{self._color(Colors.BRIGHT_BLACK, "┌─────────────────────────────────────────────────────────────────────┐")}
{self._color(Colors.BRIGHT_BLACK, "│")} {self._color(Colors.RED, "❌ ERROR:")} {self._color(Colors.WHITE, error_msg):<56} {self._color(Colors.BRIGHT_BLACK, "│")}
{self._color(Colors.BRIGHT_BLACK, "└─────────────────────────────────────────────────────────────────────┘")}
"""
        print(msg)
    
    def print_footer(self):
        """Print footer with controls."""
        footer = f"""
{self._color(Colors.BRIGHT_BLACK, "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")}
{self._color(Colors.DIM, "  Press Ctrl+C to exit • Scanning continuously...")}
{self._color(Colors.BRIGHT_BLACK, "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")}
"""
        print(footer)
    
    def print_scan_start(self):
        """Print scan start indicator."""
        self.scan_count += 1
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"\n{self._color(Colors.CYAN, '▶')} {self._color(Colors.WHITE, f'Scan #{self.scan_count}')} {self._color(Colors.DIM, f'at {timestamp}')}")
        print(self._color(Colors.BRIGHT_BLACK, "─" * 71))


# ═════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ═════════════════════════════════════════════════════════════════════════════

async def main():
    """Main application entry point."""
    display = Display()
    
    try:
        async with JupiterClient() as client:
            scanner = ArbitrageScanner(client)
            
            while True:
                try:
                    display.clear_screen()
                    display.print_header()
                    display.print_status_bar(client)
                    display.print_scan_start()
                    
                    # Scan all routes
                    opportunities = await scanner.scan_all_routes()
                    
                    # Filter and sort opportunities
                    valid_opportunities = [
                        opp for opp in opportunities
                        if opp is not None
                    ]
                    
                    # Sort by profit (highest first)
                    valid_opportunities.sort(
                        key=lambda x: x.profit_percent,
                        reverse=True
                    )
                    
                    # Display results
                    if valid_opportunities:
                        profitable = [
                            opp for opp in valid_opportunities
                            if opp.profit_percent >= Config.MIN_PROFIT_PERCENT
                        ]
                        
                        if profitable:
                            print(f"\n{display._color(Colors.GREEN, '💎 Found profitable opportunities!')}\n")
                            for i, opp in enumerate(profitable[:5], 1):
                                display.print_opportunity(opp, i)
                        else:
                            # Show top 3 even if not profitable
                            print(f"\n{display._color(Colors.YELLOW, '📊 Top routes (no significant profit):')}\n")
                            for i, opp in enumerate(valid_opportunities[:3], 1):
                                display.print_opportunity(opp, i)
                    else:
                        display.print_no_opportunities()
                    
                    display.print_footer()
                    
                    # Wait before next scan
                    await asyncio.sleep(Config.MIN_CYCLE_INTERVAL)
                    
                except asyncio.CancelledError:
                    raise
                except Exception as e:
                    display.print_error(str(e))
                    await asyncio.sleep(Config.MIN_CYCLE_INTERVAL)
                    
    except KeyboardInterrupt:
        print(f"\n\n{display._color(Colors.CYAN, '👋 Goodbye! Stay profitable.')}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{display._color(Colors.RED, f'Fatal error: {e}')}")
        sys.exit(1)


if __name__ == "__main__":
    # Check Python version
    if sys.version_info < (3, 8):
        print("Error: Python 3.8+ required")
        sys.exit(1)
    
    # Run main loop
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nMonitor stopped. See you in the multiverse!")
        sys.exit(0)
