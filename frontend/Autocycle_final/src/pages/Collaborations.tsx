import React from "react";
import { Link } from "react-router-dom";
import FlowNavigator from "@/components/FlowNavigator";

const Collaborations: React.FC = () => {
  return (
    <div className="bg-background min-h-screen flex px-4 justify-center">
      <div className="max-w-[1200px] w-full flex flex-col">
        <div className="flex">
        {/* Navigation */}
        <FlowNavigator currentStep="form" />
        </div>

        {/* Header */}
        <div className="w-full mb-14">
          <h2 className="font-mulish text-2xl font-extrabold leading-snug text-primary uppercase text-left">
            START BY TELLING US WHETHER YOU&apos;RE CONTRIBUTING OR LOOKING FOR MATERIALS.
          </h2>
        </div>

        {/* Boxes Container */}
        <div className="flex justify-center">
        <div className="w-[80%] flex justify-between gap-4">
        
          {/* Box 1 – I HAVE MATERIAL (left-aligned) */}
          <Link
            to="/have-material"
            className="w-[350px] h-[350px] cursor-pointer flex flex-col group relative"
          >
            <div className="w-full h-full flex flex-col items-center justify-between py-8 px-4 bg-[#E7F1F6]">
              <div className="flex flex-col items-center">
                <span className="font-mulish text-lg font-bold text-primary text-center mb-2 tracking-wide">
                  FOR BRAND <br /> COLLABRATION
                </span>
                <span className="font-mulish text-2xl font-extrabold text-primary text-center uppercase">
                  I HAVE MATERIAL
                </span>
              </div>
            </div>
            <img
              src="images/Material Pile.png"
              alt="Material pile"
              className="absolute -bottom-[90px] -left-[51px] max-w-[156%] h-auto"
            />
          </Link>

          {/* Box 2 – I NEED MATERIAL (right-aligned) */}
          <Link
            to="/need-material"
            className="w-[350px] h-[350px] cursor-pointer flex flex-col group relative"
          >
            <div className="w-full h-full flex flex-col items-center justify-between py-8 px-4 bg-[#ECF5DC]">
              <div className="flex flex-col items-center">
                <span className="font-mulish text-lg font-bold text-primary text-center mb-2 tracking-wide">
                  FOR BRAND <br /> COLLABRATION
                </span>
                <span className="font-mulish text-2xl font-extrabold text-primary text-center uppercase">
                  I NEED MATERIAL
                </span>
              </div>
            </div>
            <img
              src="images/Material Sample.png"
              alt="Material sample"
              className="absolute -bottom-[60px] -left-[90px] max-w-[156%] h-auto"
            />
          </Link>
        </div>
      </div>
    </div>
    </div>
  );
};

export default Collaborations;
