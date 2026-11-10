import asyncio
from web3 import AsyncWeb3
from web3.providers import AsyncHTTPProvider

# ==============================================================================
# PROJECT:     EVM Block-Level USDC Whale Tracker
# DEVELOPER:   btctrl-labs (https://github.com)
# DESCRIPTION: High-performance asynchronous ERC-20 log monitoring pipeline.
# ==============================================================================

# Global Configuration - Insert your Ethereum RPC Endpoint here (HTTP/HTTPS URL)
RPC_URL = "wss://eth-mainnet.g.alchemy.com/v2/VVk73bYE2YPWu88a8SXa9"

# Official USDC Smart Contract Address on Ethereum Mainnet
USDC_CONTRACT_ADDRESS = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"

# Keccak-256 hash of the ERC-20 Transfer event signature: "Transfer(address,address,uint256)"
TRANSFER_EVENT_TOPIC = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"

# WHALE FILTER THRESHOLD: Minimum USDC amount to be displayed
MIN_TRANSFER_AMOUNT = 100000.0

def print_welcome_status():
    print("=" * 70)
    print("🚀 SYSTEM: EVM Block-Level USDC Whale Tracker v1.0.0")
    print("👨‍💻 ENGINE: Built & Optimized by btctrl-labs")
    print("=" * 70)

async def track_usdc_transfers():
    print_welcome_status()
    print("🔄 Connecting to Ethereum network via RPC... Please wait...")
    
    # Initialize the standardized AsyncHTTPProvider
    w3 = AsyncWeb3(AsyncHTTPProvider(RPC_URL))
    
    if await w3.is_connected():
        print("✅ Successfully connected to the blockchain network!")
    else:
        print("❌ Network connection failed.")
        return

    print(f"📡 Polling active. Monitoring USDC transfers ABOVE {MIN_TRANSFER_AMOUNT:,.2f} USDC per block...\n")
    
    # Fetch the current block number as our starting point
    try:
        last_block_number = await w3.eth.block_number
        print(f"Current network block height: #{last_block_number}")
    except Exception as e:
        print(f"❌ Error fetching initial block height: {e}")
        return

    while True:
        try:
            current_block_number = await w3.eth.block_number
            
            # Trigger when a new block is mined (approx. every 12 seconds)
            if current_block_number > last_block_number:
                last_block_number = current_block_number
                print(f"\n📦 New Block Mined: #{current_block_number}")
                
                # Request logs for the specific USDC contract and the Transfer topic in this block
                log_filter = {
                    "fromBlock": current_block_number,
                    "toBlock": current_block_number,
                    "address": USDC_CONTRACT_ADDRESS,
                    "topics": [TRANSFER_EVENT_TOPIC]
                }
                
                logs = await w3.eth.get_logs(log_filter)
                
                # Process every single USDC transfer log found in the block
                whale_count = 0
                for log in logs:
                    try:
                        # Extract the data field which holds the transfer amount
                        data_hex = log.get("data", "0x0")
                        
                        # Convert hex string or bytes data to integer
                        if isinstance(data_hex, bytes):
                            raw_value = int.from_bytes(data_hex, byteorder="big")
                        else:
                            raw_value = int(data_hex, 16) if data_hex != "0x" else 0
                        
                        # USDC uses 6 decimals (unlike ETH which uses 18 decimals)
                        usdc_amount = raw_value / 10**6
                        
                        # WHALE-FILTER CONDITION: Only proceed if amount is greater than or equal to threshold
                        if usdc_amount >= MIN_TRANSFER_AMOUNT:
                            whale_count += 1
                            
                            # Topics contain: [Event Signature, From Address, To Address]
                            topics = log.get("topics", [])
                            
                            # Extract and format addresses from 32-byte hex strings to standard 20-byte addresses
                            from_addr = "0x" + topics[1].hex()[-40:] if len(topics) > 1 else "Unknown"
                            to_addr = "0x" + topics[2].hex()[-40:] if len(topics) > 2 else "Unknown"
                            
                            tx_hash = log.get("transactionHash").hex()
                            
                            # Output whale transaction details with brand tag
                            print(f"🐋 [btctrl-whale-alert] {usdc_amount:,.2f} USDC transfered!")
                            print(f"   Hash: 0x{tx_hash}")
                            print(f"   From: {from_addr} ➔ To: {to_addr}\n")
                            
                    except Exception as log_error:
                        print(f"⚠ Error parsing individual log entry: {log_error}")
                
                print(f"🔍 Checked {len(logs)} total transfers. Displayed {whale_count} whale movements.")
            
            # Poll every 4 seconds to balance performance and network rate limits
            await asyncio.sleep(4)
            
        except Exception as e:
            print(f"⚠ Temporary network alert during polling: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    try:
        asyncio.run(track_usdc_transfers())
    except KeyboardInterrupt:
        print("\n🛑 Tracker stopped by user.")
