'use client';

import React from 'react';
import { DndProvider } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';

import { Plate } from '@udecode/plate/react';

import { useCreateEditor } from '@/components/editor/use-create-editor';
// import { SettingsDialog } from '@/components/editor/settings';
import { Editor, EditorContainer } from '@/components/plate-ui/editor';
import { serializeEditorContent } from '@/lib/editor-content-parser';

type OnChange = React.ComponentProps<typeof Plate>['onChange'];

export function PlateEditor({ initValueMarkdown, saveContent }: { initValueMarkdown?: string, saveContent: (content: string) => void }) {
  const editor = useCreateEditor({
    initValueMarkdown,
  });

  const onChange: OnChange = (options) => {
    const savedValue = serializeEditorContent(options.editor);
    saveContent(savedValue);
  }

  return (
    <DndProvider backend={HTML5Backend}>
      <Plate editor={editor} onChange={onChange}>
        <EditorContainer>
          <Editor variant="demo" />
        </EditorContainer>

        {/* <SettingsDialog /> */}
      </Plate>
    </DndProvider>
  );
}
