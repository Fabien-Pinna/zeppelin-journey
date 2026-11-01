import test from 'node:test';
import assert from 'node:assert/strict';
import { islands } from '../src/features/journey/world.js';
import { islandBoundary } from '../src/features/journey/landscape.js';
import { moveWalker, obstaclesFor, penetration, TRAPEZE } from '../src/features/journey/physics.js';
import layouts from '../src/features/journey/layouts.json' with { type: 'json' };

test('shore and pool prevent walking onto decorative water',()=>{
  const i=islands.find(i=>i.id==='clubmed');
  const [x,z]=moveWalker(i.position[0]-8,i.position[2]-1.5,-12,0,i);
  assert.ok(x-i.position[0]>-13.6);
  assert.equal(penetration(x-i.position[0],z-i.position[2],layouts.clubmed.find(o=>o.name==='sea')),null);
  const [px,pz]=moveWalker(i.position[0]+13,i.position[2]-4,0,-6,i);
  assert.ok(pz-i.position[2]>-5.7);
  assert.equal(penetration(px-i.position[0],pz-i.position[2],layouts.clubmed.find(o=>o.name==='pool')),null);
});

test('three gantries, performer pivot and safety net share exported dimensions',()=>{
  const posts=layouts.clubmed.filter(o=>o.name==='trapeze-post');
  assert.equal(posts.length,6);
  assert.equal(new Set(posts.map(o=>o.position[2])).size,3);
  const flyer=posts.find(o=>Math.abs(o.position[2]-TRAPEZE.pivot[2])<.001);
  assert.ok(Math.abs(flyer.size[1]-TRAPEZE.pivot[1])<.04);
  const net=layouts.clubmed.find(o=>o.name==='safety-net');
  assert.ok(Math.abs(net.position[1]-TRAPEZE.net.height)<.001);
  assert.equal(net.position[0], TRAPEZE.pivot[0]);
  // The entire side-guy envelope ends left of the boarding pier's x=4.8 edge.
  assert.ok(TRAPEZE.pivot[0] + 16 * .545 < 4.8);
});

test('new circus cast is clear of equipment and all silhouettes vary',()=>{
  const objects=obstaclesFor('circus');
  for(const actor of objects.filter(o=>['stage-manager','clown'].includes(o.name))) {
    for(const obstacle of objects.filter(o=>o!==actor))
      assert.equal(penetration(actor.position[0],actor.position[2],obstacle,.3),null,`${actor.name} / ${obstacle.name}`);
  }
  assert.equal(new Set(islands.map(i=>[0,.5,1].map(a=>islandBoundary(i.id,a).toFixed(2)).join(','))).size,9);
});
