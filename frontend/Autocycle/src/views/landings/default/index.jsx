'use client';

// @project
import { Feature18, Feature20 } from '@/blocks/feature';
import { Hero17 } from '@/blocks/hero';
import { Faq6 } from '@/blocks/faq';
import LazySection from '@/components/LazySection';
import useDataThemeMode from '@/hooks/useDataThemeMode';

// @data
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
} from './data';
import { Cta4, Cta5 } from '@/blocks/cta';
import Cta from '@/views/sections/Cta';

/***************************  PAGE - MAIN  ***************************/

export default function Main() {
  useDataThemeMode();

  return (
    <>
      <Hero17 {...hero} />
      {/* Feature 1 */}
      <Feature18 {...feature18} />
      <Feature20 {...feature20} /> 

      <LazySection
        sections={[

          { importFunc: () => import('@/blocks/integration').then((module) => ({ default: module.Integration2 })), props: integration },
          
        ]}
        offset="200px"
      />

      
      

     
      <Faq6 {...faq} />
      <LazySection
        sections={[
          { importFunc: () => import('@/blocks/cta').then((module) => ({ default: module.Cta4 })), props: cta4 }
        ]}
        offset="200px"
      />
      <Cta5 {...cta5} />
    </>
  );
}
