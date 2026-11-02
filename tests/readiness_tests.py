# Copyright (C) 2026 RF StateSide LLC; SPDX-License-Identifier: AGPL-3.0-or-later
"""Isolated loopback and mocked SocketCAN readiness checks; never open CAN."""
import asyncio, json, unittest
from unittest.mock import patch, Mock
import network_bridge_tests as baseline
m = baseline.m

class Readiness(unittest.IsolatedAsyncioTestCase):
 asyncSetUp = baseline.Protocol.asyncSetUp
 asyncTearDown = baseline.Protocol.asyncTearDown
 peer = baseline.Protocol.peer
 send = baseline.Protocol.send
 async def test_start_failure_releases_socket(self):
  bus=Mock()
  bridge=m.Bridge('isolated-nonexistent')
  with patch.object(m.socket,'socket',return_value=bus), patch.object(m.socket,'PF_CAN',29,create=True), patch.object(m.socket,'SOL_CAN_RAW',101,create=True), patch.object(m.socket,'CAN_RAW_RECV_OWN_MSGS',4,create=True), patch.object(m.socket,'CAN_RAW',1,create=True), patch.object(bridge,'check_health',side_effect=ValueError('synthetic unhealthy link')):
   with self.assertRaises(ValueError): await bridge.start()
  bus.close.assert_called_once()
  self.assertIsNone(bridge.bus)

 async def test_allowlist_denies_even_receive(self):
  self.b.allow=[m.ipaddress.ip_network('192.0.2.0/24')]
  r,w=await asyncio.open_connection('127.0.0.1',self.port);self.writers.append(w)
  self.assertEqual(await asyncio.wait_for(r.read(),1),b'')

 async def test_receive_is_intentionally_unauthenticated(self):
  r,w=await asyncio.open_connection('127.0.0.1',self.port);self.writers.append(w)
  self.assertEqual(json.loads(await r.readline())['kind'],'hello')
  _,tx,_,_=await self.peer('tx')
  await self.send(tx,kind='frame',id=0x89f8012c,dlc=0,data='')
  self.assertEqual(json.loads(await asyncio.wait_for(r.readline(),1))['kind'],'frame')

 async def test_no_key_rejects_tx_but_allows_rx(self):
  self.b.key=b''
  _,_,_,reply=await self.peer('tx');self.assertEqual(reply['kind'],'error')
  _,_,_,reply=await self.peer('rx');self.assertEqual(reply['kind'],'ready')

 async def test_stale_queue_revokes_before_write(self):
  class Bus:
   def __init__(self): self.sent=[]
   def send(self,data): self.sent.append(data);return 16
  bus=Bus();self.b.bus=bus
  r,w,_,_=await self.peer('tx')
  peer=next(p for p in self.b.peers if p['mode']=='tx')
  peer['queue'].put_nowait((dict(id=0x89f8012c,dlc=0,data=''),m.time.monotonic()-3))
  self.assertEqual(json.loads(await asyncio.wait_for(r.readline(),1))['kind'],'error')
  self.assertEqual(bus.sent,[])

 async def test_malformed_and_oversized_envelopes(self):
  for data in (b'[]\n',b'{invalid}\n',b'x'*1026+b'\n'):
   r,w,_,_=await self.peer()
   w.write(data);await w.drain()
   reply=json.loads(await asyncio.wait_for(r.readline(),1))
   self.assertEqual(reply['kind'],'error')

 async def test_write_fault_revokes_all_clients(self):
  class Bus:
   def send(self,data): raise OSError('synthetic failure')
  self.b.bus=Bus()
  r,w,_,_=await self.peer('tx');other,_,_,_=await self.peer('rx')
  await self.send(w,kind='frame',id=0x89f8012c,dlc=0,data='')
  self.assertEqual(json.loads(await asyncio.wait_for(other.readline(),1))['kind'],'error')
  self.assertTrue(self.b.fault);self.assertEqual(self.b.sequence,0)

 async def test_health_rules_without_can_socket(self):
  bridge=m.Bridge('test0')
  link=dict(flags=['UP'],linkinfo=dict(info_kind='can',info_data=dict(state='ERROR-ACTIVE',bittiming=dict(bitrate=250000)),info_xstats={}),stats64=dict(rx=dict(errors=0,dropped=0),tx=dict(errors=0,dropped=0)))
  with patch.object(m.subprocess,'check_output',side_effect=lambda *a,**k:json.dumps([link]).encode()):
   bridge.check_health()
   link['stats64']['rx']['dropped']=1
   with self.assertRaises(ValueError):bridge.check_health()
   link['linkinfo']=dict(info_kind='vcan');bridge.check_health()
   link['flags']=[]
   with self.assertRaises(ValueError):bridge.check_health()

if __name__=='__main__':unittest.main()
