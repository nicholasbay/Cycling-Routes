import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogDescription,
  DialogTitle,
} from '@/components/ui/dialog';

interface InfoDialogProps {
  isOpen: boolean;
  setIsOpen: (open: boolean) => void;
}

export function InfoDialog({isOpen, setIsOpen}: InfoDialogProps) {
  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      {/* Ensure dialog content appears above map tiles */}
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