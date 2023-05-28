import "@styles/globals.css";
import { Bai_Jamjuree } from "next/font/google";
import "react-toastify/dist/ReactToastify.css";

const bai_jam = Bai_Jamjuree({
  subsets: ["latin", "vietnamese"],
  weight: ["200", "300", "400", "500", "600", "700"],
});

export const metadata = {
  title: "PAutoBot",
  description: "PAutoBot - Your private assistant for automation",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={bai_jam.className}>{children}</body>
    </html>
  );
}
