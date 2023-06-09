import { toast } from "react-toastify";

import { clearChatHistory } from "@/lib/requests/chat";

export default function ModelSelector() {
  const ingestData = () => {
    toast.info("Ingesting your data...");
    fetch("/api/0/documents/ingest", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then(async (response) => {
        let data = await response.json();
        if (!response.ok) {
          const error = (data && data.message) || response.status;
          console.log(error);
          return Promise.reject(error);
        }
      })
      .catch((error) => {
        console.error("There was an error!", error);
        toast.error(error);
      });
  };

  return (
    <>
      <div className="text-lg font-bold mt-4">This Context</div>
      <div className="mt-3">
        <button
          className={
            "w-full text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2"
          }
          onClick={() => {
            ingestData();
          }}
        >
          Ingest Data
        </button>
        <button
          className="w-full text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2"
          onClick={() => {
            clearChatHistory().then(() => {
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
