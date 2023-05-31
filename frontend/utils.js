export const openDocumentsFolder = () => {
  fetch("/api/open_in_file_explorer", {
    method: "POST",
  });
};
