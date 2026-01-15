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
          <DialogTitle>Title</DialogTitle>
          <DialogDescription>Description</DialogDescription>
        </DialogHeader>

        <div>
          Content
        </div>
      </DialogContent>
    </Dialog>
  );
}