'use client';
import { Toaster } from 'sonner';

import { PlateEditor } from '@/components/editor/plate-editor';
import { SettingsProvider } from '@/components/editor/settings';
import { useState } from 'react';

export default function Page() {
  const [content, setContent] = useState('# Hello World');

  const saveContent = (content: string) => {
    setContent(content);
  }

  return (
    <div className="h-screen w-full" data-registry="plate">
      <SettingsProvider>
        <PlateEditor initValueMarkdown={content} saveContent={saveContent} />
      </SettingsProvider>

      <Toaster />
    </div>
  );
}
