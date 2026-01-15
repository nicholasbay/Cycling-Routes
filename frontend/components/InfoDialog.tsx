import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogOverlay,
  DialogTitle
} from '@/components/ui/dialog';

interface InfoDialogProps {
  isOpen: boolean;
  setIsOpen: (open: boolean) => void;
}

export function InfoDialog({isOpen, setIsOpen}: InfoDialogProps) {
  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      {/* Ensure dialog overlay and content appear above map tiles */}
      <DialogOverlay className='z-1000' />

      <DialogContent className='z-1000'>
        <DialogHeader>
          <DialogTitle>PitStop</DialogTitle>
          <DialogDescription>
            Plan cycling routes that stay within bike-sharing time limits.
          </DialogDescription>
        </DialogHeader>

        <div className='max-h-[50dvh] overflow-y-auto space-y-2'>
          <h2 className='text-lg font-semibold'>How to Use</h2>
          <ol className='list-decimal list-inside space-y-1'>
            <li>Enter a start location in the "Start Location" field.</li>
            <li>Enter an end location in the "End Location" field.</li>
            <li>Specify the desired interval (in minutes) between parking spots.</li>
            <li>Click the button to find routes with the intermediate parking spots.</li>
          </ol>

          <h2 className='text-lg font-semibold'>Icons</h2>
          <ul className='list-none list-inside space-y-1'>
            <li><img src='/icons/location-blue.png' alt="Start Location" className='w-8 h-8 inline-block mr-2'/>Start Location</li>
            <li><img src='/icons/location-red.png' alt="End Location" className='w-8 h-8 inline-block mr-2'/>End Location</li>
            <li><img src='/icons/bike-parking.png' alt="Parking Spot" className='w-8 h-8 inline-block mr-2'/>Parking Spot</li>
            <li><img src='/icons/position.png' alt="Current Location" className='w-8 h-8 inline-block mr-2'/>Current Location</li>
          </ul>
        </div>
      </DialogContent>
    </Dialog>
  );
}