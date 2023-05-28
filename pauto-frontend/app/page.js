"use client";
import Sidebar from "@components/Sidebar";
import Main from "@components/Main";
import { ToastContainer } from "react-toastify";

export default function Home() {
  return (
    <>
      <div className="relative w-full h-full">
        <div className="bg-gray-200 shadow-md fixed w-[400px] h-full top-0">
          <Sidebar />
        </div>
        <div className="h-full fixed left-[400px] right-0 top-0 bottom-0 overflow-auto">
          <Main />
          <ToastContainer />
        </div>
      </div>
    </>
  );
}
