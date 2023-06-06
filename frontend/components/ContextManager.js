import { toast } from "react-toastify";
import { useState } from "react";

import { clearChatHistory } from "@/lib/requests/chat";
import LoadingIcon from "./icons/LoadingIcon";

export default function ModelSelector() {
  const [ingesting, setIngesting] = useState(false);
  const ingestData = () => {
    setIngesting(true);
    toast.info("Ingesting your data...");
    fetch("/api/default/documents/ingest", {
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
        toast.success("All data has been ingested!");
        setIngesting(false);
      })
      .catch((error) => {
        console.error("There was an error!", error);
        toast.error("There was an error!");
        setIngesting(false);
      });
  };

  return (
    <>
      <div className="text-lg font-bold mt-4">This Context</div>
      <div className="mt-3">
        <button
          className={
            "w-full text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2" +
            (ingesting ? " opacity-80" : "")
          }
          onClick={() => {
            if (ingesting) return;
            ingestData();
          }}
        >
          Ingest Data
          {ingesting ? <LoadingIcon /> : null}
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
