'use client';

import * as React from 'react';

import { MessageSquareTextIcon } from 'lucide-react';
import { useEditorRef } from 'platejs/react';

import { commentPlugin } from '@/components/editor/plugins/comment-kit';

import { ToolbarButton } from './toolbar';

// COMMENT FEATURE DISABLED - Comment out toolbar button functionality
export function CommentToolbarButton() {
  // COMMENT FEATURE DISABLED - Return null to hide the component entirely
  return null;

  /* ORIGINAL COMMENT TOOLBAR BUTTON - COMMENTED OUT
  const editor = useEditorRef();

  return (
    <ToolbarButton
      onClick={() => {
        editor.getTransforms(commentPlugin).comment.setDraft();
      }}
      data-plate-prevent-overlay
      tooltip="Comment"
    >
      <MessageSquareTextIcon />
    </ToolbarButton>
  );
  */
}
