# RayNetworkBridge v0.1.0

Public Engineering Reference — AS-IS. First standalone Python source-release scope.

RayNetworkBridge exposes an existing Linux SocketCAN interface to compatible
RN2K/1 TCP clients, including RayNmeaSimulator Network NMEA2000. It transports
Classic CAN frames and leaves NMEA decoding and device identity to the client.

- RX access restricted by network binding and optional CIDR allowlists.
- Shared-key HMAC-SHA256 authorization for TX and bounded route-service sessions.
- Multiple clients, origin/sequence metadata, bounded queues and physical pacing.
- Explicit fault/lease handling; no automatic reauthorization or stale TX retries.
- Existing Linux vcan support and a CAN-free in-process virtual test hub.
- Matching deployed source is advertised and retrievable from the same listener
  without a key or a dependency on GitHub access, subject to the RX IP allowlist.
- Failed CAN startup releases its socket; regression coverage is included.

Requirements: Python 3.9+ API compatibility (use a supported distribution Python),
Linux SocketCAN and iproute2 for physical CAN. No pip dependencies or compiled
installer. Install the complete source tree and follow README.md.

The bridge does not configure CAN, install a service, decode NMEA PGNs, implement
NMEA 0183/CAN FD or provide TLS. RX is not individually authenticated. Service
PGN filtering is coarse and is not a safety-critical authorization boundary.
Do not use this tool as an operational navigation or vessel-control system.

Source and tests are AGPL-3.0-or-later. Read the source-availability and security
instructions before deploying a modified version or exposing a listener.
