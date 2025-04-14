'use client';
import React from 'react';
import Image from 'next/image';
import { Container, Grid, Stack, Box, Typography } from '@mui/material';
import { AboutGroup } from '@/components/cards/about-card';
import Wave from '@/images/graphics/Wave';
// Define gallery items (replace with your data)
const galleryItems = [
    {
        id: 1,
        
        description: 'BMW AG, Recycling & Demontage Zentrum (RDZ): setting the pace on the path to circularity for 30 years.',
        image: '/assets/images/team/team3.JPG', // Replace with your image path
    },
    {
        id: 2,
       
        description: 'Circular Economy @ Collab Munich Event.',
        image: '/assets/images/team/team2.png',
    },
    {
        id: 3,
        
        description: 'BMW recycle plant Visit at Garching, Munchen',
        image: '/assets/images/team/team1.png',
    },
    // Add more items as needed
];
const sampleData = {
    review: 'Team: AutoCycle',
    avatarGroups: [
        {
            avatar: '/assets/images/user/avatar3.png',
            name: 'Casimir Uhlig',
            title: 'Product Manager',
            linkedinUrl: 'https://www.linkedin.com/in/casimiruhlig/',
        },
        {
            avatar: '/assets/images/user/avatar1.png',
            name: 'Varvara Sharova',
            title: 'Marketing Manager',
            linkedinUrl: 'https://www.linkedin.com/in/vvsharova/',
        },
        {
            avatar: '/assets/images/user/avatar4.png',
            name: 'Nihan Öztürk',
            title: 'Product Designer',
            linkedinUrl: 'https://www.linkedin.com/in/nihanozturk/',
        },
        {
            avatar: '/assets/images/user/avatar2.png',
            name: 'Nidhi Sonavane ',
            title: 'AI Engineeer',
            linkedinUrl: 'https://www.linkedin.com/in/nidhi-sonavane/',
        },
        {
            avatar: '/assets/images/user/avatar5.png',
            name: 'Pranjal Goyal',
            title: 'Software Engineer',
            linkedinUrl: 'https://www.linkedin.com/in/pranjal-goyal-42a7a55b/',
        },
    ],
};

const GallerySection: React.FC = () => {
    return (
       
            <Container maxWidth="md">
                {/* Header */}

            <Box sx={{ pb: 6, textAlign: 'center', mt: 6 }}>
                <Typography
                    variant="h3"
                    sx={{ fontSize: { xs: '1.75rem', md: '1.125rem' }, fontWeight: "normal", color: '4B5563' }}
                >
                    Our journey began with a simple yet critical question:

                </Typography>
                <Typography
                    variant="body1"
                    sx={{ mt: 1, fontSize: { xs: '1.75rem', md: '2.125rem' }, color: '#111827', lineHeight: '1.55' }}
                >

                    How can we help ensure that materials—especially plastics used in the automotive industry—are given a second life, rather than ending up in incineration or landfills?
                </Typography>
                <Typography
                    variant="h3"
                    sx={{ fontSize: { xs: '1.75rem', md: '1.125rem' }, fontWeight: "normal", color: '4B5563', mt: 3 }}
                >
                    This question inspired us to develop a digital solution that supports the recycling of automotive plastics.


                </Typography>
            </Box>
            {/* Image Grid */}
            <Grid container spacing={2} justifyContent="center">
                {/* Portrait Image (Left) */}
                <Grid item xs={12} md={6}>
                    <Box sx={{ maxWidth: 350, mx: 'auto' }}>
                        <Box
                            sx={{
                                position: 'relative',
                                width: '100%',
                                aspectRatio: '9/16',
                                borderRadius: '12px',
                                overflow: 'hidden',
                            }}
                        >
                            <Image
                                src={galleryItems[0].image}
                                alt={galleryItems[0].title}
                                fill
                                style={{ objectFit: 'cover', transform: 'scale(1.05)' }}
                                priority
                            />
                        </Box>
                        <Box sx={{ mt: 3, textAlign: 'center' }}>
                            <Typography variant="body2" sx={{ fontSize: '0.875rem', color: '#4B5563', mt: 0.5 }}>
                                {galleryItems[0].description}
                            </Typography>
                        </Box>
                    </Box>
                </Grid>

                {/* Landscape Images (Right, Stacked) */}
                <Grid
                    item
                    xs={12}
                    md={6}
                    sx={{
                        display: 'flex',
                        alignItems: 'center', // Vertically center the Stack
                        justifyContent: 'center',
                    }}
                >
                    <Stack direction="column" spacing={2} sx={{ maxWidth: 350, mx: 'auto' }}>
                        {/* Top Landscape */}
                        <Box>
                            <Box
                                sx={{
                                    position: 'relative',
                                    width: '100%',
                                    aspectRatio: '16/9',
                                    borderRadius: '12px',
                                    overflow: 'hidden',
                                }}
                            >
                                <Image
                                    src={galleryItems[1].image}
                                    alt={galleryItems[1].title}
                                    fill
                                    style={{ objectFit: 'cover', transform: 'scale(1.05)' }}
                                    priority
                                />
                            </Box>
                            <Box sx={{ mt: 3, textAlign: 'center' }}>

                                <Typography variant="body2" sx={{ fontSize: '0.875rem', color: '#4B5563', mt: 0.5 }}>
                                    {galleryItems[1].description}
                                </Typography>
                            </Box>
                        </Box>

                        {/* Bottom Landscape */}
                        <Box>
                            <Box
                                sx={{
                                    position: 'relative',
                                    width: '100%',
                                    aspectRatio: '16/9',
                                    borderRadius: '12px',
                                    overflow: 'hidden',
                                }}
                            >
                                <Image
                                    src={galleryItems[2].image}
                                    alt={galleryItems[2].title}
                                    fill
                                    style={{ objectFit: 'cover', transform: 'scale(1.05)' }}
                                />
                            </Box>
                            <Box sx={{ mt: 3, textAlign: 'center' }}>
                                <Typography variant="h6" sx={{ fontSize: '1.125rem', fontWeight: 'medium', color: '#111827' }}>
                                    {galleryItems[2].title}
                                </Typography>
                                <Typography variant="body2" sx={{ fontSize: '0.875rem', color: '#4B5563', mt: 0.5 }}>
                                    {galleryItems[2].description}
                                </Typography>
                            </Box>
                        </Box>
                    </Stack>
                </Grid>
            </Grid>

            <Box sx={{ textAlign: 'center', mt: 6, mb: 6 }}>
                <Typography
                    variant="h3"
                    sx={{ fontSize: { xs: '1.75rem', md: '1.125rem' }, fontWeight: "normal", color: '4B5563', mt: 3 }}
                >
                    With diverse professional and cultural backgrounds, our team brings together expertise in design, artificial intelligence, engineering, marketing, and business. Together, we’re tackling this challenge head-on. We believe technology can bridge the gap between plastic part manufacturers and OEMs, turning sustainability into a win-win situation for all parties involved.
                </Typography>
            </Box>
           
            <Box sx={{ textAlign: 'center', mt: 6 }}>

                <Typography
                    variant="body1"
                    sx={{ mt: 1, fontSize: { xs: '1.75rem', md: '2.125rem' }, color: '#111827', lineHeight: '1.75' }}
                >

                    We are a passionate team formed at the Digital Product School, united by a shared mission: to make future sourcing smarter, more sustainable, and truly circular.

                </Typography>


            </Box>
            
            <Box component="main" sx={{ maxWidth: '100vw', overflowX: 'hidden', mt: 6, mb: 6 }}>
                <AboutGroup review={sampleData.review} avatarGroups={sampleData.avatarGroups} />
                <Wave />
            </Box>
        
         
          
              

            
           
         
            </Container>
        
    );
};

export default GallerySection;
