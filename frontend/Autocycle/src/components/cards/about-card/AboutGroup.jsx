'use client';
import PropTypes from 'prop-types';
import AvatarGroup from '@mui/material/AvatarGroup';
import { Grid, Stack, Box, Avatar, Typography, Link } from '@mui/material';
import Image from 'next/image';
// @project
import GetImagePath from '@/utils/GetImagePath';
import SvgIcon from '@/components/SvgIcon';
// @types

// @assets


/***************************  CARD - About GROUP  ***************************/

export default function AboutGroup({ review, avatarGroups}) {
 
  return (
    <Stack sx={{ gap: 2, }}>
      <Stack sx={{ gap: 1 }}>
        <Grid container spacing={2} justifyContent="center">
          {avatarGroups.map((item, index) => (
            <Grid item xs={12} sm={4} md={2.4} key={index}>
              <Stack alignItems="center" spacing={1}>
                <Avatar
                  src={GetImagePath(item.avatar)}
                  alt={item.name}
                  imgProps={{ loading: 'lazy' }}
                  sx={{ width: { xs: 48, md: 56 }, height: { xs: 48, md: 56 }, border: '1px solid', borderColor: 'divider' }}
                />
                <Box textAlign="center">
                  <Typography variant="subtitle2" sx={{ fontSize: { xs: '0.875rem', md: '1rem' }, color: 'text.primary' }}>
                   {item.name}
                  </Typography>
                  <Typography variant="body2" sx={{ fontSize: { xs: '0.75rem', md: '0.875rem' }, color: 'text.secondary' }}>
                  {item.title}
                  </Typography>
                </Box>
                <Link
                  href={item.linkedinUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  sx={{ display: 'flex', alignItems: 'center', color: '#5BC80C', '&:hover': { color: '#0A66C2' } }}
                >
                  <SvgIcon name={'tabler-brand-linkedin'} size={16} color='#5BC80C' />
                  <Typography variant="body2" sx={{ fontSize: '0.75rem' }}>
                    LinkedIn
                  </Typography>
                </Link>
              </Stack>
            </Grid>
          ))}
        </Grid>
      </Stack>
    </Stack>
  );
}

AboutGroup.propTypes = { review: PropTypes.string, avatarGroups: PropTypes.array };
