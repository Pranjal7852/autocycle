'use client';
import PropTypes from 'prop-types';
import {useState, useEffect} from 'react'
import { SECTION_PATH, BUY_NOW_URL, ADMIN_PATH, DOCS_URL } from '@/path';
// @mui


import { useTheme } from '@mui/material/styles';
import Button from '@mui/material/Button';
import Chip from '@mui/material/Chip';
import Divider from '@mui/material/Divider';
import Grid from '@mui/material/Grid';
import OutlinedInput from '@mui/material/OutlinedInput';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

import Tab from '@mui/material/Tab';
import TabContext from '@mui/lab/TabContext';
import TabList from '@mui/lab/TabList';
import TabPanel from '@mui/lab/TabPanel';
import SvgIcon from '@/components/SvgIcon';
import GraphicsImage from '@/components/GraphicsImage';
const linkProps = { target: '_blank', rel: 'noopener noreferrer' };
// @third-party
import { motion } from 'framer-motion';

// @project
import ButtonAnimationWrapper from '@/components/ButtonAnimationWrapper';
import ContainerWrapper from '@/components/ContainerWrapper';
import { GraphicsCard } from '@/components/cards';
import { ProfileGroup } from '@/components/cards/about-card';
import LogoWatermark from '@/components/logo/LogoWatermark';
import Typeset from '@/components/Typeset';

import { SECTION_COMMON_PY } from '@/utils/constant';

// @assets
import Wave from '@/images/graphics/Wave';

/***************************  CALL TO ACTION - 5  ***************************/

const CalendlyEmbed = ({ url }) => {
  useEffect(() => {
    const head = document.querySelector("head");
    const script = document.createElement("script");
    script.setAttribute(
      "src",
      "https://assets.calendly.com/assets/external/widget.js"
    );
    head.appendChild(script);
  }, []);

  return (
    <div
      className="calendly-inline-widget"
      data-url={url}
      style={{ minHeight: "750px", width: "100%", margin: "2rem auto", border: "2px solid #fff" }}
    ></div>
  );
};

export default function Cta5({ heading, caption, label, input = false, primaryBtn, secondaryBtn, description, saleData, profileGroups }) {
  const theme = useTheme();
  useEffect(() => {
    const script = document.createElement("script");
    script.src = "https://assets.calendly.com/assets/external/widget.js";
    script.async = true;
    document.body.appendChild(script);
  }, []);
  const boxPadding = { xs: 3, md: 5 };
  const imagePadding = { xs: 3, sm: 4, md: 5 };
  const [value, setValue] = useState('1');
  const handleChange = (event, newValue) => {
    setValue(newValue);
  };
  const topics = [
      {
        icon: 'tabler-contract',
      title: 'Fill Out Contact Form',
        title2: 'Leverage Power of Material UI Components',
        description: 'The power and flexibility of Material UI components in admin template',
        image: {
          light: '/assets/images/graphics/default/admin-dashboard.png',
          dark: '/assets/images/graphics/default/admin-dashboard-dark.png'
        },
      },
      {
        icon: 'tabler-video-plus',
        title: 'Book Discovery Call',
        title2: 'Flexible Theming Options',
        description: 'Tailor themes effortlessly with MUI 7 robust theming system.',
        image: '/assets/images/graphics/default/admin-dashboard-2.png',
        list: [
          { primary: 'Easy options for Theming' },
          { primary: 'Layout Options' },
          { primary: 'Color Presets tailored to your Web Apps' },
          { primary: 'Consistency in Design' }
        ],
        actionBtn: { children: 'View Dashboard', href: ADMIN_PATH, ...linkProps },
        actionBtn2: { children: 'Docs', href: DOCS_URL, ...linkProps }
      },
    ]
  return (
    <ContainerWrapper sx={{ py: SECTION_COMMON_PY }}>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{
          duration: 0.5,
          delay: 0.4
        }}
      >
        <Grid container spacing={1.5}>
         
          <Grid size={{ xs: 12, sm: 12, md: 12 }} id="contact">
            <GraphicsCard sx={{ position: 'relative' }}>
              <Stack
                sx={{ alignItems: 'flex-start', gap: { xs: 5.75, sm: 10 }, p: { xs: 3, sm: 4, md: 8 }, position: 'relative', zIndex: 1 }}
              >
                <Stack sx={{ gap: 5 }}>
                  <Stack direction="column" sx={{
                    alignItems: {
                      xs: "center",      // center on small screens
                      md: "flex-start",  // left-align on medium and up
                    }, gap: 1}}>
                    <TabContext value={value}>
                      <Typography component="div" variant="h1">
                        Let's Talk
                      </Typography>
                      <Typography sx={{ color: 'text.secondary' }}>No matter how numerous and large the challenges are, at Autocycle every project, no matter how big, begins with a good conversation. </Typography>

                      <GraphicsCard sx={{ width: { xs: 1, sm: 'unset' } }}>
                        <Box sx={{ p: 0.25 }}>
                          <TabList
                            onChange={handleChange}
                            sx={{ '& .MuiTabs-indicator': { display: 'none' }, minHeight: 'unset', p: 0.25 }}
                            variant="scrollable"
                          >
                            {topics.map((item, index) => (
                              <Tab
                                label={item.title}
                                disableFocusRipple
                                icon={
                                  <SvgIcon
                                    {...(typeof item.icon === 'string' ? { name: item.icon } : { ...item.icon })}
                                    size={16}
                                    stroke={2}
                                    color="text.secondary"
                                  />
                                }
                                value={String(index + 1)}
                                key={index}
                                iconPosition="start"
                                tabIndex={0}
                                sx={{
                                  minHeight: 44,
                                  borderRadius: 10,
                                  borderWidth: 1,
                                  borderStyle: 'solid',
                                  borderColor: 'transparent',
                                  '& svg ': { mr: 1 },
                                  '&.Mui-selected': {
                                    bgcolor: 'grey.200',
                                    borderColor: 'grey.400',
                                    color: 'text.primary',
                                    '& svg': { stroke: 'text.primary' }
                                  },
                                  '&.Mui-focusVisible': { bgcolor: 'grey.300' },
                                  '&:hover': { bgcolor: 'grey.200' }
                                }}
                              />
                            ))}
                          </TabList>
                        </Box>
                      </GraphicsCard>
                            
                     
                          <TabPanel value={"2"} key={"2"} sx={{ p: 0, width: 1 }}>
                            {/* <Typeset {...{ heading: "Book Discovery Call", caption, captionProps: { sx: { maxWidth: 478 } } }} /> */}
                            <Grid container spacing={1.5}>
                          <CalendlyEmbed url="https://calendly.com/casimir-uhlig-dpschool/get-to-know" />


                            </Grid>
                          </TabPanel>

                      <TabPanel value={"1"} key={"1"} sx={{ p: 0, width: 1 }}>
                        {/* <Typeset {...{ heading: "Fill Out Contact Form", caption, captionProps: { sx: { maxWidth: 478 } } }} /> */}
                        <Grid container spacing={1.5}>
                          <Stack sx={{ gap: 1, width: { xs: '100%', sm: '100%', md: '100%' } }}>
                            <OutlinedInput
                              placeholder={input.placeholder || 'Your Name*'}
                              slotProps={{ input: { 'aria-label': 'Name' } }}
                              sx={{
                                ...theme.typography.caption2,
                                color: "#5bc80c",
                                p: 0.5,

                                whiteSpace: 'nowrap',
                                '& .MuiOutlinedInput-input': { p: '6px 20px' },
                                '& .MuiOutlinedInput-notchedOutline': { borderRadius: 25 }
                              }}
                            />
                            {input.helpertext && (
                              <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                                Help
                              </Typography>
                            )}
                            <OutlinedInput
                              placeholder={input.placeholder || 'Your Email Address*'}

                              slotProps={{ input: { 'aria-label': 'Email address' } }}
                              sx={{
                                ...theme.typography.caption2,
                                color: "#5bc80c",
                                p: 0.5,

                                whiteSpace: 'nowrap',
                                '& .MuiOutlinedInput-input': { p: '6px 20px' },
                                '& .MuiOutlinedInput-notchedOutline': { borderRadius: 25 }
                              }}
                            />
                            <OutlinedInput
                              placeholder={input.placeholder || 'Your Phone Number'}

                              slotProps={{ input: { 'aria-label': 'Phone Number' } }}
                              sx={{
                                ...theme.typography.caption2,
                                color: "#5bc80c",
                                p: 0.5,

                                whiteSpace: 'nowrap',
                                '& .MuiOutlinedInput-input': { p: '6px 20px' },
                                '& .MuiOutlinedInput-notchedOutline': { borderRadius: 25 }
                              }}
                            />
                            <OutlinedInput
                              placeholder={input.placeholder || 'Regarding'}

                              slotProps={{ input: { 'aria-label': 'Regarding' } }}
                              sx={{
                                ...theme.typography.caption2,
                                color: "#5bc80c",
                                p: 0.5,

                                whiteSpace: 'nowrap',
                                '& .MuiOutlinedInput-input': { p: '6px 20px' },
                                '& .MuiOutlinedInput-notchedOutline': { borderRadius: 25 }
                              }}
                            />
                            <OutlinedInput
                              placeholder={input.placeholder || 'Your Request*'}
                              slotProps={{ input: { 'aria-label': 'Request' } }}
                              sx={{
                                ...theme.typography.caption2,
                                color: "#5bc80c",
                                p: 0.5,

                                whiteSpace: 'nowrap',
                                '& .MuiOutlinedInput-input': { p: '6px 20px' },
                                '& .MuiOutlinedInput-notchedOutline': { borderRadius: 25 }
                              }}
                            />
                            <Button
                              color="primary"
                              variant="contained"
                              sx={{ px: 4, minWidth: { xs: 110, md: 120 } }}
                             
                  
                            >
                              Submit
                            </Button>
                          </Stack>
                        </Grid>
                      </TabPanel>
                    </TabContext>
                  </Stack>
                 
                </Stack>
               
                
                
              
              </Stack>
              <Box sx={{ position: 'absolute', right: -160, bottom: -160, display: { xs: 'none', md: 'block' }, transform: 'scaleX(-1)' }}>
                <LogoWatermark />
              </Box>
            </GraphicsCard>
          </Grid>
         
        </Grid>
      </motion.div>
    </ContainerWrapper>
  );
}

Cta5.propTypes = {
  heading: PropTypes.string,
  caption: PropTypes.string,
  label: PropTypes.string,
  input: PropTypes.oneOfType([PropTypes.any, PropTypes.bool]),
  primaryBtn: PropTypes.any,
  secondaryBtn: PropTypes.any,
  description: PropTypes.oneOfType([PropTypes.node, PropTypes.string]),
  saleData: PropTypes.any,
  profileGroups: PropTypes.object
};
