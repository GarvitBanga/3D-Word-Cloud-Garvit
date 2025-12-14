import React, { useMemo, useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { Text, Float, Stars } from '@react-three/drei';
import * as THREE from 'three';
import type { Topic } from '../api';

interface WordCloudProps {
    words: Topic[];
}

const Word = ({ word, weight, position, color }: { word: string; weight: number; position: [number, number, number]; color: string }) => {
    const meshRef = useRef<THREE.Mesh>(null);
    useFrame((state) => {
        if (meshRef.current) {
            meshRef.current.lookAt(state.camera.position);
        }
    });
    const fontSize = Math.max(0.5, weight / 2);
    return (
        <Float speed={2} rotationIntensity={0.5} floatIntensity={0.5}>
            <Text
                ref={meshRef}
                position={position}
                fontSize={fontSize}
                color={color}
                anchorX="center"
                anchorY="middle"
            >
                {word}
            </Text>
        </Float>
    );
};

export const WordCloud: React.FC<WordCloudProps> = ({ words }) => {
    const groupRef = useRef<THREE.Group>(null);
    useFrame(() => {
        if (groupRef.current) groupRef.current.rotation.y += 0.001;
    })
    const wordComponents = useMemo(() => {
        const tempWords: React.JSX.Element[] = [];
        const sphereRadius = 15;
        const goldenRatio = (1 + Math.sqrt(5)) / 2;
        const angleIncrement = Math.PI * 2 * goldenRatio;
        words.forEach((item, i) => {
            const t = i / words.length;
            const inclination = Math.acos(1 - 2 * t);
            const azimuth = angleIncrement * i;
            const x = sphereRadius * Math.sin(inclination) * Math.cos(azimuth);
            const y = sphereRadius * Math.sin(inclination) * Math.sin(azimuth);
            const z = sphereRadius * Math.cos(inclination);
            const color = new THREE.Color().setHSL(Math.random(), 0.8, 0.6).getStyle();
            
            tempWords.push(
                <Word key={item.word} word={item.word} weight={item.weight} position={[x, y, z]} color={color} />
            );
        });
        return tempWords;
    }, [words]);

    return (
        <>
            <ambientLight intensity={0.5} />
            <pointLight position={[10, 10, 10]} />
            <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />
            <group ref={groupRef}>{wordComponents}</group>
        </>
    );
};
