# RN2K/1 compatibility contract

Retain wire protocol version 1 independently of the proposed application version.
Use the released RayNmeaSimulator contract; do not invent a second PGN protocol.

Transport is TCP with newline-terminated JSON commands, at most 1024 bytes per
command including its newline. Server greeting fields are `kind=hello`,
`version=1`, `interface`, random `client`, and fresh 64-character hexadecimal
`nonce`. Reply with `kind=auth`, exact `interface`, `mode=rx|tx|service` and
hexadecimal `proof` for TX/service. Proof is HMAC-SHA256 of UTF-8
`nonce|client|mode|interface`, keyed with the stripped bytes of the shared key
file. Reply is `kind=ready`, matching `mode` and a new `nonce`. In-connection
reauthorization is rejected; open a new connection for a new role.

RX delivery is public to accepted IP peers, even before auth. TX/service requires
a valid key proof. Send `kind=ping` approximately each second; server replies
`kind=pong`. TX lease is 3 seconds. The input read timeout is 5 seconds. Service
additionally has a nonrenewable 60-second hard limit and a 512-frame budget.

Frames are `kind=frame`, `id` (uint32 Linux CAN ID including EFF/RTR flags), `dlc`
(0..8), and `data` (hexadecimal bytes of matching length). Server adds `seq`
(monotonically increasing within one process), `origin` (assigned client or bus),
and `timestamp_ns` (wall clock, not a synchronized hardware CAN timestamp).
CAN error injection and FD are unsupported. Standard/RTR frames can traverse the
bridge, but the simulator decodes only extended Classic CAN data frames.

Network frames are written once to SocketCAN and forwarded once to other clients,
without an origin echo. The socket disables receive-own-messages. Legitimate
identical repeated frames are preserved. This property applies to a single bridge
instance; arbitrary multi-bridge topologies are not qualified.

Service raw PGN allowlist: 59392, 59904, 60928, 126208, 126464, 126993, 126996,
126998. This is not a complete semantic read-only filter. RayNmeaSimulator's
RouteServicePolicy additionally restricts decoded messages/selectors.

Bounds: 16 accepted clients; 128 queued TX frames per client; maximum queue age
2 seconds; 500 submitted frames/second/client; shared physical CAN write spacing
at least 5 ms. Before writing an envelope, pending output above 64 KiB causes
disconnect (a high-water check, not an exact maximum allocation). Virtual mode
does not apply physical CAN pacing. Slow readers, malformed commands, expired
leases, queue overflow and CAN faults revoke affected sessions. CAN write/health
faults fail the bridge closed for further clients until operator intervention.

CAN health inspection runs every 0.5 seconds with an ip subprocess timeout of
2 seconds. Non-vcan links must be UP, ERROR-ACTIVE at 250000 bit/s with zero
reported error/drop and CAN extended statistics. No interface changes or counter
resets are performed. Disconnect discards pending application queue entries;
it cannot recall data already accepted by the kernel or CAN network.

## Deployment source offer

The `hello` envelope additionally contains an optional `source` object with
`license`, a prominent `notice`, `request=source`, `bytes`, `sha256`, and
`revision=sha256:<archive digest>`. The digest identifies the complete deployment
source ZIP; it is content-addressed and does not assert a Git commit or public
URL. The CLI requires and snapshots an explicit source allowlist at startup.
Runtime keys/configuration, Git metadata and arbitrary files are never selected.

On a fresh connection, a source client sends `{"kind":"source"}`. It does not
authenticate for TX. An already RX-authorized connection may also request source;
TX/service connections must reconnect RX first. Existing IP/client-count limits
apply. This command does not enqueue CAN data or authorize Sending.

The dedicated response consists of `kind=source_chunk`, sequential zero-based
`index` and base64 `data` (at most 512 decoded bytes/chunk), then
`kind=source_end`, `bytes` and `sha256`. Each envelope remains below the existing
1024-byte limit. The server closes the connection after transfer; CAN broadcasts
are suppressed for that source-transfer session. Frames already queued before
the request may precede the chunks. Other clients continue normally.

Source input and archive sizes are bounded to 2 MiB; server transfer deadline is
5 seconds. The provided helper has a 15-second overall deadline, line/size/order/
checksum checks, and a bound on preceding CAN frames. It saves only verified
bytes, does not overwrite and never extracts/executes them. SHA-256 detects an
incorrect transfer, not a malicious network peer: use SSH for server identity,
confidentiality and integrity over untrusted networks.

Existing RN2K/1 clients ignore the extra greeting object and receive no source
chunks unless they explicitly request them. Version, CAN envelopes, challenge
authentication, heartbeats, rate limits and leases remain unchanged. Modified
operators must update the source allowlist for added preferred code and keep the
offer usable for their network users. Public project publication alone does not
identify a later modified deployment.
