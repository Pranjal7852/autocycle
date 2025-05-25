import { useLocation, Link } from "react-router-dom";
import { useEffect } from "react";

const NotFound = () => {
  const location = useLocation();

  useEffect(() => {
    console.error(
      "404 Error: User attempted to access non-existent route:",
      location.pathname
    );
  }, [location.pathname]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-background">
      <div className="text-center">
        <h1 className="text-5xl font-bold text-primary font-poppins mb-4">404</h1>
        <p className="text-xl text-muted-foreground mb-6 font-mulish">Oops! Page not found</p>
        <Link
          to="/"
          className="inline-block font-poppins bg-primary text-primary-foreground px-6 py-3 rounded-lg shadow hover:bg-primary/90 transition"
        >
          Return to Home
        </Link>
      </div>
    </div>
  );
};

export default NotFound;