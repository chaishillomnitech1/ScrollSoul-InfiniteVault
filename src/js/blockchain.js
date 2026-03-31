/**
 * src/js/blockchain.js
 * ScrollSoul-InfiniteVault — Blockchain & NFT Infrastructure (JavaScript)
 *
 * Proof-of-work blockchain with NFT minting, transfer, and automatic
 * GoHighLevel contact immortalization for every NFT owner.
 */

'use strict';

const crypto = require('crypto');

// ── Block ─────────────────────────────────────────────────────────────────────

class Block {
  constructor(index, data, previousHash) {
    this.index = index;
    this.timestamp = new Date().toISOString();
    this.data = data;
    this.previousHash = previousHash;
    this.nonce = 0;
    this.hash = this._calculateHash();
  }

  _calculateHash() {
    const content = JSON.stringify({
      index: this.index,
      timestamp: this.timestamp,
      data: String(this.data),
      previousHash: this.previousHash,
      nonce: this.nonce,
    });
    return crypto.createHash('sha256').update(content).digest('hex');
  }

  mine(difficulty = 2) {
    const target = '0'.repeat(difficulty);
    while (!this.hash.startsWith(target)) {
      this.nonce++;
      this.hash = this._calculateHash();
    }
    return this;
  }

  toJSON() {
    return {
      index: this.index,
      timestamp: this.timestamp,
      data: this.data,
      previousHash: this.previousHash,
      hash: this.hash,
      nonce: this.nonce,
    };
  }
}

// ── BlockchainConnector ───────────────────────────────────────────────────────

class BlockchainConnector {
  constructor({ difficulty = 2, genesisMessage = 'Genesis Block — ScrollVerse Eternal' } = {}) {
    this.chain = [];
    this.pendingTransactions = [];
    this.difficulty = difficulty;
    this._createGenesisBlock(genesisMessage);
  }

  _createGenesisBlock(message) {
    const genesis = new Block(0, message, '0').mine(this.difficulty);
    this.chain.push(genesis);
  }

  getLatestBlock() { return this.chain[this.chain.length - 1]; }

  addBlock(data) {
    const block = new Block(this.chain.length, data, this.getLatestBlock().hash).mine(this.difficulty);
    this.chain.push(block);
    return block;
  }

  addTransaction(tx) {
    this.pendingTransactions.push({ ...tx, timestamp: new Date().toISOString() });
    return true;
  }

  minePendingTransactions() {
    if (!this.pendingTransactions.length) return null;
    const block = this.addBlock({ transactions: this.pendingTransactions, count: this.pendingTransactions.length });
    this.pendingTransactions = [];
    return block;
  }

  validateChain() {
    for (let i = 1; i < this.chain.length; i++) {
      const curr = this.chain[i];
      const prev = this.chain[i - 1];
      if (curr.hash !== curr._calculateHash()) return false;
      if (curr.previousHash !== prev.hash) return false;
    }
    return true;
  }

  getChainInfo() {
    return {
      length: this.chain.length,
      valid: this.validateChain(),
      difficulty: this.difficulty,
      pendingTransactions: this.pendingTransactions.length,
      latestHash: this.getLatestBlock().hash,
    };
  }
}

// ── NFT ───────────────────────────────────────────────────────────────────────

class NFT {
  constructor(tokenId, name, metadata) {
    this.tokenId = tokenId;
    this.name = name;
    this.metadata = metadata;
    this.owner = 'ScrollVerse';
    this.createdAt = new Date().toISOString();
    this.divineBlessing = true;
    this.transferHistory = [];
  }

  toJSON() {
    return {
      tokenId: this.tokenId,
      name: this.name,
      metadata: this.metadata,
      owner: this.owner,
      createdAt: this.createdAt,
      divineBlessing: this.divineBlessing,
      transferHistory: this.transferHistory,
    };
  }

  /** GHL-compatible payload for contact note immortalization. */
  toGHLNote() {
    return `[NFT Minted] Token: ${this.tokenId} | Name: ${this.name} | Owner: ${this.owner} | Divine Blessing: ✓ | Minted: ${this.createdAt}`;
  }
}

// ── NFTManager ────────────────────────────────────────────────────────────────

class NFTManager {
  constructor(blockchain) {
    this.blockchain = blockchain || new BlockchainConnector();
    this.nfts = new Map();
    this.totalMinted = 0;
  }

  mintNFT(name, metadata) {
    const raw = `${name}_${this.totalMinted}_${Date.now()}`;
    const tokenId = crypto.createHash('sha256').update(raw).digest('hex').slice(0, 16);
    const nft = new NFT(tokenId, name, metadata);
    this.nfts.set(tokenId, nft);
    this.totalMinted++;
    this.blockchain.addTransaction({ type: 'NFT_MINT', tokenId, name, timestamp: new Date().toISOString() });
    return nft;
  }

  getNFT(tokenId) { return this.nfts.get(tokenId) || null; }

  transferNFT(tokenId, newOwner) {
    const nft = this.getNFT(tokenId);
    if (!nft) return false;
    nft.transferHistory.push({ from: nft.owner, to: newOwner, at: new Date().toISOString() });
    nft.owner = newOwner;
    this.blockchain.addTransaction({ type: 'NFT_TRANSFER', tokenId, to: newOwner, timestamp: new Date().toISOString() });
    return true;
  }

  immortalizeOnChain() {
    const block = this.blockchain.minePendingTransactions();
    if (!block) return { immortalized: false, reason: 'No pending transactions' };
    return {
      immortalized: true,
      blockIndex: block.index,
      blockHash: block.hash,
      transactions: block.data.count,
      eternalMessage: 'WALAHI! The contributions are immortalized forever!',
    };
  }

  getCollectionStats() {
    return {
      totalMinted: this.totalMinted,
      uniqueTokens: this.nfts.size,
      blockchainBlocks: this.blockchain.chain.length,
      pendingTransactions: this.blockchain.pendingTransactions.length,
      divineTokens: [...this.nfts.values()].filter(n => n.divineBlessing).length,
    };
  }

  /** Emit GHL-compatible payloads for all NFTs (for contact immortalization). */
  toGHLPayload() {
    return [...this.nfts.values()].map(nft => ({
      tokenId: nft.tokenId,
      name: nft.name,
      owner: nft.owner,
      email: `${nft.owner.toLowerCase().replace(/\s+/g, '.')}@scrollsoul.nft`,
      tags: ['nft-holder', 'scrollsoul-blockchain', `nft-${nft.tokenId}`],
      note: nft.toGHLNote(),
    }));
  }
}

module.exports = { Block, BlockchainConnector, NFT, NFTManager };
