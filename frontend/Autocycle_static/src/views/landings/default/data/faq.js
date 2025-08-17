// @project
import branding from '@/branding.json';

export const faq = {
  heading: 'Frequently Asked Questions',
  caption: `Answers to common queries about ${branding.brandName}.`,
  defaultExpanded: 'Fees & Charges',
  faqList: [
    {
      question: ` What is ${branding.brandName}?`,
      answer: `Autocycle is a sourcing consultancy service connecting OEMs, required to comply with stringent EPR regulations for managing end-of-life vehicles, with plastic parts manufacturers. We facilitate strategic partnerships that ensure the quality, quantity, and timing of sourced materials meet your long-term needs.`,
      category: 'General'
    },
    {
      question: `Who Is Behind ${branding.brandName}?`,
      answer: `Our focus is on plastic materials derived from end-of-life products. By building strategic partnerships and leveraging our deep industry knowledge, we mitigate waste creation and offer you a reliable stream of high-quality, recyclable plastics.`,
      category: 'General'
    },
    {
      question: `What Kind of Materials Can Be Traded?`,
      answer: {
        content: `Yes, ${branding.brandName} is built for both, with a Figma UI kit for designers and React code for developers.`,
        type: 'list',
        data: [
          { primary: 'Figma UI Kit for Designers.' },
          { primary: 'React Material UI Code for Developers.' },
          { primary: 'Seamless Collaboration.' }
        ]
      },
      category: 'General'
    },
    {
      question: `How do you ensure Quality and Quantity over the supply chain?`,
      answer: `We work closely with industry partners that specialize in connecting all players over the supply chain to ensure that the right quantity and quality material is ready for production at the time you need it.`,
      category: 'General'
    },
    {
      question: 'How do you support clients after project implementation?',
      answer: 'After we implement the project we follow up with Quality Control and support you if any issues arise.',
      category: 'General'
    },
  ],
  getInTouch: {
    link: { children: 'Get in Touch', href: "#contact", rel: 'noopener noreferrer' }
  },
  categories: ['General', 'Pricing & Licenses', 'Support & Updates'],
  activeCategory: 'General'
};
