import { toast } from "react-toastify";

export default function ModelSelector() {
  return (
    <div
      className="flex"
      onClick={() => {
        toast.warn("This feature is not available yet!");
      }}
    >
      <select
        className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
        defaultValue={"GPT4All"}
        disabled={true}
      >
        <option value="GPT4All">GPT4All</option>
        <option value="LlamaCpp">LlamaCpp</option>
      </select>
    </div>
  );
}
