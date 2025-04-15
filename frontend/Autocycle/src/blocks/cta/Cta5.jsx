'use client';
import PropTypes from 'prop-types';
import { useState, useEffect } from 'react';
import { SECTION_PATH, BUY_NOW_URL, ADMIN_PATH, DOCS_URL } from '@/path';
import { initializeApp } from 'firebase/app';
import { getFirestore, collection, addDoc } from 'firebase/firestore';
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
import Snackbar from '@mui/material/Snackbar';
import Alert from '@mui/material/Alert';
import SvgIcon from '@/components/SvgIcon';
import GraphicsImage from '@/components/GraphicsImage';
const linkProps = { target: '_blank', rel: 'noopener noreferrer' };
import { motion } from 'framer-motion';
import ButtonAnimationWrapper from '@/components/ButtonAnimationWrapper';
import ContainerWrapper from '@/components/ContainerWrapper';
import { GraphicsCard } from '@/components/cards';
import { ProfileGroup } from '@/components/cards/about-card';
import LogoWatermark from '@/components/logo/LogoWatermark';
import Typeset from '@/components/Typeset';
import { SECTION_COMMON_PY } from '@/utils/constant';
import Wave from '@/images/graphics/Wave';

// Firebase configuration
const firebaseConfig = {
  type: 'service_account',
  projectId: 'autocycle-282a6',
  private_key_id: '17caa663ccc57f40a1c3143fc63a941a298a0491',
  apiKey: '-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDhJ0Qv+8ELxo6u\nygKyUcTxQavpbgNOJ0lW7mdG9xiD9SvrxnGoF5WhzLaVENUW65H9lHOZ5QFE5Y+r\nvt9QKeURAL8PC3blmbbjxh7ZtNUWTmxqA8MqkgcJux/I9m/oKG8xWJ133k/AKBzo\nnLwQbz9W+fUIKOvgdwNoL3LecVbnCKLsFFgHoYdCLwqjQzXh9oGnHR9c611Lr1cm\nrlBBBwY21islHq+Old6YAcChY3AJ70HxdjV/9YqO9QwMcrccAaJmV6AcFpXaMVye\nIvNJO4X5B7NK8ApGJ6Jfs7M0xAplpMdhe2ywYhDT2K9NuIaIKVj4gA0zAbmum21Y\nxOBvQJ99AgMBAAECggEACN34BH/AsYsHUYDpLEamH+47K/1GKgzICaFn9daDY6cD\nLMzq6vjKzs12H1bDXZy3aiovh08KhsEXsGba+pg7yjiiTaBg9VfhaQUDcAV8It3B\nzUcKp6GKn2p8LPjvnVACWQopYXAi6elqggqyKV+IOg+sA79A0t09CBxeRL5n8r9E\nYOInbDge35SH3ZXsmyoHFYoo+0hGUTJf22yp2Eodljmw+3yMS7bALB2C6LVVfuSO\nqTlWnQ6BjmsHx9HztsTifs64THklN5ljyOZq8pM/mGWz5+hDJkxsiAfa1VDgi4eJ\nfGIABh6d13NIc99LFnXtDWPQObEBgBGXCF0oGl9BjQKBgQD/hsqSYzZPv+ik8Q9U\nNDd/ErZ5Z6Km5qtf0/7mHAXQNKb5HNG8gelKA1+6LWPldWClfQOK87+xlh6KDj18\nROuVTfxeeDg5pnXOjrRaXKOx18vCNpd/+xCR9rf55fJ1Miw8vK/xaD90qA2YNOFP\nfRcAG3dI7LEZfXX8NLn7vF/zqwKBgQDhkhFN/IqmVGkq3fb2TPoAV2CL1Af7xz2W\niXvPneq1Oxb5LlXl1O1C3UTJoU1h5DLPD8YZGe+QE9uL7Syll6WMLvMZphsXyfCU\n4BmcGU6DU/ztpYm7IvZAEtnqMJh3G3Wp5TfAs0rIzF0aKAqY9u97WVP89Y3nZn/j\nzgd5hmgRdwKBgQDbYBTAMw8ozqDkItU/PIk8vosMle3tjnIpFm9rjTlsdBe6HYTv\nazUnRthDlb6C/A/aZAbLn9K+mxxi+DDPZLhA+bAmRt42mHPhv2CVh50+DP+xIH9W\n7+xc9E0k7ccH2OhjyLbg8dgwxirNtvCM9t7tR6dUY2j0cmL+ASJ/Pk2+ewKBgCpO\nvzglWcwAoQkNQLjJj0ppGQ6g4i5zHDYT60jxkYgUYSazbiEBYs7buX8n5d+qcW0s\nxDcJCkm3r8H65hjY7I/ybl4tLX+0vI7vyV3h0TwIkLPyDHcxA4bZAk5Odwo/+D25\nZE+cUTaAPiYdxH8UMa6s/ne/hrIUI4CSsAw3DWXZAoGADDy8KQGgwZUIoaSsEV8A\nWS9W2WzqHpUX3tOmU8x+PvNgu+lq1Rt4q/AIaMmVqbU0E7pEATUYGbanCJG9kiSX\ne1nAnKDCx03/J2r/8n4b7JobI1zagcN1fIZz0UxrmtaOoorPdMdJlgp4rrguHSIl\n9oVDGHLqpMbhQ/DCw+ZvPrU=\n-----END PRIVATE KEY-----\n',
  client_email: 'firebase-adminsdk-fbsvc@autocycle-282a6.iam.gserviceaccount.com',
  client_id: '108095535176108099276',
  auth_uri: 'https://accounts.google.com/o/oauth2/auth',
  token_uri: 'https://oauth2.googleapis.com/token',
  auth_provider_x509_cert_url: 'https://www.googleapis.com/oauth2/v1/certs',
  client_x509_cert_url:'https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40autocycle-282a6.iam.gserviceaccount.com',
  universe_domain: 'googleapis.com'
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

const CalendlyEmbed = ({ url }) => {
  useEffect(() => {
    const head = document.querySelector('head');
    const script = document.createElement('script');
    script.setAttribute('src', 'https://assets.calendly.com/assets/external/widget.js');
    head.appendChild(script);
  }, []);

  return (
    <div
      className="calendly-inline-widget"
      data-url={url}
      style={{ minHeight: '750px', width: '100%', margin: '2rem auto', border: '2px solid #fff' }}
    ></div>
  );
};

export default function Cta5({ heading, caption, label, input = false, primaryBtn, secondaryBtn, description, saleData, profileGroups }) {
  const theme = useTheme();
  const [value, setValue] = useState('1');
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    regarding: '',
    request: ''
  });
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'success'
  });

  useEffect(() => {
    const script = document.createElement('script');
    script.src = 'https://assets.calendly.com/assets/external/widget.js';
    script.async = true;
    document.body.appendChild(script);
  }, []);

  const boxPadding = { xs: 3, md: 5 };
  const imagePadding = { xs: 3, sm: 4, md: 5 };

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async () => {
    try {
      await addDoc(collection(db, 'contacts'), {
        ...formData,
        timestamp: new Date()
      });
      setSnackbar({
        open: true,
        message: 'Form submitted successfully!',
        severity: 'success'
      });
      setFormData({
        name: '',
        email: '',
        phone: '',
        regarding: '',
        request: ''
      });
    } catch (error) {
      setSnackbar({
        open: true,
        message: 'Error submitting form. Please try again.',
        severity: 'error'
      });
    }
  };

  const handleSnackbarClose = () => {
    setSnackbar({ ...snackbar, open: false });
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
      }
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
    }
  ];

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
                  <Stack
                    direction="column"
                    sx={{
                      alignItems: {
                        xs: 'center',
                        md: 'flex-start'
                      },
                      gap: 1
                    }}
                  >
                    <TabContext value={value}>
                      <Typography component="div" variant="h1">
                        Let's Talk
                      </Typography>
                      <Typography sx={{ color: 'text.secondary' }}>
                        No matter how numerous and large the challenges are, at Autocycle every project, no matter how big, begins with a
                        good conversation.
                      </Typography>

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

                      <TabPanel value={'2'} key={'2'} sx={{ p: 0, width: 1 }}>
                        <Grid container spacing={1.5}>
                          <CalendlyEmbed url="https://calendly.com/casimir-uhlig-dpschool/get-to-know" />
                        </Grid>
                      </TabPanel>

                      <TabPanel value={'1'} key={'1'} sx={{ p: 0, width: 1 }}>
                        <Grid container spacing={1.5}>
                          <Stack sx={{ gap: 1, width: { xs: '100%', sm: '100%', md: '100%' } }}>
                            <OutlinedInput
                              name="name"
                              value={formData.name}
                              onChange={handleInputChange}
                              placeholder={input.placeholder || 'Your Name*'}
                              slotProps={{ input: { 'aria-label': 'Name' } }}
                              sx={{
                                ...theme.typography.caption2,
                                color: '#5bc80c',
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
                              name="email"
                              value={formData.email}
                              onChange={handleInputChange}
                              placeholder={input.placeholder || 'Your Email Address*'}
                              slotProps={{ input: { 'aria-label': 'Email address' } }}
                              sx={{
                                ...theme.typography.caption2,
                                color: '#5bc80c',
                                p: 0.5,
                                whiteSpace: 'nowrap',
                                '& .MuiOutlinedInput-input': { p: '6px 20px' },
                                '& .MuiOutlinedInput-notchedOutline': { borderRadius: 25 }
                              }}
                            />
                            <OutlinedInput
                              name="phone"
                              value={formData.phone}
                              onChange={handleInputChange}
                              placeholder={input.placeholder || 'Your Phone Number'}
                              slotProps={{ input: { 'aria-label': 'Phone Number' } }}
                              sx={{
                                ...theme.typography.caption2,
                                color: '#5bc80c',
                                p: 0.5,
                                whiteSpace: 'nowrap',
                                '& .MuiOutlinedInput-input': { p: '6px 20px' },
                                '& .MuiOutlinedInput-notchedOutline': { borderRadius: 25 }
                              }}
                            />
                            <OutlinedInput
                              name="regarding"
                              value={formData.regarding}
                              onChange={handleInputChange}
                              placeholder={input.placeholder || 'Regarding'}
                              slotProps={{ input: { 'aria-label': 'Regarding' } }}
                              sx={{
                                ...theme.typography.caption2,
                                color: '#5bc80c',
                                p: 0.5,
                                whiteSpace: 'nowrap',
                                '& .MuiOutlinedInput-input': { p: '6px 20px' },
                                '& .MuiOutlinedInput-notchedOutline': { borderRadius: 25 }
                              }}
                            />
                            <OutlinedInput
                              name="request"
                              value={formData.request}
                              onChange={handleInputChange}
                              placeholder={input.placeholder || 'Your Request*'}
                              slotProps={{ input: { 'aria-label': 'Request' } }}
                              sx={{
                                ...theme.typography.caption2,
                                color: '#5bc80c',
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
                              onClick={handleSubmit}
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
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={handleSnackbarClose}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={handleSnackbarClose} severity={snackbar.severity} sx={{ width: '100%' }}>
          {snackbar.message}
        </Alert>
      </Snackbar>
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
