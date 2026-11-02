# RayNetworkBridge public-source release readiness

M1.3, 2026-11-02. Target: documented v0.1.0 Python source, Public Engineering
Reference — AS-IS. This is the sole maintained repository audit. Detailed test
logs, manifests and reports remain outside tracked source.

## Source authority and preservation

- Independent PRIVATE repository RFStateSide/RayNetworkBridge, ID 1442660341.
  Accepted initial commit: 1418990ef77bb0c3848eef1be3c552272e3d421b.
  Its root commit imports no RayNmeaSimulator history. The owner accepted M1.3
  and authorized private source closeout in M1.3A; no publication is authorized.
- RF StateSide ownership, full AGPL-3.0-or-later and original provenance retained.
  Added source-offer/helper/test code uses Python standard-library APIs only.
  No Qt, NMEA, SDL, CANboat, artwork, credentials or runtime libraries bundled.
- Source inventory is 14 explicit preferred-source files. Runtime configuration,
  keys, captures, user data, Git history and engineering evidence are excluded.
  The deployed-source offer uses the same allowlist and adds a hash manifest.
- Original socket-cleanup fix and readiness regression remain present; original
  tests are unchanged. RayNmeaSimulator source/release and operational bridges,
  CAN interfaces, owner data and Qt Creator configurations remain untouched.

## Matching corresponding-source offer

- CLI snapshots the executed bridge source plus the complete allowlisted source
  tree before opening CAN. Missing, symlinked or oversized preferred source fails
  startup instead of advertising an incomplete offer. Snapshot ZIP is immutable
  in memory and bounded to 2 MiB; no disk archive is written by the server.
- Startup and hello prominently offer free deployment source. A content-addressed
  SHA-256 revision identifies actual snapshot bytes rather than mutable master,
  an invented Git commit or an unavailable private GitHub URL.
- Optional RN2K/1 source metadata and an explicitly requested RX-only transfer
  provide a usable retrieval path independent of public repository visibility.
  IP/client limits remain; no TX key or CAN authorization is needed for source.
  Transfer is bounded, suppresses broadcasts on that dedicated session and closes
  afterward. The helper checks envelope/order/size/digest and never overwrites,
  extracts or executes downloaded content.
- README/protocol explain AGPL section 13, project source versus later modified
  deployments, extending the source allowlist for added code and presenting the
  notice to users of client interfaces that hide optional protocol metadata.
  This implements the engineering delivery mechanism; it is not an independent
  legal title/compliance certification for arbitrary future modified deployments.

## Focused qualification

- 25 Python cases pass on Windows, Ubuntu and Rpi5_ssd, including all 18 previous
  authorization, bounds, fault, pacing, queue and cleanup tests. New cases cover
  actual source inventory/manifest/determinism, missing/symlink/size rejection,
  key-free retrieval/no CAN TX, immutable offer, CIDR restriction, legacy hello
  bounds/auth, TX-session rejection and malformed/order/checksum handling.
- Offered ZIP is independently extracted and its complete test suite passes.
- Linux actual CLI startup, RX heartbeat, helper download and overwrite refusal
  pass in temporary loopback-only directories; no CAN sockets or service changes.
- Released-compatible RayNmeaSimulator transport/core passes the updated hello
  and existing multi-client/route/Stop cases: 10 Qt pass incidents, 2 opt-in
  physical/other-host cases skipped. New fields are ignored; ordinary clients
  never receive source chunks without requesting them. CAN framing, proof,
  heartbeat/lease semantics and original TX limits remain unchanged.
- Source syntax, Markdown links/anchors, notices, privacy and preferred-source
  inventory reviewed. README encoding defect and stale candidate wording fixed.
  Proposed v0.1.0 source-only notes prepared without a Release or tag.

## Security, safety and scope limits

- RX is not individually authenticated; TX/service uses a shared key. No bridge
  encryption or server identity guarantee; use restrictive bind/CIDR or SSH.
  Snapshot hashes do not authenticate an untrusted network peer. Service PGN
  filtering is coarse; the simulator supplies precise route policy. None is a
  certified navigation, collision-avoidance or vessel-control safety system.
- Boat runtime remains unknown; historical deployment is not current verification.
  No Boat contact, physical transmission, managed-service installation or new
  physical vessel qualification is required for this approved source-only scope.
- Real kernel-vcan, long-load and managed-service lifecycle claims remain excluded
  unless separately qualified. No binary/runtime distribution is proposed.
- M1.2 permission review: two existing organization owners have admin access;
  no other collaborators/teams/keys/hooks/installed Apps found. Actions defaults
  to a read-only token and no workflows are shipped. master is unprotected;
  GitHub's ruleset API reports a private-plan limitation. Recheck access and
  available branch protection at publication; do not change visibility to bypass it.

## Decision and remaining owner gates

Engineering GO for the narrowly scoped, documented public Python source release.
The owner accepted M1.3 and the source-only scope and authorized private
commit/push in M1.3A. No remaining demonstrated source-delivery implementation
blocker is identified in this scope. Public visibility, public tag/Release and website
publication each require separate authorization. After an approved commit, verify
the release source from a fresh clone and recheck anonymous source access when
visibility is intentionally changed. Do not advertise a publication event before
it occurs. Operational replacement remains separately authorized work.
