/***************************  DEFAULT / AI THEME - PALETTE  ***************************/

export default function palette() {
  const textPrimary = '#1A1C1E'; // AI/neutral/10 - on surface
  const textSecondary = '#4A4A4A'; // AI/neutral variant/30 - on surface variant (using Charcoal Grey)
  const divider = '#D9D9D9'; // AI/neutral variant/80 - outline variant (using Soft Grey)
  const background = '#F5F5F5'; // Using Warm White

  const lightPalette = {
    primary: {
      lighter: '#CAFFA3', // AI/primary/90 - primary container / primary fixed (Light Green)
      light: '#92E066', // AI/primary/80 - primary fixed dim (derived intermediate green)
      main: '#5BC80C', // AI/primary/40 - primary (Vibrant Green)
      dark: '#3A7B05', // AI/primary/30 - on primary fixed variant (Deep Green)
      darker: '#1A3D02' // AI/primary/10 - on primary container / on primary fixed (derived darkest green)
    },
    secondary: {
      lighter: '#D3E4D3', // AI/secondary/90 - secondary container / secondary fixed (derived lighter Muted Green-Grey)
      light: '#B7C8B7', // AI/secondary/80 - secondary fixed dim (derived light Muted Green-Grey)
      main: '#A3BFA3', // AI/secondary/40 - secondary (Muted Green-Grey)
      dark: '#718871', // AI/secondary/30 - on secondary fixed variant (derived darker Muted Green-Grey)
      darker: '#3F4E3F' // AI/secondary/10 - on secondary container / on secondary fixed (derived darkest Muted Green-Grey)
    },
    grey: {
      50: '#F5F5F5', // AI/neutral/98 - surface / surface bright (Warm White)
      100: '#F1F4F1', // AI/neutral/96 - surface container low (derived near Warm White)
      200: '#EBEFEB', // AI/neutral/94 - surface container (derived neutral)
      300: '#E6E9E6', // AI/neutral/92 - surface container high (derived neutral)
      400: '#D9D9D9', // AI/neutral/90 - surface container highest (Soft Grey)
      500: '#CED2CE', // AI/neutral/87 - surface dim (derived near Soft Grey)
      600: divider, // AI/neutral variant/80 - outline variant (Soft Grey)
      700: '#727872', // AI/neutral variant/50 - outline (derived neutral)
      800: textSecondary, // AI/neutral variant/30 - on surface variant (Charcoal Grey)
      900: textPrimary // AI/neutral/10 - on surface
    },
    text: {
      primary: textPrimary, // AI/neutral/10 - on surface
      secondary: textSecondary // AI/neutral variant/30 - on surface variant
    },
    divider,
    background: {
      default: background
    }
  };

  return {
    ...lightPalette
  };
}