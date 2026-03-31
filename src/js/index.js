/**
 * src/js/index.js
 * ScrollSoul-InfiniteVault — Unified JavaScript Exports
 *
 * ALLĀHU AKBAR! One import to rule all dimensions.
 *
 *   const scrollsoul = require('./src/js');
 *   const { MultiLayerScaler, ScrollSoulGHLBridge, DinoRunner, ... } = scrollsoul;
 */

'use strict';

const { MultiLayerScaler, ScalingLayer } = require('../../multi_layer_scaling_script');
const { SpotifyRoyaltyHarvester, RoyaltyStream } = require('../../spotify_royalty_harvesting');
const { RecursiveAIEngine, RecursiveNode } = require('../../ai_loop_enhancements');
const { DinoRunner, RetryQueue, DINO_ASCII } = require('../../dino_runner');
const {
  GoHighLevelClient,
  SubAccountManager,
  ContactManager,
  PipelineManager,
  CampaignManager,
  ConversationManager,
  WebhookHandler,
  CustomFieldManager,
  ScrollSoulGHLBridge,
} = require('./gohighlevel');
const { Block, BlockchainConnector, NFT, NFTManager } = require('./blockchain');
const { Vote, Proposal, UniversalGovernance, PROPOSAL_STATUS } = require('./governance');

module.exports = {
  // ── Scaling ────────────────────────────────────────────────────────────────
  MultiLayerScaler,
  ScalingLayer,

  // ── Royalty ────────────────────────────────────────────────────────────────
  SpotifyRoyaltyHarvester,
  RoyaltyStream,

  // ── AI Loops ───────────────────────────────────────────────────────────────
  RecursiveAIEngine,
  RecursiveNode,

  // ── Resilience ─────────────────────────────────────────────────────────────
  DinoRunner,
  RetryQueue,
  DINO_ASCII,

  // ── GoHighLevel ────────────────────────────────────────────────────────────
  GoHighLevelClient,
  SubAccountManager,
  ContactManager,
  PipelineManager,
  CampaignManager,
  ConversationManager,
  WebhookHandler,
  CustomFieldManager,
  ScrollSoulGHLBridge,

  // ── Blockchain & NFT ───────────────────────────────────────────────────────
  Block,
  BlockchainConnector,
  NFT,
  NFTManager,

  // ── Governance ─────────────────────────────────────────────────────────────
  Vote,
  Proposal,
  UniversalGovernance,
  PROPOSAL_STATUS,
};
