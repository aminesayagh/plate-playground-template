import { SlateEditor } from "@udecode/plate";
import { deserializeMd, serializeMd, deserializeInlineMd } from "@udecode/plate-markdown";
import { z } from "zod";

type UnknownObject = Record<string, unknown>;

type TText = {
    text: string;
} & UnknownObject;

type Descendant = TElement | TText;

type TElement = {
    children: Descendant[];
    type: string;
} & UnknownObject;

type EditorContent = TElement[];

type UnknownEditorContent = EditorContent | string;

const textSchema = z.object({
    text: z.string(),
});

const elementSchema: z.ZodType<TElement> = z.lazy(() =>
    z.object({
        children: z.array(z.union([textSchema, elementSchema])),
        type: z.string(),
    })
);



export const deserializeEditorContent = (editor: SlateEditor, content: string): EditorContent => {
    return deserializeMd(editor, content);
}

export const serializeEditorContent = (editor: SlateEditor): string => {
    return serializeMd(editor);
}

