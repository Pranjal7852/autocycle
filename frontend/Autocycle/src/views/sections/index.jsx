'use client';
import { useEffect, useState } from 'react';

// @next
import NextLink from 'next/link';

// @mui
import { alpha, useTheme } from '@mui/material/styles';


// @third-party
import { motion } from 'framer-motion';

// @project
import ContainerWrapper from '@/components/ContainerWrapper';
import { GraphicsCard } from '@/components/cards';
import SectionHero from '@/components/SectionHero';
import SvgIcon from '@/components/SvgIcon';
import {
  benefit,
  clientele,
  cta4,
  cta5,
  faq,
  feature20,
  feature21,
  feature18,
  hero,
  integration,
  other,
  pricing,
  testimonial
} from '@/views/landings/default/data';
import { Clientele3 } from '@/blocks/clientele';
import { Testimonial10 } from '@/blocks/testimonial';
import { Cta4, Cta5 } from '@/blocks/cta';
import useFocusWithin from '@/hooks/useFocusWithin';
import { PAGE_PATH } from '@/path';
import { generateFocusVisibleStyles } from '@/utils/CommonFocusStyle';
import GetImagePath from '@/utils/GetImagePath';

// @assets
import Background from '@/images/graphics/Background';
import Wave from '@/images/graphics/Wave';
import Gallery from './Gallery';
import GallerySlider from '@/app/about/GallerySlider/GallerySlider';


/***************************  SECTIONS LAYOUT  ***************************/

export default function Sections() {
  const theme = useTheme();
  


  const isFocusWithin = useFocusWithin();

  return (
    <>
      <SectionHero heading="Read our Story" search={false} offer />
      <ContainerWrapper>
       
      <GallerySlider></GallerySlider>
      <Testimonial10  {...testimonial} />
       {/* <Clientele3 {...clientele} /> */}
        <Cta5 {...cta5} />
      </ContainerWrapper>
    </>
  );
}
