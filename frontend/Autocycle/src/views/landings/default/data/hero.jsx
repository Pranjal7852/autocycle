// @mui
import CardMedia from '@mui/material/CardMedia';
import Chip from '@mui/material/Chip';
import Typography from '@mui/material/Typography';
import { SECTION_PATH } from '@/path';

export const hero = {
  chip: {
    label: (
      <>
        <Typography variant="caption" sx={{ color: 'text.secondary' }}>
          One Platform, Endless
        </Typography>
        <Chip
          label={
            <Typography variant="caption" sx={{ color: 'primary.darker' }}>
              ♻️ Recyling
            </Typography>
          }
          sx={{ height: 24, bgcolor: 'primary.lighter', mr: -1, ml: 0.75, '& .MuiChip-label': { px: 1.25 } }}
        />
      </>
    )
  },
  headLine: 'Catch today the material flows of tomorrow.',
  captionLine: 'Bridging the Gap Between Your Sourcing Needs and OEM End-of-Life Products',
  primaryBtn: { children: 'Our Solution', href: SECTION_PATH },
  videoSrc: 'https://d2elhhoq00m1pj.cloudfront.net/saasable-intro.mp4',
  videoThumbnail: '/assets/videos/thumbnails/intro-thumbnail.png',
  listData: [
    { image: '/assets/images/shared/react.svg', title: 'React 18' },
    { image: '/assets/images/shared/next-js.svg', title: 'Next.js' },
    { image: '/assets/images/shared/material-ui.svg', title: 'Material UI v7' },
    { image: '/assets/images/shared/typescript.svg', title: 'TypeScript' },
    { image: '/assets/images/shared/javascript.svg', title: 'JavaScript' },
    { image: '/assets/images/shared/m3.svg', title: 'Material 3' },
    { image: '/assets/images/shared/figma.svg', title: 'Figma' }
  ]
};
