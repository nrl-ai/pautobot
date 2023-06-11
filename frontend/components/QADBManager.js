import { toast } from "react-toastify";
import { useState, useRef, useEffect } from "react";

import LoadingIcon from "./icons/LoadingIcon";
import {
  openDocument,
  deleteDocument,
  getDocuments,
  uploadDocument,
} from "@/lib/requests/documents";
import { getBotInfo } from "@/lib/requests/bot";

export default function ModelSelector() {
  const SUPPORTED_FILE_TYPES = [
    ".csv",
    ".docx",
    ".doc",
    ".enex",
    ".eml",
    ".epub",
    ".html",
    ".md",
    ".msg",
    ".odt",
    ".pdf",
    ".pptx",
    ".ppt",
    ".txt",
    ".zip",
  ];

  const fileInput = useRef(null);
  const [dragging, setDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [documents, setDocuments] = useState([]);
  const refetchDocuments = (contextId) => {
    getDocuments(contextId)
      .then((data) => {
        setDocuments(data);
      })
      .catch((error) => {
        toast.error(error);
      });
  };
  useEffect(() => {
    refetchDocuments(0);
  }, []);

  const [botInfo, setBotInfo] = useState(null);
  const getAndSetBotInfo = () => {
    getBotInfo()
      .then((data) => {
        setBotInfo(data);
      })
      .catch((error) => {
        toast.error(error);
      });
  };

  // Periodically get bot info every 5 seconds
  useEffect(() => {
    getAndSetBotInfo();
    const interval = setInterval(() => {
      getAndSetBotInfo();
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const isValidFile = (file) => {
    let fileExtension = file.name?.split(".")?.pop();
    fileExtension = fileExtension?.toLowerCase();
    if (!fileExtension || !SUPPORTED_FILE_TYPES.includes("." + fileExtension)) {
      return false;
    }
    return true;
  };

  const uploadFiles = async (files) => {
    if (!files || files.length == 0) {
      toast.error("No file selected.");
      return;
    }

    // Clone the files array
    files = [...files];

    // Start uploading
    setUploading(true);

    let numUploaded = 0;
    let numFailed = 0;
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      if (!isValidFile(file)) {
        toast.error(
          "File type not supported: " + file.name
        );
        numFailed++;
        continue;
      }
      await uploadDocument(0, file)
        .then(async (response) => {
          numUploaded++;
          refetchDocuments(0);
        })
        .catch((error) => {
          toast.error(error);
          numFailed++;
          refetchDocuments(0);
        });
    }

    toast.info(
      "Uploaded " +
        numUploaded +
        " file(s). " +
        (numFailed > 0 ? "Failed to upload " + numFailed + " file(s)." : "")
    );
    fileInput.current.value = "";
    setUploading(false);
  };

  return (
    <>
      <div className="text-lg font-bold mt-4">Q&A Database</div>
      <div className="mb-2 text-sm">
        {documents.length > 0 ? (
          <span>You have {documents.length} document(s). </span>
        ) : (
          <span>
            You have no document. Please upload a file and ingest data for Q&A.
          </span>
        )}
      </div>
      <div className="relative rounded-lg overflow-hidden max-h-[200px] mb-4"
        onDragOver={
          (e) => {
            e.preventDefault();
            e.stopPropagation();
          }
        }
        onDragEnter={
          (e) => {
            e.preventDefault();
            e.stopPropagation();
            setDragging(true);
          }
        }
        onDragLeave={
          (e) => {
            e.preventDefault();
            e.stopPropagation();
            setDragging(false);
          }
        }
        onDrop={
          (e) => {
            e.preventDefault();
            e.stopPropagation();
            uploadFiles(e.dataTransfer.files);
          }
        }
      >
        {dragging && (
          <div className="absolute inset-0 flex flex-col items-center justify-center bg-gray-100 dark:bg-gray-800 bg-opacity-50">
            <div className="text-gray-500 dark:text-gray-400">
              Drop files to upload
            </div>
          </div>
        )}
        <table className="w-full text-sm text-left text-gray-500 dark:text-gray-400">
          <tbody>
            {documents.map((document, key) => (
              <tr key={document.id} className="bg-white dark:bg-gray-700">
                <td className="pl-2">{key + 1}.</td>
                <td className="px-0 py-1.5 whitespace-nowrap max-w-[150px] overflow-hidden">
                  {document.name}
                </td>
                <td className="pl-2 whitespace-nowrap">
                  <button
                    onClick={() => {
                      openDocument(0, document.id);
                    }}
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      strokeWidth={1.5}
                      stroke="currentColor"
                      className="w-5 h-5 ml-2"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="M3.75 9.776c.112-.017.227-.026.344-.026h15.812c.117 0 .232.009.344.026m-16.5 0a2.25 2.25 0 00-1.883 2.542l.857 6a2.25 2.25 0 002.227 1.932H19.05a2.25 2.25 0 002.227-1.932l.857-6a2.25 2.25 0 00-1.883-2.542m-16.5 0V6A2.25 2.25 0 016 3.75h3.879a1.5 1.5 0 011.06.44l2.122 2.12a1.5 1.5 0 001.06.44H18A2.25 2.25 0 0120.25 9v.776"
                      />
                    </svg>
                  </button>
                  <button
                    onClick={() => {
                      let confirmation = confirm(
                        "Are you sure you want to delete this document?"
                      );
                      if (confirmation) {
                        deleteDocument(0, document.id)
                          .then((response) => {
                            toast.success("Document deleted!");
                            refetchDocuments(0);
                          })
                          .catch((error) => {
                            toast.error(error);
                          });
                      }
                    }}
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      strokeWidth={1.5}
                      stroke="currentColor"
                      className="w-5 h-5 ml-2"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0"
                      />
                    </svg>
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {botInfo?.is_ingesting_data && (
        <div className="text-sm text-gray-500 dark:text-gray-400">
          <span>
            <span className="font-bold text-orange-400">Note:</span> The bot is
            currently ingesting data. Please wait until it finishes.
          </span>
          <LoadingIcon />
        </div>
      )}
      <div className="mt-3">
        <input
          className="hidden"
          type="file"
          ref={fileInput}
          accept={SUPPORTED_FILE_TYPES.join(",")}
          multiple={true}
          onChange={(e) => {
            uploadFiles(e.target.files);
          }}
        />
        <button
          className={
            "w-full py-2.5 px-5 mr-2 mb-2 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-200" +
            (uploading ? " opacity-80" : "")
          }
          onClick={() => {
            if (uploading) return;
            fileInput.current.click();
          }}
        >
          Upload Files
          {uploading ? <LoadingIcon /> : null}
        </button>
      </div>
    </>
  );
}
