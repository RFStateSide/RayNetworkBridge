# RayNetworkBridge public-source release readiness

M1.4, 2026-11-02. Published v0.1.0 Python source, Public Engineering
Reference — AS-IS. This is the sole maintained repository audit. Detailed test
logs, manifests and reports remain outside tracked source.


## Verified public publication — M1.4

- PUBLIC repository: https://github.com/RFStateSide/RayNetworkBridge
  (original standalone ID 1442660341 retained).
- Accepted release source: `9d2dac04a9374aca93e37b558c7aed7ac24c5607`.
  Annotated `v0.1.0` tag object: `ea5381a71adb2964a0df91424360e7c50db792f0`.
  It points exactly to the accepted source and is not moved by this audit update.
- Published source-only Release:
  https://github.com/RFStateSide/RayNetworkBridge/releases/tag/v0.1.0
  (Release ID 431224587). Approved notes retained with download/verification data.
- Single manually uploaded asset: `RayNetworkBridge-0.1.0.tar.gz`, 33,858 bytes,
  asset ID 701063560. SHA-256:
  `d5769e8ed62f644c15301856bf789e3a481668669bfd1b673424ee3ed00d468d`.
  Versioned top directory contains all 14 accepted source/support files.
  Two independent constructions from accepted Git blobs produce identical bytes;
  fixed gzip timestamp, commit-derived tar timestamp, normalized owner/modes.
- Anonymous clone/tag/README/license/provenance/protocol and GitHub-generated
  source download verified. Anonymous Release asset download matches retained
  package and website-workflow copy exactly. Generated GitHub source links are
  separate from the single uploaded distribution asset.
- Downloaded package extraction, committed-file hashes, syntax, CLI and 25 focused
  tests pass. Its independently extracted offered-source ZIP also passes all 25.
  Actual virtual CLI network-source retrieval matches the deployed snapshot;
  SHA-256 `a582465918facbaca004d5229d08430a048722ecfdcc147fe0871522b36c0608`.
  No real CAN socket/transmission or operating service changes were required.
- Only existing administrators RayJr2/kb1so have maintainer access; no teams,
  deploy keys, hooks or installed Apps found. Actions defaults read-only; no
  workflows shipped. Public fork access is enabled; Pages is not enabled.
  master has no ruleset/protection; the public ruleset API is now accessible and
  returns none. Protection policy remains an owner maintenance decision.
- No RF StateSide website changes or announcement. An identical verified artifact
  is retained privately for the separately authorized website download workflow.
  No compiled installers, extra assets or new physical/service claims published.

## Source authority and preservation

- Independent PRIVATE repository RFStateSide/RayNetworkBridge, ID 1442660341.
  Accepted initial commit: 1418990ef77bb0c3848eef1be3c552272e3d421b.
  Its root commit imports no RayNmeaSimulator history. The owner accepted M1.3
  and authorized private source closeout in M1.3A and controlled publication in
  M1.4. Release source is fixed at 9d2dac04a9374aca93e37b558c7aed7ac24c5607.
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

## Decision and remaining owner actions

PUBLIC RELEASE PASS for the approved source-only v0.1.0 scope. The owner explicitly
accepted M1.3/M1.3A and authorized M1.4 visibility/tag/source Release operations.
The released code/tag and distribution archive remain fixed to the accepted
commit. This later audit-only commit records verified outcomes and is not a
replacement release source or rebuilt distribution.

RF StateSide website/Marine Firmware & Tools listing and download integration
remain a separate owner-approved task. Operational replacement, managed-service
or further physical qualification remain separately authorized work. Review
maintenance/branch protection policy with the owner; no permissions were changed
to perform this release. Future operator modifications must retain usable matching
source and truthful source identity; publication does not certify arbitrary
modified deployments or marine safety.
