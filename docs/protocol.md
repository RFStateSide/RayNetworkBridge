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
