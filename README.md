# EVM Block-Level USDC Whale Tracker 🐋

A high-performance, asynchronous Python script designed to monitor the Ethereum blockchain in real-time. It intercepts every single block's log emissions, filters ERC-20 event signatures, and isolates high-value USDC (Stablecoin) movements exceeding \$100,000 USD.

Built with an architecture that avoids fragile WebSocket connections by using a robust, production-grade JSON-RPC HTTP polling mechanism compatible with any network provider (Alchemy, Infura, QuickNode, or local nodes).

## Features
- **Asynchronous Execution:** Built on top of Python's `asyncio` and `web3.py` (v6+) for non-blocking I/O.
- **Low-Level Log Parsing:** Instead of requesting full block traces, it requests specific logs filtered by the official ERC-20 `Transfer` topic hash (`0xddf2...`), significantly saving infrastructure credits.
- **Whale Filtering:** Skips retail traffic and only alerts on whale movements (\$100k+).
- **Network Agnostic:** Completely neutral configuration. Works with any standard EVM RPC URL.

## Technical Architecture
- **Language:** Python 3.10+
- **Core Libraries:** `web3`, `asyncio`, `aiohttp`
- **Data Decoding:** Converts raw 32-byte hex topics into standard 20-byte EVM addresses and handles decimal conversions for standard ERC-20 token spaces (6 decimals for USDC).

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd evm-usdc-whale-tracker
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   source .venv/bin/activate  # On Linux/macOS
   ```

3. **Install dependencies:**
   ```bash
   pip install --only-binary=:all: web3
   ```

4. **Configuration:**
   Open `mempool_tracker.py` and ensure the `RPC_URL` value is set to your personal EVM node endpoint.

5. **Run the tracker:**
   ```bash
   python mempool_tracker.py
   ```

## Production Sample Output
```text
🔄 Connecting to Ethereum network via RPC... Please wait...
✅ Successfully connected to the blockchain network!
📡 Polling active. Monitoring USDC transfers ABOVE 100,000.00 USDC per block...

📦 New Block Mined: #26383236
🐋 [btctrl-whale-alert] 1,885,663.74 USDC transfered!
   Hash: 0x794...
   From: 0x6fa... -> To: 0xb9f...

🔍 Checked 64 total transfers. Displayed 1 whale movements.
```

