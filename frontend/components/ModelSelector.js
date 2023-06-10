export default function ModelSelector() {
  return (
    <>
      <div className="text-lg font-bold mt-4">Model</div>
      <div className="flex">
        <select
          className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 mt-2"
          defaultValue={"GPT4All-J v1.3-groovy"}
        >
          <option value="GPT4All-J v1.3-groovy">GPT4All-J v1.3-groovy</option>
        </select>
      </div>
      <div className="mt-4 ml-2 text-sm">
        <div>
          <span className="font-bold">Source:</span> <a href="https://gpt4all.io/index.html" target="_blank" rel="noreferrer">gpt4all.io</a>
        </div>
        <div>
          <span className="font-bold">License:</span> Apache 2.0
        </div>
      </div>
    </>
  );
}
