# Copyright (C) 2026 RF StateSide LLC; SPDX-License-Identifier: AGPL-3.0-or-later
"""Real-source archive, bounded retrieval and RN2K/1 compatibility regressions."""
import asyncio, base64, hashlib, importlib.util, io, json, tempfile, unittest, zipfile
from pathlib import Path
from unittest.mock import patch
import network_bridge_tests as baseline
m = baseline.m
root = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('get_source', root/'tools/network-can/get_source.py')
client = importlib.util.module_from_spec(spec);spec.loader.exec_module(client)

class Archive(unittest.TestCase):
 def test_actual_source_complete_deterministic_and_no_owner_files(self):
  data, meta=m.build_source_offer();self.assertEqual((data,meta),m.build_source_offer())
  self.assertEqual(hashlib.sha256(data).hexdigest(),meta['sha256'])
  self.assertEqual(meta['revision'],'sha256:'+meta['sha256'])
  with zipfile.ZipFile(io.BytesIO(data)) as archive:
   self.assertEqual(set(archive.namelist()),set(m.SOURCE_PATHS)|{'SOURCE_MANIFEST.json'})
   manifest=json.loads(archive.read('SOURCE_MANIFEST.json'))
   self.assertEqual(len(manifest),len(m.SOURCE_PATHS))
   for item in manifest:
    content=archive.read(item['path'])
    self.assertEqual(hashlib.sha256(content).hexdigest(),item['sha256'])
    self.assertEqual(len(content),item['bytes'])
   self.assertEqual(archive.read('tools/network-can/raynmea_bridge.py'),m.IMPLEMENTATION_SOURCE)
   self.assertEqual(archive.read('LICENSE'),(root/'LICENSE').read_bytes())
 def test_missing_source_symlink_and_size_bounds(self):
  with tempfile.TemporaryDirectory() as temporary:
   with self.assertRaises(ValueError):m.build_source_offer(Path(temporary))
  with patch.object(Path,'is_symlink',lambda file:file.name=='README.md'):
   with self.assertRaises(ValueError):m.build_source_offer()
  with patch.object(m,'MAX_SOURCE_BYTES',100):
   with self.assertRaises(ValueError):m.build_source_offer()

class Protocol(unittest.IsolatedAsyncioTestCase):
 asyncTearDown=baseline.Protocol.asyncTearDown
 peer=baseline.Protocol.peer
 send=baseline.Protocol.send
 async def asyncSetUp(self):
  await baseline.Protocol.asyncSetUp(self)
  self.b.source_offer=m.build_source_offer()
 async def test_advertised_source_retrieved_without_key_and_no_can_tx(self):
  self.b.key=b''
  data,digest=await asyncio.to_thread(client.receive_source,'127.0.0.1',self.port)
  self.assertEqual(data,self.b.source_offer[0]);self.assertEqual(digest,self.b.source_offer[1]['sha256'])
  self.assertEqual(self.b.sequence,0)
 async def test_hello_stays_within_legacy_bounds_and_existing_auth_works(self):
  r,w,hello,ready=await self.peer('tx')
  self.assertLessEqual(len((json.dumps(hello,separators=(',',':'))+'\n').encode()),1024)
  self.assertEqual(hello['version'],1);self.assertIn('source',hello);self.assertEqual(ready['kind'],'ready')
  await self.send(w,kind='ping');self.assertEqual(json.loads(await r.readline())['kind'],'pong')
 async def test_tx_source_request_is_rejected(self):
  r,w,_,_=await self.peer('tx');await self.send(w,kind='source')
  self.assertEqual(json.loads(await r.readline())['kind'],'error');self.assertEqual(self.b.sequence,0)
 async def test_source_cidr_restriction_and_snapshot_stability(self):
  original=self.b.source_offer
  with patch.object(m,'IMPLEMENTATION_SOURCE',b'changed after startup'):
   data,_=await asyncio.to_thread(client.receive_source,'127.0.0.1',self.port)
  self.assertEqual(data,original[0])
  self.b.allow=[m.ipaddress.ip_network('192.0.2.0/24')]
  with self.assertRaises(ValueError):await asyncio.to_thread(client.receive_source,'127.0.0.1',self.port)
 async def test_untrusted_offer_order_size_checksum_and_missing_offer(self):
  async def trial(offer,packets):
   async def handler(reader,writer):
    writer.write((json.dumps(dict(kind='hello',version=1,source=offer))+'\n').encode());await writer.drain()
    await reader.readline()
    for packet in packets:writer.write((json.dumps(packet)+'\n').encode())
    await writer.drain();writer.close();await writer.wait_closed()
   server=await asyncio.start_server(handler,'127.0.0.1',0)
   try:
    with self.assertRaises((ValueError,KeyError)):
     await asyncio.to_thread(client.receive_source,'127.0.0.1',server.sockets[0].getsockname()[1])
   finally:server.close();await server.wait_closed()
  digest=hashlib.sha256(b'x').hexdigest()
  offer=dict(bytes=1,sha256=digest,revision='sha256:'+digest,request='source')
  await trial({},[])
  await trial(dict(offer,bytes=client.MAX_BYTES+1),[])
  await trial(offer,[dict(kind='source_chunk',index=1,data='eA==')])
  await trial(offer,[dict(kind='source_chunk',index=0,data='eQ=='),dict(kind='source_end',bytes=1,sha256=digest)])
  await trial(offer,[dict(kind='source_chunk',index=0,data=base64.b64encode(b'xx').decode())])

if __name__=='__main__':unittest.main()
