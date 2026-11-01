import { Canvas } from '@react-three/fiber';
import { Scenery } from './Scenery.jsx';
import { Journey } from '../journey/Journey.jsx';

/** Canvas boundary kept separate so the readable portfolio never needs WebGL. */
export const World = (props) => <Canvas
  shadows dpr={[1, 1.5]} camera={{ position: [34, 27, 43], fov: 46, near: 0.1, far: 220 }}
  gl={{ antialias: true, powerPreference: 'high-performance' }}
  fallback={<div className="canvas-fallback">La 3D n’est pas disponible sur cet appareil. Retrouvez toutes les escales dans le carnet de voyage.</div>}
>
  <color attach="background" args={[props.night ? '#263e50' : '#bdd4d2']} />
  <fog attach="fog" args={[props.night ? '#263e50' : '#bdd4d2', 65, 160]} />
  <hemisphereLight args={[props.night ? '#a9b7df' : '#fff4dc', '#6b8075', props.night ? 1 : 1.3]} />
  <directionalLight position={[-20, 35, 20]} intensity={props.night ? 1 : 2} color={props.night ? '#d3dcff' : '#ffe1af'} castShadow shadow-mapSize={[2048, 2048]} shadow-camera-left={-65} shadow-camera-right={65} shadow-camera-top={65} shadow-camera-bottom={-65} shadow-camera-far={120} shadow-bias={-0.001} />
  <Scenery night={props.night} reduced={props.reduced} onExhibit={props.onExhibit} showLabels={props.mode !== 'overview'} />
  <Journey {...props} />
</Canvas>;
