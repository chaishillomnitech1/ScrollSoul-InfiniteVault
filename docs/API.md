# API Documentation

## ScrollSoul-InfiniteVault API Reference

### Multi-Layer Scaling Framework

#### MultiLayerScaler

**Constructor:**
```python
MultiLayerScaler(initial_layers: int = 3)
```

**Methods:**

- `distribute_load(load: int) -> Dict[str, Any]`
  - Distributes load across available scaling layers
  - Returns distribution results with layer information

- `get_status() -> Dict[str, Any]`
  - Returns comprehensive status of all scaling layers
  - Includes metrics, utilization, and layer details

- `optimize() -> Dict[str, Any]`
  - Optimizes load distribution for karmic balance
  - Returns optimization results

---

### Spotify Royalty Harvesting

#### SpotifyRoyaltyHarvester

**Constructor:**
```python
SpotifyRoyaltyHarvester()
```

**Methods:**

- `harvest_stream(artist: str, track: str, streams: int, rate_per_stream: float = 0.003) -> Dict[str, Any]`
  - Harvests a royalty stream
  - Returns harvest results with revenue and karma alignment

- `get_total_royalties() -> float`
  - Returns total harvested royalties

- `get_artist_breakdown() -> Dict[str, float]`
  - Returns royalty breakdown by artist

- `generate_report() -> Dict[str, Any]`
  - Generates comprehensive royalty report

- `align_with_universe() -> Dict[str, Any]`
  - Aligns royalty distribution with universal principles

---

### AI-Driven Recursive Loops

#### RecursiveAIEngine

**Constructor:**
```python
RecursiveAIEngine(max_depth: int = 10)
```

**Methods:**

- `create_recursive_pattern(initial_value: Any, expansion_function: Callable, depth_limit: Optional[int] = None) -> RecursiveNode`
  - Creates a recursive pattern with custom expansion
  - Returns root node of the pattern

- `process_recursive_loop(node: RecursiveNode, processor: Callable) -> Dict[str, Any]`
  - Processes all nodes in a recursive loop
  - Returns processing results with karma metrics

- `fractal_expand(seed_value: Any, iterations: int = 5) -> Dict[str, Any]`
  - Creates fractal expansion pattern
  - Returns expansion results

- `get_engine_status() -> Dict[str, Any]`
  - Returns comprehensive engine status

- `achieve_enlightenment() -> Dict[str, Any]`
  - Achieves recursive enlightenment state
  - Returns enlightenment metrics

---

### NFT & Blockchain Infrastructure

#### BlockchainConnector

**Constructor:**
```python
BlockchainConnector()
```

**Methods:**

- `add_block(data: Any) -> Block`
  - Adds a new block to the chain
  - Returns the created block

- `add_transaction(transaction: Dict[str, Any]) -> bool`
  - Adds transaction to pending pool
  - Returns success status

- `mine_pending_transactions() -> Block`
  - Mines all pending transactions into a new block
  - Returns the mined block

- `validate_chain() -> bool`
  - Validates the entire blockchain
  - Returns validation result

- `get_chain_info() -> Dict[str, Any]`
  - Returns blockchain information

#### NFTManager

**Constructor:**
```python
NFTManager(blockchain: Optional[BlockchainConnector] = None)
```

**Methods:**

- `mint_nft(name: str, metadata: Dict[str, Any]) -> NFT`
  - Mints a new NFT
  - Returns the created NFT

- `get_nft(token_id: str) -> Optional[NFT]`
  - Retrieves NFT by token ID
  - Returns NFT or None

- `transfer_nft(token_id: str, new_owner: str) -> bool`
  - Transfers NFT ownership
  - Returns success status

- `get_collection_stats() -> Dict[str, Any]`
  - Returns NFT collection statistics

- `immortalize_on_chain() -> Dict[str, Any]`
  - Immortalizes pending transactions on blockchain
  - Returns immortalization results

---

### Universal Governance

#### UniversalGovernance

**Constructor:**
```python
UniversalGovernance()
```

**Methods:**

- `create_proposal(title: str, description: str, voting_period_days: int = 7) -> Proposal`
  - Creates a new governance proposal
  - Returns the created proposal

- `cast_vote(proposal_id: str, voter: str, choice: bool, weight: float = 1.0) -> bool`
  - Casts a vote on a proposal
  - Returns success status

- `finalize_proposal(proposal_id: str, threshold: float = 50.0) -> Dict[str, Any]`
  - Finalizes a proposal and determines outcome
  - Returns finalization results

- `execute_proposal(proposal_id: str) -> Dict[str, Any]`
  - Executes a passed proposal
  - Returns execution results

- `get_active_proposals() -> List[Dict[str, Any]]`
  - Returns all active proposals

- `get_governance_stats() -> Dict[str, Any]`
  - Returns comprehensive governance statistics

- `align_with_cosmic_will() -> Dict[str, Any]`
  - Aligns governance with cosmic principles
  - Returns alignment metrics
