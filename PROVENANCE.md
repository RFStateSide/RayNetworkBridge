# Source provenance and standalone extraction

The bridge and original protocol regressions come from RF StateSide's accepted
RayNmeaSimulator source. Authoritative preparation baseline:
`846e5b27c1c3cd61f16a8bfcf4b6bd6d358e94a9`.
Their contents match the corrected released application build source
`bf212fc3389314153911ed5f4b759b9f56e2723f`.

Original paths: `tools/network-can/raynmea_bridge.py`,
`tools/network-can/README.md`, and `tests/network_bridge_tests.py`.
The bridge baseline SHA-256 is
`0d7569d29ebd1168ea1ec5b74ab3468b8f580b5ad7496be6a5b4212a76dca89f`.
The existing RF StateSide copyright/SPDX headers and AGPL license are retained.
The private historical provenance identifies introduction/change evidence at
`46fdc58cecad58ec75d72ec65c4d54a7d51ef58f`; this does not establish inherited
ancestry in a future independent repository or independently certify legal title.

The candidate adds startup-exception socket cleanup (before any listener starts),
isolated regression tests and standalone documentation. Engineering preparation
used OpenAI Codex assistance; original RF StateSide engineering ownership is
retained. There are no imported Qt, SDL, CANboat, NMEA library, icon, route, image
or hardware-design files in this source candidate. The bridge uses Python's
standard library and Linux SocketCAN/iproute2 APIs. Runtime dependencies are not
bundled or relicensed as RF StateSide code.

The retained integration guide discusses RayNmeaSimulator's separately maintained
client tests. It does not imply this independent candidate includes that C++
application or Qt build. No private key, deployed configuration, owner dataset,
historical audit or Git history is required by the candidate.


The standalone repository begins with independent history; the source hashes and
historical references above are provenance, not imported parent commits. The
qualified startup correction and its failing-before/passing-after regression are
preserved in the initial commit. M1.2 retains all M1.1 implementation/test bytes;
only the README, this provenance note and the sole release audit are refreshed
for independent private repository establishment.
