export default function ModelSelector() {
  return (
    <>
      <div className="text-lg font-bold mt-4">Model</div>
      <div className="flex">
        <select
          className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 mt-2"
          defaultValue={"GPT4All"}
        >
          <option value="GPT4All">GPT4All</option>
        </select>
      </div>
      <div className="mt-4 ml-2 text-sm">
        <div>
          <span className="font-bold">Source:</span> GPT4All
        </div>
        <div>
          <span className="font-bold">License:</span> Apache 2.0
        </div>
      </div>
    </>
  );
}
