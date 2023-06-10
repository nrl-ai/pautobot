import { toast } from "react-toastify";

import { clearChatHistory } from "@/lib/requests/history";
import { ingestData } from "@/lib/requests/documents";

export default function ModelSelector() {
  return (
    <>
      <div className="text-lg font-bold mt-4">This Context</div>
      <div className="mt-3">
        <button
          className={
            "w-full text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2"
          }
          onClick={() => {
            toast.info("Ingesting data...");
            ingestData(0)
              .catch((error) => {
                toast.error(error);
              });
          }}
        >
          Ingest Data
        </button>
        <button
          className="w-full text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2"
          onClick={() => {
            clearChatHistory(0).then(() => {
              toast.success("Chat history cleared!");
              window.location.reload();
            });
          }}
        >
          Clear History
        </button>
      </div>
    </>
  );
}
