import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const syntheses = defineCollection({
  loader: glob({ base: '../content/syntheses', pattern: '**/*.md' }),
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    cluster_id: z.string(),
    summary: z.string(),
    reviewed_at: z.coerce.date(),
    status: z.enum(['approved', 'draft']),
    order: z.number().int(),
    disclaimer_override: z.string().optional(),
    editor_name: z.string(),
    editor_email: z.string().email(),
    editor_photo: z.string(),
    editor_contact_sentence: z.string(),
  }),
});

const featured = defineCollection({
  loader: glob({ base: '../content/featured', pattern: '**/*.md' }),
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    summary: z.string(),
    reviewed_at: z.coerce.date(),
    disclaimer_override: z.string().optional(),
  }),
});

const pages = defineCollection({
  loader: glob({ base: '../content/pages', pattern: '**/*.md' }),
  schema: z.object({
    title: z.string(),
    slug: z.string(),
  }),
});

export const collections = {
  syntheses,
  featured,
  pages,
};
