import React from "react";

const LegalNotice: React.FC = () => {
  return (
    <div className="bg-white min-h-screen py-16 px-4 sm:px-8 lg:px-56 text-[#222] font-mulish">
      <h1 className="text-3xl font-bold mb-10 uppercase">Legal Notice</h1>

      <section className="mb-8">
        <p>
          <span className="font-bold">UnternehmerTUM GmbH</span><br />
          Lichtenbergstr. 6<br />
          85748 Garching b. München
        </p>
      </section>

      <section className="mb-8">
        <p className="font-bold mb-1">Represented by</p>
        <ul className="ml-5 list-disc">
          <li>Prof. Dr. Helmut Schönenberger (CEO)</li>
          <li>Stefan Drüssler</li>
          <li>Claudia Frey</li>
          <li>Christian Mohr</li>
          <li>Thomas Zeller</li>
        </ul>
      </section>

      <section className="mb-8">
        <p className="font-bold mb-1">Contact</p>
        <ul className="ml-5 list-none">
          <li>Phone: +49 89-541 986 9800</li>
          <li>Fax: +49 89-541 987 0060</li>
          <li>Email: <a href="mailto:info@unternehmertum.de" className="underline text-blue-600">info@unternehmertum.de</a></li>
        </ul>
      </section>

      <section className="mb-8">
        <p className="font-bold mb-1">VAT Number</p>
        <p>
          VAT identification number in accordance with Section 27 a of the German VAT act:<br />
          <span className="font-semibold">DE 252 789 694</span>
        </p>
      </section>

      <section className="mb-8">
        <p className="font-bold mb-1">Responsible in Accordance with Section 18 Paragraph 2 MStV</p>
        <ul className="ml-5 list-disc">
          <li>Prof. Dr. Helmut Schönenberger (CEO)</li>
          <li>Stefan Drüssler</li>
          <li>Claudia Frey</li>
          <li>Christian Mohr</li>
          <li>Thomas Zeller</li>
        </ul>
      </section>

      <section className="mb-8">
        <h2 className="font-bold mb-1">Accountability for Content</h2>
        <p>
          The contents of our pages have been created with the utmost care. However, we cannot guarantee the contents' accuracy, completeness or topicality. According to statutory provisions, we are furthermore responsible for our own content on these web pages. In this matter, please note that we are not obliged to monitor the transmitted or saved information of third parties, or investigate circumstances pointing to illegal activity. Our obligations to remove or block the use of information under generally applicable laws remain unaffected by this as per §§ 8 to 10 of the Telemedia Act (TMG).
        </p>
      </section>

      <section className="mb-8">
        <h2 className="font-bold mb-1">Accountability for Links</h2>
        <p>
          Responsibility for the content of external links (to web pages of third parties) lies solely with the operators of the linked pages. No violations were evident to us at the time of linking. Should any legal infringement become known to us, we will remove the respective link immediately.
        </p>
    </section>
     <section className="mb-9">
      <h2 className="font-bold mb-1">Copyright</h2>
      <p>
        Our web pages and their contents are subject to German copyright law. Unless expressly permitted by law, every form of utilizing, reproducing or processing works subject to copyright protection on our web pages requires the prior consent of the respective owner of the rights. Individual reproductions of a work are only allowed for private use. The materials from these pages are copyrighted and any unauthorized use may violate copyright laws.
      </p>
     </section>
</div>
);
};

export default LegalNotice;