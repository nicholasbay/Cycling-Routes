'use client';

import dynamic from 'next/dynamic';
import { useMemo } from 'react';

import { Loading } from '@/components/Loading';
import { useUserPosition } from '@/hooks/useUserPosition';

export default function Home() {
  const { position } = useUserPosition();

  const Map = useMemo(() => dynamic(
    () => import('@/components/Map'),
    { 
      loading: () => <Loading
        className="flex flex-row items-center justify-center h-screen gap-4"
        message="Loading map..."
        iconSize={48}
      />,
      ssr: false
    }
  ), []);

  return (
    <div className='flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black'>
      <div className='w-screen h-screen'>
        <Map userPosition={position} />
      </div>
    </div>
  );
}
