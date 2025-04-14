// @project
import { landingMegamenu, pagesMegamenu } from '../../common-data';
import SvgIcon from '@/components/SvgIcon';
import { SECTION_PATH, ADMIN_PATH, BUY_NOW_URL, DOCS_URL, FREEBIES_URL } from '@/path';

/***************************  DEFAULT - NAVBAR  ***************************/

const linkProps = { target: '_blank', rel: 'noopener noreferrer' };
export const navbar = {
  customization: true,
  secondaryBtn: {
    children: <SvgIcon name="tabler-brand-linkedin" color="primary.main" size={18} />,
    href: "https://www.linkedin.com/company/autocycle1/posts/?feedView=all",
    ...linkProps,
    sx: { minWidth: 40, width: 40, height: 40, p: 0 }
  },
  primaryBtn: { children: "Let's talk", href: "/#contact", },
  navItems: [
    { id: 'home', title: 'Home', link: '/' },
    { id: 'solution', title: 'Solution', link: "/#solution" },
    { id: 'faq', title: 'FAQ', link: "/#faq" },
    { id: 'about', title: 'About us', link: "/about" },
  ]
};
