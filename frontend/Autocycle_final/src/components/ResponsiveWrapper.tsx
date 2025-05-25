import React, { useState, useEffect, ReactNode } from 'react';

interface ResponsiveWrapperProps {
  children: ReactNode;
}

const ResponsiveWrapper: React.FC<ResponsiveWrapperProps> = ({ children }) => {
  const [isSmallScreen, setIsSmallScreen] = useState(false);

  useEffect(() => {
    const checkScreenSize = () => {
      setIsSmallScreen(window.innerWidth < 1200);
    };

    checkScreenSize(); // Initial check

    window.addEventListener('resize', checkScreenSize);
    return () => window.removeEventListener('resize', checkScreenSize);
  }, []);

  if (isSmallScreen) {
    return (
      <div className="flex items-center justify-center min-h-screen text-center px-4 bg-white">
        <p className="text-xl poppins font-semibold text-black">
          This website is not optimized for small screens. Please use a larger device.
        </p>
      </div>
    );
  }

  return <>{children}</>;
};

export default ResponsiveWrapper;
