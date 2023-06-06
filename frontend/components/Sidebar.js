import SidebarTopMenu from "./SidebarTopMenu";
import SidebarBottomMenu from "./SidebarBottomMenu";

export default function Sidebar() {
  return (
    <>
      <div className="h-full shadow-md">
        <div className="bg-[#007FF4] w-full h-full flex flex-col shadow-lg">
          <div align="center" className="mb-16 pt-4 px-2 pb-4 grow-0">
            <img
              alt="PAutoBot"
              className="w-10 h-auto mx-auto mb-2 p-2 rotate-logo hover:rotate-0 transition bg-white rounded-md"
              src="/pautobot.png"
            />
            <h1 align="center" className="text-md font-semibold text-white">
              PAuto
            </h1>
          </div>
          <div className="flex flex-col grow">
            <div className="grow">
              <SidebarTopMenu />
            </div>
            <div className="grow-0">
              <SidebarBottomMenu />
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
