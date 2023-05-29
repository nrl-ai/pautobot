import "@styles/globals.css";
import { Bai_Jamjuree } from "next/font/google";
import "react-toastify/dist/ReactToastify.css";

const bai_jam = Bai_Jamjuree({
  subsets: ["latin", "vietnamese"],
  weight: ["200", "300", "400", "500", "600", "700"],
});

export default function RootLayout({ Component, pageProps}) {
  return (
    <div className={bai_jam.className}>
      <Component {...pageProps} />
    </div>
  );
}
