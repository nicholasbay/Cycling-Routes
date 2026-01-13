'use client';

import dynamic from 'next/dynamic';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { useMemo, useState } from 'react';

import { Button } from '@/components/ui/button';
import { Loading } from '@/components/Loading';
import { InputPanel } from '@/components/InputPanel';
import { RoutesPanel } from '@/components/RoutesPanel';
import { useRoutes } from '@/contexts/RoutesContext';
import { useUserPosition } from '@/hooks/useUserPosition';
import { Location } from '@/types';
import { fetchRoute } from '@/services';

const DEFAULT_INTERVAL_MINS = 30;

export default function Home() {
  const { position } = useUserPosition();
  const { routes, setRoutes, clearRoutes, setLoading, setError } = useRoutes();

  const [start, setStart] = useState<Location | null>(null);
  const [end, setEnd] = useState<Location | null>(null);
  const [intervalMins, setIntervalMins] = useState<number>(DEFAULT_INTERVAL_MINS);
  const [isPanelVisible, setIsPanelVisible] = useState<boolean>(false);

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

  const handleSubmit = async () => {
    if (!start || !end) return;

    setLoading(true);
    setError(null);
    clearRoutes();  // Clear previous routes

    try {
      const routeResult = await fetchRoute(start, end, intervalMins);
      setRoutes(routeResult);
      console.log(routeResult)
    } catch (error) {
      console.error('Error fetching route:', error);
    } finally {
      setLoading(false);
    };
  };

  return (
    <div className='flex flex-col min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black'>
      <div className='h-screen w-screen relative'>
        <div className='absolute top-4 left-4 z-1000 flex flex-col md:flex-row gap-2 items-start'>
          <Button
            className='bg-white hover:bg-zinc-100 shadow-lg mt-4'
            variant='outline'
            size='icon'
            onClick={() => setIsPanelVisible(!isPanelVisible)}
          >
            {isPanelVisible ? <ChevronLeft className='h-4 w-4' /> : <ChevronRight className='h-4 w-4' />}
          </Button>


          {isPanelVisible && (
            <div className='space-y-2'>
              <InputPanel
                onStartSelect={(location) => setStart(location)}
                onEndSelect={(location) => setEnd(location)}
                onIntervalChange={(value) => setIntervalMins(value)}
                onSubmit={handleSubmit}
                startPoint={start}
                endPoint={end}
                intervalMins={intervalMins}
              />
              <RoutesPanel routes={routes} />
            </div>
          )}
        </div>
        <Map userPosition={position} />
      </div>
    </div>
  );
}
