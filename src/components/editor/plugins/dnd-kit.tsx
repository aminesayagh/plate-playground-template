'use client';

import { DndProvider } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';

import { DndPlugin } from '@platejs/dnd';
import { PlaceholderPlugin } from '@platejs/media/react';

import { BlockDraggable } from '@/components/ui/block-draggable';

// UPLOAD FEATURE DISABLED - Comment out file drop functionality but keep drag and drop for blocks
export const DndKit = [
  DndPlugin.configure({
    options: {
      enableScroller: true,
      // UPLOAD FEATURE DISABLED - Comment out file drop handler
      // onDropFiles: ({ dragItem, editor, target }) => {
      //   editor
      //     .getTransforms(PlaceholderPlugin)
      //     .insert.media(dragItem.files, { at: target, nextBlock: false });
      // },
      onDropFiles: ({ dragItem, editor, target }) => {
        console.warn('File drop functionality is currently disabled');
        // Optional: Show user feedback
        // toast.error('File upload is currently disabled');
      },
    },
    render: {
      aboveNodes: BlockDraggable,
      aboveSlate: ({ children }) => (
        <DndProvider backend={HTML5Backend}>{children}</DndProvider>
      ),
    },
  }),
];
