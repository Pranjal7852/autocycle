import React from "react";
import { Link } from "react-router-dom";

const Footer = () => {
  return (
    <footer className="w-full bg-white py-10">
      <div className="mx-auto flex flex-col md:flex-row justify-between items-start">
        {/* LEFT: Logo/Brand + Info */}
        <div className="flex flex-col gap-3 md:w-1/2">
          <div className="text-3xl font-extrabold uppercase mb-2">AUTOCYCLE</div>
          <div className="text-base">Based in Munich, operating across Europe</div>
          <div className="text-base">
            <a href="mailto:info@autocycle.dps" className="decoration-blue-500 underline-offset-2">
              info@autocycle.dps
            </a>
          </div>
          <div className="text-base">Lichtenbergstraße 6, 85748 Garching bei München</div>
          <div className="text-base mt-4">&copy; 2025 AutoCycle</div>
        </div>

        {/* RIGHT: Links, stacked */}
        <div className="flex flex-col gap-6 justify-end">
          <Link to="/privacy-policy" className="text-lg font-medium hover:underline text-right md:text-left">
            Privacy Policy
          </Link>
          <Link to="/legal-notice" className="text-lg font-medium hover:underline text-right md:text-left">
            Legal Notice
          </Link>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
