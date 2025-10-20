import React, { useState, useEffect } from 'react';

interface LoadingComponentProps {
    gifSrc?: string;
    loadingTexts?: string[];
    showTimer?: boolean;
    timerDuration?: number; // in seconds
    onTimerComplete?: () => void;
    textChangeInterval?: number; // in milliseconds
    className?: string;
}

export const LoadingComponent: React.FC<LoadingComponentProps> = ({
    gifSrc = "/gifs/rotating.gif",
    loadingTexts = [
        "Almost there... Great things take a few seconds",
        "Loading your content...",
        "Just a moment please...",
        "We're preparing something amazing...",
        "Hang tight, we're almost done..."
    ],
    showTimer = false,
    timerDuration = 60,
    onTimerComplete,
    textChangeInterval = 3000,
    className = ""
}) => {
    const [currentTextIndex, setCurrentTextIndex] = useState(0);
    const [timeLeft, setTimeLeft] = useState(timerDuration);

    // Change loading text periodically
    useEffect(() => {
        const textInterval = setInterval(() => {
            setCurrentTextIndex((prevIndex) =>
                (prevIndex + 1) % loadingTexts.length
            );
        }, textChangeInterval);

        return () => clearInterval(textInterval);
    }, [loadingTexts.length, textChangeInterval]);

    // Handle countdown timer
    useEffect(() => {
        if (!showTimer) return;

        const timer = setInterval(() => {
            setTimeLeft((prevTime) => {
                if (prevTime <= 1) {
                    clearInterval(timer);
                    if (onTimerComplete) {
                        onTimerComplete();
                    }
                    return 0;
                }
                return prevTime - 1;
            });
        }, 1000);

        return () => clearInterval(timer);
    }, [showTimer, onTimerComplete]);

    // Format time to display as MM:SS
    const formatTime = (seconds: number): string => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    };

    return (
        <div className={`flex flex-col items-center justify-center min-h-screen bg-white p-8 ${className}`}>
            {/* GIF Container */}
            <div className="mb-8 relative">
              
                    <img
                        src={gifSrc}
                        alt="Loading animation"
                        className="w-[500px] h-full object-contain"
                    />
                
            </div>

            {/* Loading Text */}
            <div className="text-center mb-6 max-w-md">
                <h2 className="text-xl font-semibold text-gray-800 mb-2 transition-opacity duration-500 whitespace-nowrap">
                    {loadingTexts[currentTextIndex]}
                </h2>
              
            
            </div>

            {/* Timer (if enabled) */}
            {showTimer && (
                <div className="text-center">
                    <div className="bg-white rounded-lg shadow-md px-6 py-4 border-l-4 border-blue-500">
                        <p className="text-sm text-gray-600 mb-1">Time remaining:</p>
                        <p className="text-2xl font-mono font-bold text-blue-600">
                            {formatTime(timeLeft)}
                        </p>

                        {/* Progress bar */}
                        <div className="mt-3 w-full bg-gray-200 rounded-full h-2">
                            <div
                                className="bg-blue-500 h-2 rounded-full transition-all duration-1000 ease-linear"
                                style={{
                                    width: `${((timerDuration - timeLeft) / timerDuration) * 100}%`
                                }}
                            />
                        </div>
                    </div>

                    {timeLeft <= 5 && timeLeft > 0 && (
                        <p className="text-orange-600 font-medium mt-2 animate-pulse">
                            Almost ready!
                        </p>
                    )}

                    {timeLeft === 0 && (
                        <p className="text-green-600 font-medium mt-2">
                            Complete!
                        </p>
                    )}
                </div>
            )}
        </div>
    );
};