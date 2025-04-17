// @project
import branding from '@/branding.json';
import { IconType } from '@/enum';
import { SECTION_PATH, BUY_NOW_URL, ADMIN_PATH, DOCS_URL } from '@/path';

const linkProps = { target: '_blank', rel: 'noopener noreferrer' };

export const feature2 = {
  heading: 'Culture of Innovation',
  caption:
    'Join a team that embraces forward-thinking ideas, fosters innovation, and cultivates an environment where your creativity can flourish.',
  features: [
    {
      icon: { name: 'tabler-users', type: IconType.STROKE, color: 'grey.900', stroke: 1 },
      title: 'Teamwork',
      content: 'We embrace varied perspectives and backgrounds, creating an inclusive environment.'
    },
    {
      icon: { name: 'tabler-star', type: IconType.STROKE, color: 'grey.900', stroke: 1 },
      title: 'Inclusivity',
      content: 'We embrace varied perspectives and backgrounds, creating an inclusive environment.'
    },
    {
      icon: { name: 'tabler-chart-histogram', type: IconType.STROKE, color: 'grey.900', stroke: 1 },
      title: 'Growth',
      content: 'Our culture prioritizes continuous learning, encouraging personal and professional development. '
    }
  ]
};

export const feature5 = {
  heading: 'Beyond the 9-to-5',
  caption: 'Our benefits go beyond the standard, ensuring your life outside of work is just as fulfilling.',
  image1: '/assets/images/graphics/ai/graphics3-light.svg',
  image2: '/assets/images/graphics/ai/graphics2-light.svg',
  features: [
    {
      icon: 'tabler-coin',
      title: 'Compensation',
      content: 'Enjoy a competitive salary that recognizes your skills and contributions.'
    },
    {
      icon: 'tabler-health-recognition',
      title: 'Healthcare',
      content: "Access to a comprehensive healthcare plan, ensuring you and your family's well-being."
    }
  ],
  features2: [
    {
      icon: 'tabler-briefcase',
      title: 'Automated Scaling',
      content: 'Embrace a flexible work environment, allowing you to balance work.'
    },
    {
      icon: 'tabler-users',
      title: 'Real-Time',
      content: 'Support your family commitments with family-friendly policies and benefits.'
    }
  ],
  profileGroups: {
    avatarGroups: [
      { avatar: '/assets/images/user/avatar1.png' },
      { avatar: '/assets/images/user/avatar2.png' },
      { avatar: '/assets/images/user/avatar3.png' },
      { avatar: '/assets/images/user/avatar4.png' },
      { avatar: '/assets/images/user/avatar5.png' }
    ],
    review: '10k+ Reviews (4.5 out of 5)'
  },
  content: 'Explore diverse career paths within the company through our internal mobility programs.',
  actionBtn: { children: 'Explore all Features', href: '#' }
};

export const feature20 = {
  heading: 'Service Tailored to your Needs',
  caption: 'Interested how we can fix your future sourcing?',
  actionBtn: { children: "Let's Talk", href: "/#contact" },
  secondaryBtn: { children: 'Our Solutions', href: "/#solution" },
  features: [
    {
      icon: 'tabler-accessible',
      title: 'Reliable Pricing',
      content: "We offer consistent, transparent pricing so you can plan with confidence — no hidden costs, no surprises."},
    {
      icon: 'tabler-icons',
      title: 'Planning Made Easy',
      content: "Structured timelines and clear milestones make your sourcing process predictable and easy to manage — from first contact to delivery." },
    {
      icon: 'tabler-stack-2',
      title: 'Quality You Can Count On',
      content: "Every material we match comes with verified origin and consistent properties — ensuring it meets your standards in both performance and volume."  },
    {
      icon: 'tabler-rocket',
      title: 'Flexible Timing',
      content: "We adapt to your schedule. Whether you’re ready now or planning ahead, our team is here when you need us" },
    {
      icon: 'tabler-help',
      title: 'Full Traceability',
      content: "Track every step of your project. From sourcing to shipment, we ensure transparent documentation and a clear chain of custody."  },
    {
      icon: 'tabler-refresh',
      title: 'Added Brand Value',
      content: "Show your commitment to circularity with traceable sourcing. It’s more than compliance — it’s a story your brand can proudly tell." }
  ]
};

export const feature21 = {
  heading: `Design Faster, Smarter with ${branding.brandName} Figma`,
  caption: 'Unlock Figma’s advanced tools for streamlined, scalable, and responsive SaaS UI design.',
  image: '/assets/images/graphics/ai/desktop1-light.svg',
  primaryBtn: { children: 'Free Figma', href: 'https://www.figma.com/community/file/1425095061180549847', ...linkProps },
  secondaryBtn: {
    children: 'Preview Pro Figma',
    href: 'https://www.figma.com/design/mlkXfeqxUKqIo0GQhPBqPb/SaasAble---UI-Kit---Preview-only?node-id=11-1833&t=JBHOIIEuYZpmN6v8-1',
    ...linkProps
  },
  features: [
    {
      animationDelay: 0.1,
      icon: 'tabler-components',
      title: 'Component Architecture'
    },
    {
      animationDelay: 0.2,
      icon: 'tabler-moon',
      title: 'Dark Mode'
    },
    {
      animationDelay: 0.3,
      icon: 'tabler-brightness-auto',
      title: 'Auto Layout'
    },
    {
      animationDelay: 0.4,
      icon: 'tabler-accessible',
      title: 'WCAG Compliant'
    },
    {
      animationDelay: 0.1,
      icon: 'tabler-icons',
      title: 'Custom Icons'
    },
    {
      animationDelay: 0.2,
      icon: 'tabler-file-stack',
      title: 'Page Demos'
    },
    {
      animationDelay: 0.3,
      icon: 'tabler-brand-matrix',
      title: 'Material 3 Guideline'
    },
    {
      animationDelay: 0.4,
      icon: 'tabler-click',
      title: 'Quick Customization'
    }
  ]
};

export const feature = {
  heading: `What’s Inside of ${branding.brandName} Plus Version`,
  features: [
    {
      image: '/assets/images/shared/react.svg',
      title: 'CRA JavaScript',
      content: 'Ensure accessibility with WCAG compliant design for browsing.'
    },
    {
      image: '/assets/images/shared/next-js.svg',
      title: 'Next.js JavaScript',
      content: 'Tailor typography for optimal readability across all screen sizes.'
    },
    {
      image: '/assets/images/shared/react.svg',
      title: 'CRA TypeScript',
      content: 'Customize Material 3 design MUI components for enhanced aesthetics.'
    },
    {
      image: '/assets/images/shared/next-js.svg',
      title: 'Next.js TypeScript',
      content: 'Adjust content layout for visual coherence on various screen sizes.'
    },
    {
      image: '/assets/images/shared/figma.svg',
      title: 'Figma ',
      content: 'Boost visibility with SEO-friendly features for better search rankings.'
    },
    {
      title: 'Check Out Our Pricing Plan',
      content: 'Choose the plan that aligns with your SaaS product requirements.',
      actionBtn: { children: 'Pricing Plan', href: BUY_NOW_URL, ...linkProps }
    }
  ]
};

export const feature7 = {
  heading: 'Real-Time Performance Insights',
  caption: 'Gain a competitive edge with real-time performance monitoring.',
  testimonials: [
    {
      image: '/assets/images/graphics/ai/graphics6-light.svg',
      features: [
        {
          icon: 'tabler-star',
          title: 'Core Value',
          content: 'Unlock growth potential through continuous monitoring, enabling proactive strategies in a competitive landscape.'
        }
      ]
    },
    {
      image: '/assets/images/graphics/ai/graphics8-light.svg',
      features: [
        {
          icon: 'tabler-route',
          title: 'Multi-Cloud Orchestration',
          content: 'Enhances flexibility and resilience in a multi-cloud environment.'
        }
      ]
    },
    {
      image: '/assets/images/graphics/ai/graphics3-light.svg',
      features: [
        {
          icon: 'tabler-history',
          title: 'Story',
          content: 'Real-time performance insights empower teams to respond swiftly, optimizing operations and driving growth.'
        }
      ]
    }
  ],
  breadcrumbs: [{ title: 'Core Value' }, { title: 'Culture' }, { title: 'Story' }]
};

export const feature23 = {
  heading: 'Culture of Innovation',
  caption:
    'Join a team that embraces forward-thinking ideas, fosters innovation, and cultivates an environment where your creativity can flourish.',
  heading2: 'Growth',
  caption2: 'Our culture prioritizes continuous learning, encouraging personal and professional development. ',
  image: '/assets/images/graphics/default/feature23-light.png',
  primaryBtn: { children: 'Join  Our Team', href: '#' },

  features: [
    {
      icon: 'tabler-users',
      title: 'Teamwork',
      content: 'We embrace varied perspectives and backgrounds, creating an inclusive environment.'
    },
    {
      icon: 'tabler-star',
      title: 'Inclusivity',
      content: 'We embrace varied perspectives and backgrounds, creating an inclusive environment.'
    }
  ]
};

export const feature18 = {
  heading: ' From Waste to Value – How It Works',
  caption: 'Our process ensures quality, compliance, and eco-friendly solutions for a cleaner tomorrow.',
  topics: [
    {
      icon: 'tabler-balloon',
      title: 'Initial Consultation',
      title2: 'Let’s Understand Your Needs',
      description: "We begin by understanding your project's needs in our first call, where we refine your material requirements. During this conversation, we’ll ask questions to ensure we fully understand your application, volume, and delivery timelines.",
      image: {
        light: '/assets/images/graphics/default/admin-dashboard.png',
        dark: '/assets/images/graphics/default/admin-dashboard-dark.png'
      },
      list: [
        { primary: 'Discuss your material requirements and application context' },
        { primary: 'Clarify technical and performance expectations' },
        { primary: 'Define volume, location, and timing needs' },
        { primary: 'Address early-stage questions or uncertainties' }
      ],
    },
    {
      icon: 'tabler-ballpen',
      title: 'List Your Requirements',
      title2: 'Tell Us What You Need',
      description: 'Once we’ve established the foundation, you’ll submit a detailed list of material specifications. This includes properties like strength, flexibility, color, and environmental concerns, which will help us pinpoint the best materials for your project.',
      image: '/assets/images/graphics/default/admin-dashboard-3.png',
      list: [
        {
          primary: 'Submit material requirements with detailed specifications' },
        { primary: 'Specify strength, flexibility, and color preferences' },
        { primary: 'Identify environmental and sustainability concerns' },
        { primary: 'Highlight any industry-specific regulations or standards' }
      ],
    },
    {
      icon: 'tabler-wand',
      title: 'Material Matching',
      title2: 'Finding the Perfect Match',
      description: 'Our platform evaluates available plastic materials that match your specifications. We identify the best-fit options based on performance, pricing, and sustainability to ensure the right material is sourced for your needs.',
      image: '/assets/images/graphics/default/admin-dashboard-2.png',
      list: [
        { primary: 'Match specifications with available plastic materials' },
        { primary: 'Compare performance, pricing, and environmental impact' },
        { primary: 'Prioritize sustainability and compliance' },
        { primary: 'Recommend the most suitable options based on your project’s requirements' }
      ],
      
    },
    {
      icon: 'tabler-tax-euro',
      title: 'Connect & Close the Deal',
      title2: 'Seal the Deal & Move Forward',
      description: 'Once a suitable material match is found, we facilitate direct negotiation with the seller. After finalizing the terms and contract, the order is confirmed, ensuring timely and efficient delivery.',
      image: '/assets/images/graphics/default/admin-dashboard.png',
      list: [
        { primary: 'Negotiate terms and pricing with the seller' },
        { primary: 'Finalize the material order and delivery details' },
        { primary: 'Sign the contract to secure the agreement' },
        { primary: 'Ensure smooth and timely order fulfillment' }
      ]
    }
  ]
};
