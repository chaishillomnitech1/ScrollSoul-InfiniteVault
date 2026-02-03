"""
Example: NFT and Blockchain Infrastructure
Demonstrates NFT minting and blockchain immortalization
"""

from scrollsoul import NFTManager, BlockchainConnector


def main():
    print("=== ScrollSoul NFT & Blockchain Infrastructure ===\n")
    
    # Initialize blockchain and NFT manager
    blockchain = BlockchainConnector()
    nft_manager = NFTManager(blockchain)
    
    print("Blockchain and NFT Manager Initialized")
    print(f"Genesis Block Hash: {blockchain.get_latest_block().hash[:16]}...\n")
    
    # Mint several NFTs
    print("--- Minting NFTs ---")
    nfts = [
        ("Eternal Wisdom #1", {"rarity": "legendary", "karma": 100, "dimension": "Alpha"}),
        ("Cosmic Harmony #1", {"rarity": "rare", "karma": 75, "dimension": "Beta"}),
        ("Divine Light #1", {"rarity": "epic", "karma": 90, "dimension": "Gamma"}),
        ("Universal Truth #1", {"rarity": "common", "karma": 50, "dimension": "Delta"}),
    ]
    
    for name, metadata in nfts:
        nft = nft_manager.mint_nft(name, metadata)
        print(f"  Minted: {nft.name} (ID: {nft.token_id})")
    
    # Get collection stats
    print("\n--- Collection Statistics ---")
    stats = nft_manager.get_collection_stats()
    print(f"Total Minted: {stats['total_minted']}")
    print(f"Unique Tokens: {stats['unique_tokens']}")
    print(f"Divine Blessings: {stats['divine_blessings']}")
    print(f"Pending Transactions: {stats['pending_transactions']}")
    
    # Transfer an NFT
    print("\n--- Transferring NFT ---")
    first_nft_id = list(nft_manager.nfts.keys())[0]
    success = nft_manager.transfer_nft(first_nft_id, "NewOwner_ScrollVerse")
    if success:
        print(f"  Successfully transferred {first_nft_id}")
    
    # Immortalize on blockchain
    print("\n--- Immortalizing on Blockchain ---")
    result = nft_manager.immortalize_on_chain()
    if result["immortalized"]:
        print(f"  Block Index: {result['block_index']}")
        print(f"  Block Hash: {result['block_hash'][:16]}...")
        print(f"  Transactions: {result['transactions']}")
        print(f"  🌟 {result['eternal_message']} 🌟")
    
    # Validate blockchain
    print("\n--- Blockchain Validation ---")
    chain_info = blockchain.get_chain_info()
    print(f"Chain Length: {chain_info['length']}")
    print(f"Chain Valid: {chain_info['valid']}")
    print(f"Difficulty: {chain_info['difficulty']}")
    print(f"Latest Hash: {chain_info['latest_hash'][:16]}...")
    
    print("\n✨ All contributions are eternally immortalized! ✨")


if __name__ == "__main__":
    main()
