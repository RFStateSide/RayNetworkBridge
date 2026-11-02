# RayNetworkBridge public-release readiness

M1.2 — independent PRIVATE source repository establishment, 2026-11-02.
This is the sole maintained repository audit. Detailed engineering evidence stays
outside tracked source. Initial public deliverable: documented Python source.

## Accepted source and private qualification

- Owner-authorized standalone extraction from the qualified M1.1 candidate;
  corrected bridge, all existing tests and startup-cleanup regression retained.
  Independent initial Git history; no RayNmeaSimulator parent history, SDKs,
  private configuration, credentials, captures or unrelated application files.
- RF StateSide ownership and AGPL-3.0-or-later retained. README covers physical
  Linux/Raspberry Pi prerequisites, isolated virtual modes, network/key setup,
  protocol, simulator integration, security limitations and AS-IS safety scope.
- M1.1 evidence: 18 isolated Python cases pass on Windows, Ubuntu and Rpi5_ssd;
  Linux CLI virtual startup/RX/heartbeat pass. Actual simulator client against the
  candidate passes (10 Qt pass incidents, two opt-in cases skipped).
- Startup regression fails against the historical defective implementation and
  passes corrected source. M1.2 fresh-clone tests and file/blob/mode comparison
  are required closeout checks; detailed receipts are kept outside this tree.
- RN2K/1 remains unchanged. TX/service is HMAC-authenticated; RX is intentionally
  unauthenticated within the IP allowlist. Traffic is unencrypted. Service mode
  is a coarse PGN gate; the simulator supplies the stricter route policy.
- Historical Boat evidence is not current runtime verification. No operational
  bridge, service or CAN interface is replaced by repository establishment.

## Remaining PUBLIC source-release gates

- Owner acceptance of the final source release, proposed v0.1.0 and public scope.
  No release/version tag, public visibility or website publication is authorized.
- Provide a prominent, usable corresponding-source offer to remote users of
  modified deployments under AGPL section 13. README now identifies the canonical
  source and its PRIVATE access limitation. A private inaccessible URL is not a
  completed source offer. Recommend a revision-pinned public source link, notice
  in startup/connection information and an access check before public release;
  no source-advertisement field is currently implemented in RN2K/1.
- Review authorship/provenance, license and all retained independent history;
  confirm GitHub access, automation and source availability at publication time.
  Headers and engineering provenance do not independently certify legal title.
- Approve README/security/safety claims. No claim of certified marine operation,
  generic NMEA gateway behavior or fully qualified managed service is made.

## Explicit qualification limits

- No current Boat process/source identity or active-client status has been
  verified. Obtain operational authorization before inspecting or replacing it.
- Kernel vcan, managed-service lifecycle, long-duration load and new physical
  deployments are separate qualification items. They may remain excluded from
  an explicitly scoped experimental source release; no systemd unit is shipped.
- No binary/runtime package is prepared. If bundling is added later, inventory
  actual redistributed components, notices and corresponding-source obligations.

PRIVATE repository establishment is authorized. PUBLIC publication and operational
replacement remain NO-GO pending the applicable owner approvals and source offer.
