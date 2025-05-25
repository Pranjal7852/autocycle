import React from "react";
import { Link } from "react-router-dom";

const HeroSection: React.FC = () => {
  return (
    <div className="w-full bg-white flex py-4 border-2 border-red-200 justify-center">
      <div className="flex flex-col md:flex-row w-full justify-center">
        {/* LEFT COLUMN */}
        <div className="flex flex-col w-[65%] z-10 border-2 border-red-200">
          <h1 className="font-plex text-black text-[104px] leading-none uppercase font-bold relative">
            UPYLCE<br />YOUR BRAND
          </h1>
          <div className="relative w-[100%] flex-shrink-0 h-[800px]">
          {/* Light blue square background */}
          <div className="absolute top-[200px] left-0 w-[600px] bg-[#E7F1F6] aspect-square -z-10 ml-[40px] xl:h-[600px]">
          {/* Text in top-left of grey square */}
          <div className="absolute bottom-2 left-1 z-10 text-left">
            <span className="font-bold text-l text-black leading-tight text-[clamp(1rem,2vw,2rem)]">
              BMW<br />x<br />DECATHLON
            </span>
          </div>
          </div>
          {/* Frisbee image overlapping the square */}
          <img
            src="/images/bmwxdecathlon.png"
            alt="BMW x Decathlon Frisbee"
            className="absolute -left-7 top-7 w-[525px] h-auto z-20 max-w-[700px]"
            style={{ pointerEvents: 'none' }}
            draggable={false}
          />
          {/* Heading */}
          <div className="absolute bottom-[8.7rem] -right-[5.7rem]">
                <h2 className=" font-plex text-black text-[104px] leading-none uppercase font-bold w-fit ml-auto text-right">
                  <span className="block">WITH</span>
                  <span className="block">RECYCLED</span>
                  <span className="block">MATERIALS</span>
                </h2>
          </div>

        </div>
          
        <div className="mt-6 mulish text-[28px] text-gray-800 z-10 space-y-4">
            <p>
              Our tool technically matches material waste between companies, then adds value through creative brand collaborations —
              turning waste into profit, and products into stories.
            </p>
            <p>
              This way, brands not only reduce waste and gain material efficiency — they also boost market value through meaningful,
              co-branded products. It's where sustainability meets strategy.
            </p>
          </div>
      </div>

        {/* RIGHT COLUMN */}
        <div className="flex flex-col w-[35%] items-center mt-[100px]  border-2 border-red-200">
        {/* Samsonite x Bosch */} 
          <div className="w-full flex justify-end items-center z-10">
            {/* Grey square background */}
            <div className="relative w-[100%] aspect-square bg-[#D2D4D6] z-10 max-w-[400px]">
              {/* Text in top-right of grey square */}
              <div className="relative top-0 right-2 z-10 text-right">
                <span className="font-bold text-black leading-tight text-[clamp(1rem,2vw,2rem)]">
                  BOSCH<br />x<br />SAMSONITE
                </span>
              </div>
              {/* Suitcase image overlapping the square */}
              <img
                src="/images/boschxsamsonite.png"
                alt="BMW x Samsonite Luggage"
                className="absolute -bottom-[3rem] -left-[3rem] h-[95%] z-20 max-w-[240]"
                style={{ pointerEvents: 'none' }}
                draggable={false}
              />
            </div>
          </div>

        {/*BUTTON*/}
        <div className="flex w-full h-[453px] place-items-center relative z-10">
          <Link to="/collaborations" className="justify-center absolute right-0 max-w-[400px]">
            <button className="w-full bg-black text-white px-5 py-4 text-[32px] font-extralight font-Poppins hover:bg-gray-900 flex items-center gap-x-5">
              <span>Get Started</span>
              <img src="/icons/arrow_outward.svg" alt="Arrow icon" className="w-18 h-18" />
            </button>
          </Link>
        </div>


        <div className="flex w-full justify-end items-center">
            {/* Amber square background */}
            <div className="relative right-0 w-[100%] aspect-square bg-[#F1E7D7] max-w-[400px] z-0">
            {/* Chair image overlapping the square */}
              <img
                src="images/bmxikeachair.png"
                alt="BMW x IKEA Chair"
                className="absolute left-[1rem] -bottom-10 w-[95%] h-auto z-30"
                style={{ pointerEvents: 'none' }}
                draggable={false}
              />

              {/* Text in top-left of square */}
              <div className="absolute top-2 left-2 z-20 text-left">
                <span className="font-bold text-black leading-tight text-[clamp(1rem,2vw,2rem)]">
                  BMW<br />x<br />IKEA
                </span>
            </div>
      
          </div>
        </div>
      </div>
      </div>
    </div>
  );
};

export default HeroSection;
