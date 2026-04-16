import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';
import { glob } from 'astro/loaders';

const syntheses = defineCollection({
  loader: glob({ base: 'src/content/syntheses', pattern: '**/*.md' }),
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    cluster_id: z.string(),
    summary: z.string(),
    reviewed_at: z.coerce.date(),
    status: z.enum(['approved', 'draft']),
    disclaimer_override: z.string().optional(),
    editor_name: z.string(),
    editor_email: z.string().email(),
    editor_photo: z.string(),
  }),
});

const pages = defineCollection({
  loader: glob({ base: 'src/content/pages', pattern: '**/*.md' }),
  schema: z.object({
    title: z.string(),
    slug: z.string(),
  }),
});

export const collections = {
  syntheses,
  pages,
};
