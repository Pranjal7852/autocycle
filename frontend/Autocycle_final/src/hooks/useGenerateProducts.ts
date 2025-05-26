import { useState } from "react";

interface GenerateProductsData {
    source_brand: string;
    plastic_type: string;
    location: string;
    target_brand: string;
}

interface GenerateProductsResponse {
    status: "success" | "error";
    result?: {
        status: string;
        results: any[]; // Can be further typed if needed
    };
    message?: string;
}

interface GenerateProductsHookResponse {
    isLoading: boolean;
    error: string | null;
    submit: (data: GenerateProductsData) => Promise<GenerateProductsResponse>;
}

const dummyResponse: GenerateProductsResponse = {
    status: "success",
    result: {
        status: "product_development_complete",
        results: [
            {
                product_name: "BMW x Adidas Eco Performance Sneakers",
                status: "success",
                result: {
                    brand: "BMW",
                    target_brand: "Adidas",
                    product_type: "sneaker",
                    product_name: "BMW x Adidas Eco Performance Sneakers",
                    product_description:
                        "An innovative sneaker design merging BMW's luxury aesthetic with Adidas' eco-friendly technology, constructed from recycled plastics. Features BMW’s signature metallic accents, a sleek silhouette, and a color palette of deep blue and vibrant green.",
                    pitch:
                        "**Concept:**  \nIntroducing the BMW x Adidas Eco Performance Sneakers, a cutting-edge fusion of luxury and sustainability, crafted from recycled plastics to deliver style, performance, and conscious living.\n\n**Leveraging Brand Identity:**  \nBMW, renowned for its commitment to luxury and innovation, brings an elevated aesthetic and precision engineering to the sneaker design, showcasing metallic accents and a sleek silhouette that resonates with its automotive heritage. Adidas, a pioneer in sustainability and sportswear, infuses eco-friendly technology and a focus on performance, enhancing the sneakers' appeal to environmentally-conscious athletes and style enthusiasts.\n\n**Market Positioning and Intended Audience:**  \nPositioned at the intersection of luxury lifestyle and eco-consciousness, the BMW x Adidas Eco Performance Sneakers target environmentally-aware millennials and Gen Z consumers who value brands that align with their sustainable values. This collaboration appeals to both automotive aficionados and fashion-forward individuals seeking high-quality, stylish footwear that reflects a commitment to the planet.\n\n**Sustainability Innovation:**  \nThese sneakers are not only striking in design but are also a testament to sustainability; constructed entirely from recycled plastics, they illustrate how premium products can lead in environmental responsibility. With a low carbon footprint and eco-friendly manufacturing processes, the shoes exemplify how luxury can embrace sustainability without compromising performance.\n\n**Co-Branding and Storytelling Potential:**  \nThe story behind the BMW x Adidas Eco Performance Sneakers will resonate deeply with consumers: two brands—each leaders in their fields—coming together to redefine luxury and sustainability. Marketing campaigns can feature narratives around the journey of transforming waste into a fashionable product, echoing both brands' push towards a greener future. Collaborations with influencers and sustainability advocates will enhance visibility, while events that showcase innovative approaches to eco-friendly design will further cement the narrative, inviting customers to be part of a movement that champions luxury and sustainability.\n\nThis collaboration not only redefines sneaker culture but encourages a paradigm shift towards sustainable consumption, anchoring both BMW and Adidas in an eco-forward narrative that inspires future innovation.",
                    image_url:
                        "https://res.cloudinary.com/dkcvg4eui/image/upload/v1748216717/product_images/BMW%20x%20Adidas%20Eco%20Performance%20Sneakers.png"
                }
            },
            {
                product_name: "Adidas x BMW Sustainable Car Mats",
                status: "success",
                result: {
                    brand: "BMW",
                    target_brand: "Adidas",
                    product_type: "automotive accessory",
                    product_name: "Adidas x BMW Sustainable Car Mats",
                    product_description:
                        "Premium car mats infused with Adidas' signature recycled ocean plastic, featuring the iconic three stripes. Designed with BMW’s luxury vehicle contours, they combine sustainability with style, available in black with touches of white and green.",
                    pitch:
                        "**Concept:** Discover the Adidas x BMW Sustainable Car Mats—premium car mats crafted from Adidas' recycled ocean plastic, designed to fit BMW's luxury contours while embodying sustainable style with iconic three stripes.  \n\n**Brand Identity Leveraging:** The collaboration harnesses Adidas's commitment to sustainability and innovation through the use of recycled materials, while BMW emphasizes luxury and craftsmanship. Together, they create a product that not only enhances the driving experience but also aligns with conscientious consumer demands.  \n\n**Market Positioning and Intended Audience:** Positioned for eco-conscious luxury vehicle owners, this product targets progressive consumers who value both style and sustainability. This demographic is typically affluent, environmentally aware, and looking for ways to integrate eco-friendly choices into their high-end lifestyle.  \n\n**Sustainability Innovation:** By utilizing recycled ocean plastics, this collaboration draws attention to the global plastic waste crisis while promoting actionable solutions. The upcycled nature of the car mats reduces landfill waste and minimizes new material usage, making luxury sustainable.  \n\n**Co-branding and Storytelling Potential:** The story of the Adidas x BMW Sustainable Car Mats highlights a shared vision for a sustainable future, where luxury does not compromise ethical responsibility. Through storytelling on social media and marketing campaigns, the brands can engage consumers in a narrative of ecological awareness, inviting them to be part of an innovative movement that blends high-performance design with responsible craftsmanship.  \n\nThis collaboration sets a new standard in automotive accessories, harmonizing luxury and sustainability in every drive.",
                    image_url:
                        "https://res.cloudinary.com/dkcvg4eui/image/upload/v1748216724/product_images/Adidas%20x%20BMW%20Sustainable%20Car%20Mats.png"
                }
            }
        ]
    }
};

export const useGenerateProducts = (): GenerateProductsHookResponse => {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const submit = async (data: GenerateProductsData): Promise<GenerateProductsResponse> => {
        setError(null);
        setIsLoading(true);
        console.log("received data", data)
        try {
            if (!data.location) {
                throw new Error("Factory location is required.");
            }

            const response = await fetch('http://0.0.0.0:8000/generateproducts', {
                method: 'POST',
                headers: {
                    'accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    source_brand: data.source_brand,
                    plastic_type: data.plastic_type,
                    location: data.location,
                    target_brand: data.target_brand
                })
            });

            if (!response.ok) {
                throw new Error('Failed to generate products');
            }

            const responseData = await response.json();

            console.log("Returning API response", responseData);
            return responseData;
        } catch (err) {
            const errorMessage = (err as Error).message || "Failed to submit form. Please try again.";
            setError(errorMessage);
            throw err;
        } finally {
            setIsLoading(false);
        }
    };

    return { isLoading, error, submit };
};
