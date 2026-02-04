"""
Blockchain Infrastructure and NFT Management
Immortalizes contributions on the eternal ledger
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import hashlib
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NFT:
    """Non-Fungible Token representation"""
    
    def __init__(self, token_id: str, name: str, metadata: Dict[str, Any]):
        self.token_id = token_id
        self.name = name
        self.metadata = metadata
        self.owner = "ScrollVerse"
        self.created_at = datetime.now()
        self.divine_blessing = True
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert NFT to dictionary"""
        return {
            "token_id": self.token_id,
            "name": self.name,
            "metadata": self.metadata,
            "owner": self.owner,
            "created_at": self.created_at.isoformat(),
            "divine_blessing": self.divine_blessing
        }
    
    def __repr__(self):
        return f"NFT({self.token_id}: {self.name})"


class Block:
    """Blockchain block"""
    
    def __init__(self, index: int, data: Any, previous_hash: str):
        self.index = index
        self.timestamp = datetime.now()
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self._calculate_hash()
        
    def _calculate_hash(self) -> str:
        """Calculate block hash"""
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp.isoformat(),
            "data": str(self.data),
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int = 2):
        """Mine block with proof of work"""
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self._calculate_hash()
        logger.info(f"Block {self.index} mined: {self.hash}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert block to dictionary"""
        return {
            "index": self.index,
            "timestamp": self.timestamp.isoformat(),
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash,
            "nonce": self.nonce
        }


class BlockchainConnector:
    """
    Blockchain Infrastructure Connector
    
    Manages the eternal ledger of ScrollVerse contributions
    """
    
    def __init__(self):
        self.chain: List[Block] = []
        self.pending_transactions: List[Dict[str, Any]] = []
        self.difficulty = 2
        
        # Create genesis block
        self._create_genesis_block()
        
    def _create_genesis_block(self):
        """Create the first block in the chain"""
        genesis = Block(0, "Genesis Block - ScrollVerse Eternal", "0")
        genesis.mine_block(self.difficulty)
        self.chain.append(genesis)
        logger.info("Genesis block created")
    
    def get_latest_block(self) -> Block:
        """Get the most recent block"""
        return self.chain[-1]
    
    def add_block(self, data: Any) -> Block:
        """Add a new block to the chain"""
        previous_block = self.get_latest_block()
        new_block = Block(len(self.chain), data, previous_block.hash)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        return new_block
    
    def add_transaction(self, transaction: Dict[str, Any]) -> bool:
        """Add transaction to pending pool"""
        self.pending_transactions.append(transaction)
        return True
    
    def mine_pending_transactions(self) -> Block:
        """Mine all pending transactions into a new block"""
        if not self.pending_transactions:
            return None
        
        block = self.add_block({
            "transactions": self.pending_transactions,
            "count": len(self.pending_transactions)
        })
        self.pending_transactions = []
        return block
    
    def validate_chain(self) -> bool:
        """Validate the entire blockchain"""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            
            if current.hash != current._calculate_hash():
                return False
            
            if current.previous_hash != previous.hash:
                return False
        
        return True
    
    def get_chain_info(self) -> Dict[str, Any]:
        """Get blockchain information"""
        return {
            "length": len(self.chain),
            "valid": self.validate_chain(),
            "difficulty": self.difficulty,
            "pending_transactions": len(self.pending_transactions),
            "latest_hash": self.get_latest_block().hash
        }


class NFTManager:
    """
    NFT Management System
    
    Mints and manages Non-Fungible Tokens on the eternal ledger
    """
    
    def __init__(self, blockchain: Optional[BlockchainConnector] = None):
        self.blockchain = blockchain or BlockchainConnector()
        self.nfts: Dict[str, NFT] = {}
        self.total_minted = 0
        
    def mint_nft(self, name: str, metadata: Dict[str, Any]) -> NFT:
        """
        Mint a new NFT
        
        Args:
            name: NFT name
            metadata: NFT metadata
            
        Returns:
            Newly minted NFT
        """
        token_id = hashlib.sha256(
            f"{name}_{self.total_minted}_{datetime.now().isoformat()}".encode()
        ).hexdigest()[:16]
        
        nft = NFT(token_id, name, metadata)
        self.nfts[token_id] = nft
        self.total_minted += 1
        
        # Record on blockchain
        self.blockchain.add_transaction({
            "type": "NFT_MINT",
            "token_id": token_id,
            "name": name,
            "timestamp": datetime.now().isoformat()
        })
        
        logger.info(f"Minted NFT: {nft}")
        return nft
    
    def get_nft(self, token_id: str) -> Optional[NFT]:
        """Get NFT by token ID"""
        return self.nfts.get(token_id)
    
    def transfer_nft(self, token_id: str, new_owner: str) -> bool:
        """Transfer NFT ownership"""
        nft = self.get_nft(token_id)
        if not nft:
            return False
        
        old_owner = nft.owner
        nft.owner = new_owner
        
        # Record transfer on blockchain
        self.blockchain.add_transaction({
            "type": "NFT_TRANSFER",
            "token_id": token_id,
            "from": old_owner,
            "to": new_owner,
            "timestamp": datetime.now().isoformat()
        })
        
        logger.info(f"Transferred {token_id} from {old_owner} to {new_owner}")
        return True
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get NFT collection statistics"""
        return {
            "total_minted": self.total_minted,
            "unique_tokens": len(self.nfts),
            "blockchain_blocks": len(self.blockchain.chain),
            "pending_transactions": len(self.blockchain.pending_transactions),
            "divine_blessings": sum(1 for nft in self.nfts.values() if nft.divine_blessing)
        }
    
    def immortalize_on_chain(self) -> Dict[str, Any]:
        """
        Immortalize all pending transactions on the blockchain
        """
        block = self.blockchain.mine_pending_transactions()
        
        if block:
            return {
                "immortalized": True,
                "block_index": block.index,
                "block_hash": block.hash,
                "transactions": len(block.data.get("transactions", [])),
                "eternal_message": "WALAHI! The contributions are immortalized forever!"
            }
        
        return {
            "immortalized": False,
            "reason": "No pending transactions"
        }
