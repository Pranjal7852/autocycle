import React, { useState } from "react";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";

interface FaqItem {
  question: string;
  answer: string;
}

const FaqSection: React.FC = () => {
  const faqItems: FaqItem[] = [
    {
      question: "What is AutoCycle?",
      answer: "AutoCycle is a platform that connects brands for sustainable collaborations. We transform recycling efforts into powerful brand assets by matching companies based on material technical requirements, brand placement, and advertising value."
    },
    {
      question: "How does the matchmaking work?",
      answer: "Our matchmaking algorithm analyzes your company's materials and sustainability goals, then identifies potential collaboration partners with complementary needs and values. We consider technical requirements, brand alignment, and potential marketing value to create meaningful partnerships."
    },
    {
      question: "What is the next step after matchmaking?",
      answer: "After finding a potential match, we facilitate an introduction between both parties. Our team helps guide the initial discussions, assists with planning the collaboration project, and provides support throughout the implementation process to ensure a successful partnership."
    }
  ];

  return (
  <>
    <div className="flex flex-col w-full mt-[129px] max-md:mt-10">
      <div className="min-h-[85px] w-full font-normal">
        <h2 className="text-[41px] text-[rgba(57,48,45,1)] leading-none max-md:max-w-full">
          Frequently Asked Questions
        </h2>
      </div>

      <div className="min-h-[270px] w-full mt-[29px] pt-[15px]">
        <Accordion type="single" collapsible className="w-full">
          {faqItems.map((item, index) => (
            <AccordionItem
              key={index}
              value={`item-${index}`}
              className="bg-white border border-black mt-[19px] w-full"
            >
              <AccordionTrigger className="flex items-center w-full text-left p-[22px] text-2xl text-[#39302D] font-normal max-md:px-5">
                {item.question}
              </AccordionTrigger>
              <AccordionContent className="px-[22px] py-4 text-lg text-[#39302D]">
                {item.answer}
              </AccordionContent>
            </AccordionItem>
          ))}
        </Accordion>
      </div>
    </div>
  </>
);
}

export default FaqSection;
