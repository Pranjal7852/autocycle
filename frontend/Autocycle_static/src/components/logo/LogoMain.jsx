'use client';

// @mui
import { useTheme } from '@mui/material/styles';
import CardMedia from '@mui/material/CardMedia';
import Box from '@mui/material/Box';

// @project
import branding from '@/branding.json';

/***************************  LOGO - MAIN  ***************************/

export default function LogoMain() {
  const theme = useTheme();
  const logoMainPath = branding.logo.main;
  console.log("test", theme)
  return logoMainPath ? (
    <CardMedia src={logoMainPath} component="img" alt="logo" sx={{ width: { xs: 112, lg: 140 } }} loading="lazy" />
  ) : (
    <Box sx={{ width: { xs: 112, lg: 140 }, height: { xs: 22, lg: 26 } }}>
        <span style={{
          fontSize: '1.5rem',         // Bigger than default (or use theme.typography.h6)
          fontWeight: 'bold',         // Makes it stand out
          letterSpacing: 1,           // Slight spacing between letters
          color: `${theme.palette.primary.main}`,      // Theme-aware color
          textTransform: 'uppercase', // Optional, gives a clean branded look
          cursor: 'pointer',          // Looks clickable
          userSelect: 'none',         // Prevents accidental text selection  }}>
        }}> AutoCycle
    </span>
    </Box>
  );
}
