import { useState } from 'react';
import axios from 'axios';
import Sidebar, { SidebarItem } from '../components/Sidebar';
import { HomeIcon, UsersIcon } from 'lucide-react';

export default function Statistical() {
  const [input, setInput] = useState('');
  const [kValue, setKValue] = useState(1);
  const [output, setOutput] = useState('');
  const [topKOutput, setTopKOutput] = useState([]);

  const handleInputChange = (e) => setInput(e.target.value);
  const handleKChange = (e) => setKValue(parseInt(e.target.value) || 1);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post(`http://127.0.0.1:8000/transliterate_statistical`, {
        word: input,
        k: kValue
      });

      if (kValue === 1) {
        setOutput(response.data.result || '');
        setTopKOutput([]);
      } else {
        setOutput('');
        setTopKOutput(response.data.top_k || []);
      }
    } catch (error) {
      console.error('Error occurred during transliteration:', error);
    }
  };

  return (
    <div className="flex h-screen w-screen overflow-hidden">
      {/* Sidebar */}
      <div className="h-full">
        <Sidebar>
          <SidebarItem icon={<HomeIcon />} text="Pure Rule Based" to="/" />
          <SidebarItem icon={<UsersIcon />} text="Statistical Approach" to="/statistical" active />
        </Sidebar>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-auto p-6 bg-gray-100">
        <div className="max-w-5xl mx-auto">
          <h1 className="text-3xl font-bold text-center mb-6">
            Statistical Transliteration System
          </h1>

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Input text */}
            <div>
              <label htmlFor="input_text" className="block mb-2 text-lg font-medium text-gray-800">
                Text in Pracalit
              </label>
              <textarea
                id="input_text"
                value={input}
                onChange={handleInputChange}
                className="bg-white w-full p-3 rounded-lg border border-gray-300 resize-y min-h-[120px]"
                placeholder="Namaste"
              />
            </div>

            {/* Input for K */}
            <div>
              <label htmlFor="k_value" className="block mb-2 text-lg font-medium text-gray-800">
                Value of K (number of top results)
              </label>
              <input
                id="k_value"
                type="number"
                min={1}
                value={kValue}
                onChange={handleKChange}
                className="bg-white w-32 p-2 rounded-lg border border-gray-300"
              />
            </div>

            {/* Output */}
            {kValue === 1 && (
              <div>
                <label className="block mb-2 text-lg font-medium text-gray-800">
                  Transliteration Result
                </label>
                <textarea
                  value={output}
                  disabled
                  className="w-full p-3 rounded-lg border border-gray-300 bg-gray-200 resize-y min-h-[100px]"
                />
              </div>
            )}

            {/* Top-K Output */}
            {kValue > 1 && topKOutput.length > 0 && (
              <div>
                <label className="block mb-2 text-lg font-medium text-gray-800">
                  Top {kValue} Suggestions
                </label>
                <ul className="list-disc list-inside bg-white p-4 rounded-lg border border-gray-300">
                  {topKOutput.map((suggestions, index) => (
                    <li key={index}>
                      <strong>Word {index + 1}:</strong> {suggestions.join(', ')}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Submit button */}
            <div className="flex justify-center">
              <button
                type="submit"
                className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-2 rounded-lg"
              >
                Transliterate
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
