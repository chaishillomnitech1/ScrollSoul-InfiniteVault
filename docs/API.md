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

---

## GoHighLevel Integration

### GoHighLevelClient

**Constructor:**
```python
GoHighLevelClient(api_key=None, location_id=None, company_id=None, use_v2=False, retry_attempts=5)
```
Auto-reads `GHL_API_KEY`, `GHL_LOCATION_ID`, `GHL_COMPANY_ID` from environment.

**Methods:**
- `get(endpoint, location_id=None, params=None)` — GET request with DinoRunner retry
- `post(endpoint, location_id=None, data=None)` — POST request
- `put(endpoint, location_id=None, data=None)` — PUT request
- `delete(endpoint, location_id=None)` — DELETE request
- `get_client_stats()` — Returns `{total_requests, total_errors, success_rate}`

---

### SubAccountManager

**Constructor:** `SubAccountManager(client: GoHighLevelClient)`

**Methods:**
- `list_locations()` — List all agency sub-accounts
- `get_location(location_id)` — Get single sub-account details
- `create_location(name, email, ...)` — Create a new sub-account
- `update_location(location_id, updates)` — Update sub-account fields
- `delete_location(location_id)` — Delete a sub-account
- `introspect_location(location_id)` — Deep-dive: contacts, pipelines, campaigns, tags, webhooks
- `introspect_all_locations()` — Deep-dive EVERY sub-account; returns aggregated stats
- `execute_across_all_locations(action, location_ids=None)` — Run any callable across all locations

---

### ContactManager

**Constructor:** `ContactManager(client: GoHighLevelClient)`

**Methods:**
- `create_contact(first_name, last_name, email, phone, tags, ...)` — Create a contact
- `get_contact(contact_id, location_id=None)` — Get contact by ID
- `search_contacts(query, location_id=None, limit=20)` — Search contacts
- `update_contact(contact_id, updates, location_id=None)` — Update contact
- `delete_contact(contact_id, location_id=None)` — Delete contact
- `add_tags(contact_id, tags, location_id=None)` — Add tags
- `remove_tags(contact_id, tags, location_id=None)` — Remove tags
- `add_note(contact_id, body, location_id=None)` — Add a note
- `add_task(contact_id, title, due_date=None, location_id=None)` — Add a task
- `upsert_contact(email, ...)` — Update if exists, create if not

---

### PipelineManager

**Constructor:** `PipelineManager(client: GoHighLevelClient)`

**Methods:**
- `list_pipelines(location_id=None)` — List all pipelines
- `create_opportunity(pipeline_id, name, contact_id, stage_id, monetary_value, ...)` — Create opportunity
- `update_opportunity(opportunity_id, updates, location_id=None)` — Update opportunity
- `move_stage(opportunity_id, stage_id, location_id=None)` — Move to a pipeline stage
- `get_opportunities(pipeline_id, location_id=None, limit=100)` — Get pipeline opportunities
- `delete_opportunity(opportunity_id, location_id=None)` — Delete opportunity

---

### CampaignManager

**Constructor:** `CampaignManager(client: GoHighLevelClient)`

**Methods:**
- `list_campaigns(location_id=None)` — List all campaigns
- `add_contact_to_campaign(campaign_id, contact_id, location_id=None)` — Enroll contact
- `remove_contact_from_campaign(campaign_id, contact_id, location_id=None)` — Remove contact
- `trigger_campaign_for_all_contacts(campaign_id, contact_ids, location_id=None)` — Batch enroll

---

### ConversationManager

**Constructor:** `ConversationManager(client: GoHighLevelClient)`

**Methods:**
- `list_conversations(location_id=None, limit=20)` — List conversations
- `get_conversation(conversation_id, location_id=None)` — Get single conversation
- `send_sms(contact_id, message, location_id=None)` — Send SMS
- `send_email(contact_id, subject, body, location_id=None)` — Send email
- `broadcast_sms(contact_ids, message, location_id=None)` — Bulk SMS

---

### WebhookHandler

**Constructor:** `WebhookHandler(client: GoHighLevelClient)`

**Methods:**
- `register_webhook(url, events=None, location_id=None)` — Register webhook endpoint
- `list_webhooks(location_id=None)` — List registered webhooks
- `delete_webhook(hook_id, location_id=None)` — Delete webhook
- `on(event, handler)` — Register local Python handler for an event type
- `dispatch(payload)` — Dispatch inbound webhook payload to handlers

---

### CalendarManager

**Constructor:** `CalendarManager(client: GoHighLevelClient)`

**Methods:**
- `list_calendars(location_id=None)` — List calendars
- `get_free_slots(calendar_id, start_date, end_date, location_id=None)` — Get availability
- `create_appointment(calendar_id, contact_id, start_time, end_time, title, ...)` — Book appointment
- `list_appointments(location_id=None, limit=20)` — List appointments

---

### CustomFieldManager

**Constructor:** `CustomFieldManager(client: GoHighLevelClient)`

**Methods:**
- `list_custom_values(location_id=None)` — List custom values
- `create_custom_value(name, value, location_id=None)` — Create custom value
- `update_custom_value(custom_value_id, value, location_id=None)` — Update value
- `upsert_custom_value(name, value, location_id=None)` — Update if exists, create if not

---

### TagManager

**Constructor:** `TagManager(client: GoHighLevelClient)`

**Methods:**
- `list_tags(location_id=None)` — List tags
- `create_tag(name, location_id=None)` — Create tag
- `delete_tag(tag_id, location_id=None)` — Delete tag

---

### ScrollSoulGHLBridge

**Constructor:**
```python
ScrollSoulGHLBridge(client=None, api_key=None, location_id=None, company_id=None)
```

**Sub-managers:** `.sub_accounts`, `.contacts`, `.pipelines`, `.campaigns`, `.conversations`, `.webhooks`, `.calendars`, `.custom_fields`, `.tags`

**Methods:**
- `sync_scaling_metrics(scaler_status, location_id=None)` — Push MultiLayerScaler → GHL custom values
- `sync_artist_to_ghl(artist, revenue, streams, pipeline_id, location_id=None)` — One artist → GHL contact + opportunity
- `sync_royalty_report(report, pipeline_id, location_id=None)` — Full royalty report → GHL
- `trigger_ai_campaign(engine_status, campaign_id, contact_ids, location_id=None)` — AI enlightenment → GHL campaign
- `sync_proposal_to_pipeline(proposal, pipeline_id, contact_id, location_id=None)` — Governance proposal → pipeline
- `sync_nft_owner_to_ghl(nft_data, location_id=None)` — NFT owner → GHL contact with blockchain note
- `execute_full_sync_across_all_locations(...)` — Execute EVERYTHING across ALL sub-accounts
- `get_bridge_status()` — Health, stats, and module connectivity

---

## JavaScript API

### DinoRunner

```javascript
const { DinoRunner, RetryQueue } = require('./dino_runner');
const runner = new DinoRunner({ maxRetries, baseDelayMs, circuitThreshold, ... });
```

- `runner.run(fn, { name })` — Execute async fn with retry + circuit-breaker
- `runner.runBatch(tasks)` — Run array of `{ fn, name }` tasks, collect all results
- `runner.executeAcrossLocations(locationIds, action)` — Run action across sub-accounts
- `runner.keepAlive(healthCheckFn, intervalMs)` — Start keep-alive interval
- `runner.getStatus()` — `{ totalRuns, successRate, circuitOpen, dinoMessage, ... }`
- `runner.announce()` — Print ASCII dino + stats

```javascript
const queue = new RetryQueue(runner, concurrency=3);
queue.enqueue(fn, name)    // Returns Promise
queue.getQueueStatus()     // { pending, running, processed }
```

### MultiLayerScaler (JS)

```javascript
const { MultiLayerScaler } = require('./multi_layer_scaling_script');
const scaler = new MultiLayerScaler({ initialLayers, defaultCapacity, autoExpand });
scaler.distributeLoad(amount)   // → { success, layer, utilization, ... }
scaler.getStatus()              // → { totalLayers, averageUtilization, layers, ... }
scaler.optimize()               // → { optimized, adjustments, averageUtilization }
scaler.toGHLPayload()           // → GHL custom-value key/value map
```

### SpotifyRoyaltyHarvester (JS)

```javascript
const { SpotifyRoyaltyHarvester } = require('./spotify_royalty_harvesting');
harvester.harvestStream(artist, track, streams, ratePerStream)
harvester.generateReport()       // → { totalRevenue, artistBreakdown, topEarners, ... }
harvester.alignWithUniverse()    // → { fairnessScore, karmaScore, ... }
harvester.toGHLPayload(pipelineId) // → Array of GHL contact/opportunity payloads
```

### RecursiveAIEngine (JS)

```javascript
const { RecursiveAIEngine } = require('./ai_loop_enhancements');
engine.fractalExpand(seedValue, iterations)   // → { totalNodes, dimensionalComplexity, ... }
engine.getEngineStatus()                      // → { karmaAccumulation, dimensionalComplexity, ... }
engine.achieveEnlightenment()                 // → { enlightened, enlightenmentScore, ... }
engine.shouldTriggerGHLCampaign()             // → boolean
engine.toGHLPayload()                         // → { ...status, shouldTrigger, enlightenment }
```

### ScrollSoulGHLBridge (JS)

```javascript
const { ScrollSoulGHLBridge } = require('./src/js/gohighlevel');
const bridge = new ScrollSoulGHLBridge({ apiKey, locationId, companyId });

bridge.subAccounts.introspectAllLocations()
bridge.subAccounts.introspectLocation(locationId)
bridge.contacts.upsertContact(email, data, locationId)
bridge.pipelines.createOpportunity(data, locationId)
bridge.campaigns.triggerForContacts(campaignId, contactIds, locationId)
bridge.conversations.sendSMS(contactId, message, locationId)
bridge.customFields.upsertCustomValue(name, value, locationId)
bridge.webhooks.registerWebhook(url, events, locationId)

bridge.syncScalingMetrics(ghlPayload, locationId)
bridge.syncRoyaltyArtists(ghlPayload, locationId)
bridge.triggerAICampaign(aiPayload, campaignId, contactIds, locationId)
bridge.executeFullSyncAcrossAllLocations({ scalerPayload, royaltyPayload, aiPayload, ... })
bridge.getBridgeStatus()
```
