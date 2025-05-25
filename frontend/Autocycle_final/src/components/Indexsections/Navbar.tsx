import React from "react";
import { Link } from "react-router-dom";

const Navbar: React.FC = () => {
  return (
    <div className="w-full pt-[35px]">
      <div className="relative w-full mx-auto h-[60px] border-2 border-red-200">
        {/* Logo - fixed to the left */}
        <div className="absolute left-0 top-1/2 -translate-y-1/2">
          <Link to="/" className="no-underline text-black">
            <div className="text-2xl font-bold uppercase leading-[36px]">
              AutoCycle
            </div>
          </Link>
        </div>

        {/* Navigation links - centered */}
        <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 flex items-center gap-16 text-lg font-medium whitespace-nowrap border-2 border-red-200">
          <Link to="/" className="no-underline text-black font-bold uppercase">HOME</Link>
          <a href="#how-it-works" className="no-underline text-black uppercase">Solution</a>
          <a href="#faq" className="no-underline text-black uppercase">FAQ</a>
        </div>
      </div>
    </div>
  );
};

export default Navbar;
