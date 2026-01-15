'use client';

import dynamic from 'next/dynamic';
import { ChevronLeft, ChevronUp } from 'lucide-react';
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
        {/* Desktop: Left sidebar */}
        <div className='hidden md:block absolute top-4 left-4 z-1000'>
          <div className='flex gap-2 items-start'>
            <Button
              className='bg-white hover:bg-zinc-100 shadow-lg mt-4'
              variant='outline'
              size='icon'
              onClick={() => setIsPanelVisible(!isPanelVisible)}
            >
              <ChevronLeft className={`h-4 w-4 transition-transform duration-300 ${!isPanelVisible ? 'rotate-180' : ''}`} />
            </Button>

            <div
              className={`
                overflow-hidden transition-all duration-500 ease-in-out
                ${isPanelVisible ? 'w-[50vw] opacity-100 translate-x-0' : 'w-0 opacity-0 -translate-x-50 pointer-events-none'}
              `}
            >
              <div className='space-y-2 max-h-[calc(100vh-2rem)] overflow-y-auto'>
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
            </div>
          </div>
        </div>

        {/* Mobile: Top drawer */}
        <div className='md:hidden absolute top-0 left-0 right-0 z-1000'>
          <div className='flex flex-col gap-2'>
            <Button
              className='bg-white hover:bg-zinc-100 shadow-lg rounded-b-lg rounded-t-none w-full'
              variant='outline'
              onClick={() => setIsPanelVisible(!isPanelVisible)}
            >
              <ChevronUp className={`h-4 w-4 transition-transform duration-300 ${!isPanelVisible ? 'rotate-180' : ''}`} />
            </Button>

            <div
              className={`
                transition-all duration-500 ease-in-out
                ${isPanelVisible ? 'max-h-[80vh] opacity-100 translate-y-0' : 'max-h-0 opacity-0 -translate-y-50 pointer-events-none'}
              `}
            >
              <div className='space-y-2 overflow-y-auto max-h-[80vh]'>
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
            </div>
          </div>
        </div>

        <Map userPosition={position} />
      </div>
    </div>
  );
}
