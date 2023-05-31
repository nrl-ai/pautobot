import "@styles/globals.css";
import "react-toastify/dist/ReactToastify.css";

import { Bai_Jamjuree } from "next/font/google";
import Head from "next/head";

const bai_jam = Bai_Jamjuree({
  subsets: ["latin", "vietnamese"],
  weight: ["200", "300", "400", "500", "600", "700"],
});

export default function RootLayout({ Component, pageProps }) {
  return (
    <>
      <Head>
        <title>PAutoBot - Your Private GPT Assistant</title>
      </Head>
      <div className={bai_jam.className}>
        <Component {...pageProps} />
      </div>
    </>
  );
}
