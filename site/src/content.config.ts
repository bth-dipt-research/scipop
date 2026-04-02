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
  }),
});

const featured = defineCollection({
  loader: glob({ base: '../content/featured', pattern: '**/*.md' }),
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    summary: z.string(),
    reviewed_at: z.coerce.date(),
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
