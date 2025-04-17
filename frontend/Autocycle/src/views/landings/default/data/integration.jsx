// @project
import SvgIcon from '@/components/SvgIcon';
import { DOCS_URL } from '@/path';

export const integration = {
  headLine: 'Built for Circular Innovation Across Industries',
  captionLine: "From construction to consumer tech, our network of high-quality post-use plastics serves industries looking to create smarter, more responsible products.",
  primaryBtn: {
    children: 'Documentation',
    startIcon: <SvgIcon name="tabler-help" color="background.default" />,
    href: DOCS_URL,
    target: '_blank',
    rel: 'noopener noreferrer'
  },
  tagList: [
    { label: 'Automotive' },
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
