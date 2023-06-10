import { ToastContainer } from "react-toastify";

import Sidebar from "@/components/Sidebar";
import Main from "@/components/Main";
import SidebarTools from "@/components/RightSidebar";

export default function Home() {
  return (
    <div className="w-full h-screen flex flex-row">
      <div className="h-screen grow-0">
        <Sidebar />
      </div>
      <div className="h-screen overflow-auto grow relative">
        <Main />
        <ToastContainer />
      </div>
      <div className="h-screen grow-0 w-[360px] p-4 bg-gray-100 border-l-2">
        <SidebarTools />
      </div>
    </div>
  );
}
