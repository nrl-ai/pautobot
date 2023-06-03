"use client";
import React from "react";
import UploadIcon from "./icons/UploadIcon";
import { toast } from "react-toastify";
import { useState, useRef, useEffect } from "react";

import { openDocumentsFolder } from "@/utils";
import { clearChatHistory } from "@/lib/requests/chat";

function LoadingIcon() {
  return (
    <svg
      aria-hidden="true"
      role="status"
      className="inline w-4 h-4 mr-3 text-gray-200 animate-spin dark:text-gray-600 ml-2"
      viewBox="0 0 100 101"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
        fill="currentColor"
      />
      <path
        d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
        fill="#1C64F2"
      />
    </svg>
  );
}

export default function SidebarTools() {
  const SUPPORTED_FILE_TYPES = [
    "csv",
    "docx",
    "doc",
    "enex",
    "eml",
    "epub",
    "html",
    "md",
    "msg",
    "odt",
    "pdf",
    "pptx",
    "ppt",
    "txt",
  ];

  const [uploading, setUploading] = useState(false);
  const [ingesting, setIngesting] = useState(false);
  const [file, setFile] = useState(null);
  const fileInput = useRef(null);
  const [documents, setDocuments] = useState([]);

  const refetchDocuments = () => {
    fetch("/api/get_documents", {
      method: "GET",
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
        setDocuments(data);
      })
      .catch((error) => {
        console.error("Error while refetching documents!", error);
        toast.error("Error while refetching documents!");
      });
  };

  useEffect(() => {
    refetchDocuments();
  }, []);

  const checkAndRejectFile = (file) => {
    let fileExtension = file.name?.split(".")?.pop();
    fileExtension = fileExtension?.toLowerCase();
    console.log(fileExtension);
    if (!fileExtension || !SUPPORTED_FILE_TYPES.includes(fileExtension)) {
      toast.error("Unsupported file type!");
      setFile(null);
      fileInput.current.value = "";
      return true;
    }
    return false;
  };

  const uploadFile = (file) => {
    setUploading(true);
    const formData = new FormData();
    formData.append("file", file);
    fetch("/api/upload", {
      method: "POST",
      body: formData,
    })
      .then(async (response) => {
        let data = await response.json();
        if (!response.ok) {
          const error = (data && data.message) || response.status;
          console.log(error);
          return Promise.reject(error);
        }
        toast.success(
          "File uploaded! Ingest your data again before searching."
        );
        setUploading(false);
        setFile(null);
        refetchDocuments();
      })
      .catch((error) => {
        console.error("There was an error!", error);
        toast.error("There was an error!");
        setUploading(false);
        setFile(null);
        refetchDocuments();
      });
  };

  const ingestData = () => {
    setIngesting(true);
    toast.info("Ingesting your data...");
    fetch("/api/ingest", {
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
      <div className="pt-4">
        <div className="flex flex-col items-center justify-center w-full mb-2">
          <div className="mb-2">
            {documents.length > 0 ? (
              <>
                You have {documents.length} document(s).{" "}
                <span
                  className="text-blue-500 cursor-pointer"
                  onClick={() => {
                    openDocumentsFolder();
                  }}
                >
                  Browse Files
                </span>
              </>
            ) : (
              <span>
                You have no document. Please upload a file and ingest data for
                Q&A.
              </span>
            )}
          </div>
          <div
            className="flex flex-col items-center justify-center w-full h-36 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 dark:hover:bg-bray-800 dark:bg-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:hover:border-gray-500 dark:hover:bg-gray-600 p-3 relative"
            onDragOver={(e) => {
              e.stopPropagation();
              e.preventDefault();
            }}
            onDrop={(e) => {
              e.preventDefault();
              if (e.dataTransfer.files.length == 0) return;
              if (checkAndRejectFile(e.dataTransfer.files[0])) return;
              setFile(e.dataTransfer.files[0]);
              fileInput.current.files = e.dataTransfer.files;
            }}
          >
            {file && (
              <div
                className="absolute top-2 right-2"
                onClick={(e) => {
                  setFile(null);
                  fileInput.current.value = "";
                  e.stopPropagation();
                }}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={1.5}
                  stroke="#555555"
                  className="w-6 h-6"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
            )}
            <div className="flex flex-col items-center justify-center pt-5 pb-6">
              {file ? (
                <>
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    height="2rem"
                    viewBox="0 0 384 512"
                  >
                    <path d="M320 464c8.8 0 16-7.2 16-16V160H256c-17.7 0-32-14.3-32-32V48H64c-8.8 0-16 7.2-16 16V448c0 8.8 7.2 16 16 16H320zM0 64C0 28.7 28.7 0 64 0H229.5c17 0 33.3 6.7 45.3 18.7l90.5 90.5c12 12 18.7 28.3 18.7 45.3V448c0 35.3-28.7 64-64 64H64c-35.3 0-64-28.7-64-64V64z" />
                  </svg>
                  <p className="mb-2 text-sm text-gray-500 dark:text-gray-400 mt-4 truncate max-w-[200px]">
                    {file.name}
                  </p>
                </>
              ) : (
                <>
                  <UploadIcon />
                  <p className="mb-2 text-sm text-gray-500 dark:text-gray-400">
                    <span
                      className="font-semibold"
                      onClick={() => {
                        fileInput.current.click();
                      }}
                    >
                      Click to upload
                    </span>{" "}
                    or drag and drop
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400 max-w-[80%]">
                    ({SUPPORTED_FILE_TYPES.join(", ")})
                  </p>
                </>
              )}
            </div>
            <input
              ref={fileInput}
              type="file"
              className="hidden"
              onChange={(e) => {
                if (e.target.files.length == 0) return;
                setFile(e.target.files[0]);
                checkAndRejectFile(e.target.files[0]);
              }}
            />
          </div>
        </div>
      </div>
      <div className="mt-3">
        <button
          className={
            "w-full text-white bg-gray-800 hover:bg-gray-900 focus:outline-none focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-gray-800 dark:hover:bg-gray-700 dark:focus:ring-gray-700 dark:border-gray-700" +
            (uploading ? " opacity-80" : "")
          }
          onClick={() => {
            if (uploading) return;
            if (!file) {
              toast.error("Please select a file!");
              return;
            }
            uploadFile(file);
          }}
        >
          Upload File
          {uploading ? <LoadingIcon /> : null}
        </button>
        <button
          className={
            "w-full text-white bg-gray-800 hover:bg-gray-900 focus:outline-none focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-gray-800 dark:hover:bg-gray-700 dark:focus:ring-gray-700 dark:border-gray-700" +
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
          className="w-full text-white bg-gray-800 hover:bg-gray-900 focus:outline-none focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-gray-800 dark:hover:bg-gray-700 dark:focus:ring-gray-700 dark:border-gray-700"
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
