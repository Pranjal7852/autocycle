
import React from "react";

const HowItWorks: React.FC = () => {
  return (
    <div className="container mx-auto px-4 py-16">
      <h2 className="text-[64px] font-bold text-center uppercase mb-16 max-md:text-4xl">
        how it works?
      </h2>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="text-center">
          <div className="font-black text-2xl mb-6">
            Step 1:
          </div>
          <h3 className="text-[#39302D] font-extrabold text-2xl mb-4">
            Enter Company & Material Info
          </h3>
          <p className="text-lg">
            Just type in your company name and the materials you work with
          </p>
        </div>
        
        <div className="text-center">
          <div className="font-black text-2xl mb-6">
            Step 2:
          </div>
          <h3 className="text-[#39302D] font-extrabold text-2xl mb-4">
            Get unique product Ideas
          </h3>
          <p className="text-lg">
            Get tailored and innovative product ideas instantly.
          </p>
        </div>
        
        <div className="text-center">
          <div className="font-black text-2xl mb-6">
            Step 3:
          </div>
          <h3 className="text-[#39302D] font-extrabold text-2xl mb-4">
            Connect with collaborators
          </h3>
          <p className="text-lg">
            Connect with potential collaborators who share your vision
          </p>
        </div>
      </div>
    </div>
  );
};

export default HowItWorks;
