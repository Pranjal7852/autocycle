// @project
import SvgIcon from '@/components/SvgIcon';
import { DOCS_URL } from '@/path';

export const integration = {
  headLine: 'Tailored for Specific Industries',
  captionLine: 'From construction to cosmetics, explore how automotive recycled plastic can serve a variety of sectors, transitioning towards circular economy.',
  primaryBtn: {
    children: 'Documentation',
    startIcon: <SvgIcon name="tabler-help" color="background.default" />,
    href: DOCS_URL,
    target: '_blank',
    rel: 'noopener noreferrer'
  },
  tagList: [
    { label: 'Automotivez' },
    { label: 'Building and Construction' },
    { label: 'Logistics & Packaging' },
    { label: 'Sports and Leisure' },
    { label: 'Toy & Game Manufacturing' },
    { label: 'Furniture and Home Goods' },
    { label: 'Tooling and Industrial Equipment' },
    { label: 'Consumer Goods' },
    { label: 'Beauty and personal care' },
    { label: 'Landscaping and Agriculture' },
    { label: 'Consumer Electronics' },
    { label: 'Education & Institutional Supplies' },
  ]
};
