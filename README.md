# RayNetworkBridge

RayNetworkBridge connects an existing Linux SocketCAN interface to compatible
network clients. It transports raw Classic CAN frames over the existing RN2K/1
TCP protocol used by RayNmeaSimulator's **Network NMEA2000** connection. The
simulator performs NMEA 2000 decoding, fast-packet handling and device identity
management; this bridge does not implement another NMEA codec.

Public Engineering Reference â€” AS-IS. This is a standalone source candidate for
owner review, not a published release or an installed service.

## Requirements and supported environments

- Linux, including Raspberry Pi OS on appropriately equipped Raspberry Pi
  systems, with SocketCAN and an owner-configured CAN interface. NMEA 2000 operation
  requires 250000 bit/s, UP, ERROR-ACTIVE and no recorded error/drop counters.
- Python 3.9 or newer (language/API minimum). Use a Python version supported by
  your Linux distribution; isolated tests currently cover 3.13 and 3.14 on Linux
  and 3.11 on Windows.
- iproute2 `ip` for physical CAN health inspection. No pip, Qt, SDL or NMEA library
  installation is required by the Python bridge.
- A controlled test network and a compatible RN2K/1 client. Physical CAN requires
  suitable hardware, drivers, wiring and termination supplied by the operator.

Windows can run the in-process virtual hub and protocol tests. Physical
SocketCAN operation is Linux-specific. CAN FD and NMEA 0183 are not implemented.

## Build and local checks

There is no native compilation step. From this source root:

```sh
python3 -B -m unittest discover -s tests -p '*tests.py' -v
python3 -B tools/network-can/raynmea_bridge.py --help
```

Tests use loopback TCP and mocked CAN only; they do not reconfigure or transmit
to a physical interface. The retained script's source Git mode is 100644; use
the explicit `python3` invocation shown above.

## Installation and configuration

Copy this source to a private directory. No installer or package manager is
invoked. Run as an appropriately restricted non-root account with access to the
already configured CAN interface. This utility never changes CAN bitrate, link
state, queue configuration or startup services.

Prepare the CAN interface separately under the network owner's operating
procedure. Read-only inspection examples are `ip -details -statistics link show
can0` and `ip -json -details -statistics link show can0`. The bridge refuses an
unhealthy interface; historical nonzero counters also cause refusal. Diagnose
the cause rather than resetting the live bus merely to pass the check.

Create a new local key without printing it:

```sh
umask 077
mkdir -p private
chmod 700 private
python3 -c 'import secrets; open("private/access.key", "x").write(secrets.token_hex(32))'
python3 -B tools/network-can/raynmea_bridge.py --interface can0 \
  --bind 127.0.0.1 --port 29501 --key-file private/access.key \
  --allow-client 127.0.0.1/32
```

Use a nonempty key, protect it with mode 0600 and share it privately with
authorized clients. Never commit a key. Omitting `--key-file` disables all TX and
service authorization. A specified but empty file also permits only RX; the
current CLI does not reject this configuration as an input error.

`--bind` defaults to loopback, `--port` to 29501, and `--interface` to can0.
Repeat `--allow-client CIDR` for each permitted network. With no allowlist, any
client able to reach the listener can connect. IPv4 and IPv6 networks must match
the actual accepted peer address family. There is no separate configuration file,
user database, per-user role policy or credential rotation command.

## Authentication and secure connections

RX is intentionally unauthenticated, including delivery before an RX auth
exchange. The IP allowlist restricts both RX and TX. TX and service authorization
require HMAC-SHA256 over a fresh RN2K/1 challenge; the shared key is not sent.
This does not encrypt traffic or authenticate the server to the client. All
holders of the shared key have the same transmit authority.

For an untrusted network, use an SSH tunnel and keep the bridge on loopback:

```sh
ssh -N -L 29501:127.0.0.1:29501 user@linux-host
```

Configure the client for 127.0.0.1:29501 and the exact remote interface name.
IP restrictions apply to the tunnel endpoint as seen by the bridge. Do not expose
the raw listener directly to the Internet. TLS, authenticated RX and encrypted
RN2K transport are not current features.

## RayNmeaSimulator integration

In Setup > NMEA2000 select Network NMEA2000, configure host/port, matching remote
interface, RX-only or RX/TX capability, access key and a distinct device number.
Connect RX first. Capability selection alone does not authorize Sending.
Explicit Enable Sending opens an authenticated TX session. Stop/F12, disconnect
and relevant configuration/mode changes revoke application authority. Reconnect
explicitly after failure; it must not silently resume Sending.

Discover/Refresh/Retrieve opens a separate bounded service session. Its server
filter permits coarse management PGNs, not a guaranteed read-only command subset.
The released simulator additionally enforces the precise route-selector policy.
An arbitrary key holder must be trusted to transmit; this bridge alone cannot
enforce navigation or vessel safety. See the [existing integration guide](tools/network-can/README.md)
and [RN2K/1 contract](docs/protocol.md).

## Virtual CAN development

For an existing owner-configured Linux vcan0 interface, use `--interface vcan0`.
The interface must already be UP; this program does not create or remove it.
Real kernel-vcan end-to-end behavior remains a separate qualification item.

Where vcan is unavailable, this command opens no CAN socket:

```sh
python3 -B tools/network-can/raynmea_bridge.py --virtual --interface lab \
  --bind 127.0.0.1 --port 29501
```

Without a key this is RX-only. To test virtual TX add a separate test-only key
file. The physical and virtual listeners must use separate ports. A virtual hub
is not an NMEA equipment simulator or a bus-timing/acknowledgment simulation.

## Running interactively and service lifecycle

Run the command interactively; Ctrl+C stops it. EOF/disconnect cancels queued
session writes. The utility provides no daemon installer, systemd unit or restart
manager. It does not reload keys without a process restart. Already queued kernel
or transmitted CAN data cannot be recalled.

A future reviewed systemd example should use Type=simple, an explicit absolute
Python/script path, a non-root service account and protected key, journald output,
and Restart=no initially. Coordinate startup with the separately owned CAN setup
service. Do not configure automatic recovery after a CAN-health fault without a
separate operational review. A systemd service restart must not authorize a
client to resume Sending automatically. No such unit is installed by this source.

## Diagnostics and limitations

Startup prints protocol, selected port and physical/virtual mode. Session-close
and TX-stop events are JSON on stdout. There are no rotating log files, web UI,
metrics endpoint or persistent capture store. Use terminal output or journald
under an independently configured service.

Verify address/port, interface spelling, IP allowlist and key permissions if
connection fails. Check the CAN health counters for a rejected physical startup.
RX does not require a key. An expired TX/service session requires fresh explicit
authorization on a new connection. Do not retry stale frames after faults.

The bridge has bounded client counts, queues, line sizes and TX rates; see the
protocol document. It offers no delivery acknowledgment from CAN equipment,
guaranteed real-time scheduling, persistence or automatic reconnection. Multiple
bridges or network forwarding loops require separate topology qualification.
Normal-mode CAN reception is not an electrically silent bus monitor.

## Safety and licensing

Use an isolated, controlled test network. Generated data can look genuine to
receivers. Do not rely on this utility or connected simulator for real-world
navigation, steering, collision avoidance, propulsion or alarms. Stopping software
cannot recall data already sent and is not an emergency-stop system.

Copyright (C) 2026 RF StateSide LLC. Existing implementation and retained tests
are AGPL-3.0-or-later; see [LICENSE](LICENSE) and [provenance](PROVENANCE.md).
Python, Linux and iproute2 remain separately licensed runtime dependencies; no
copies are bundled here. Release source must include this implementation, tests,
instructions and any modifications. Any binary/runtime distribution needs its
own actual-component inventory and corresponding-source review. AGPL-3.0-or-later
is retained for this standalone project. Initial release version v0.1.0 is
proposed, subject to owner release approval; wire protocol remains RN2K/1.
