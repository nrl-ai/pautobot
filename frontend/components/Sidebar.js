import SidebarTools from "./SidebarTools";
import ModelSelector from "./ModelSelector";
import SidebarMenu from "./SidebarMenu";

export default function Sidebar() {
  return (
    <>
      <div className="p-2 h-full">
        <div className="bg-gray-300 shadow-md w-full h-full pt-8 px-4 pb-4 rounded-2xl">
          <div align="center" className="mb-4">
            <img
              alt="PAutoBot"
              className="w-12 h-auto mx-auto mb-2"
              src="/pautobot.png"
            />
            <h1 align="center" className="text-3xl font-semibold">
              🔥 PⒶutoBot 🔥
            </h1>
            <p align="center">Your private task assistant with GPT</p>
          </div>
          <SidebarMenu />
          <ModelSelector />
          <SidebarTools />
        </div>
      </div>
    </>
  );
}
