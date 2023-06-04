export const openDocumentsFolder = () => {
  fetch("/api/default/documents/open_in_file_explorer", {
    method: "POST",
  });
};
